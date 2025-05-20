from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import JsonResponse
from django.db.models import Q
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required

from inventory.models import Product, InventoryItem
from .models import AssignedItem, Booking, Client
from .forms import BookingForm, ClientForm

# --- SCAN CHECK ---
def scan_check(request):
    message = None
    item = None
    assigned = None

    if request.method == 'POST':
        barcode = request.POST.get('barcode', '').strip()
        try:
            item = InventoryItem.objects.get(barcode=barcode)
            assigned = AssignedItem.objects.filter(inventory_item=item).order_by('-booking__start_date').first()
            if assigned:
                if not assigned.checked_out:
                    assigned.checked_out = True
                    message = f"✅ {item.product.name} checked out for {assigned.booking.event_name}."
                elif not assigned.checked_in:
                    assigned.checked_in = True
                    message = f"✅ {item.product.name} checked in from {assigned.booking.event_name}."
                else:
                    message = f"ℹ️ {item.product.name} has already been checked in."
                assigned.save()
            else:
                message = f"❌ Item '{item.product.name}' is not assigned to any booking."
        except InventoryItem.DoesNotExist:
            message = "❌ No item found with that barcode."

    return render(request, 'bookings/scan_check.html', {
        'message': message,
        'item': item,
        'assigned': assigned
    })

# --- CREATE BOOKING ---
def create_booking(request):
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save()
            return redirect('bookings:manage_booking', booking_id=booking.pk)
    else:
        form = BookingForm()

    # # Dynamically filter available items for the form
    # start_date = request.POST.get('start_date') or None
    # end_date = request.POST.get('end_date') or None

    # available_items = InventoryItem.objects.filter(is_available=True)
    # if start_date and end_date:
    #     overlapping_bookings = Booking.objects.filter(
    #         Q(start_date__lte=end_date) & Q(end_date__gte=start_date)
    #     )
    #     booked_item_ids = AssignedItem.objects.filter(
    #         booking__in=overlapping_bookings
    #     ).values_list('inventory_item_id', flat=True)
    #     available_items = available_items.exclude(id__in=booked_item_ids)

    # form.fields['items'].queryset = available_items

    return render(request, 'bookings/create_booking.html', {'form': form})

# --- MANAGE BOOKING ---
def manage_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    assigned_items = AssignedItem.objects.filter(booking=booking)

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "add_items":
            item_ids = request.POST.getlist("new_items")
            for item_id in item_ids:
                item = InventoryItem.objects.filter(id=item_id).first()
                # Only assign if not already assigned to this booking
                if item and not AssignedItem.objects.filter(booking=booking, inventory_item=item).exists():
                    AssignedItem.objects.create(booking=booking, inventory_item=item)
        elif action == "remove_item":
            item_id = request.POST.get("item_id")
            assigned_item = AssignedItem.objects.filter(booking=booking, inventory_item_id=item_id).first()
            if assigned_item:
                assigned_item.delete()
        elif action == "check_out":
            item_id = request.POST.get("item_id")
            assigned = AssignedItem.objects.filter(booking=booking, inventory_item_id=item_id).first()
            if assigned and not assigned.checked_out:
                assigned.checked_out = True
                assigned.save()
        elif action == "check_in":
            item_id = request.POST.get("item_id")
            assigned = AssignedItem.objects.filter(booking=booking, inventory_item_id=item_id).first()
            if assigned and assigned.checked_out and not assigned.checked_in:
                assigned.checked_in = True
                assigned.save()
        return redirect('bookings:manage_booking', booking_id=booking.pk)

    # Only exclude items assigned to bookings that overlap in dates
    overlapping_bookings = Booking.objects.filter(
        Q(start_date__lte=booking.end_date) & Q(end_date__gte=booking.start_date)
    ).exclude(pk=booking.pk)
    booked_item_ids = AssignedItem.objects.filter(
        booking__in=overlapping_bookings
    ).values_list('inventory_item_id', flat=True)
    already_assigned_ids = assigned_items.values_list('inventory_item_id', flat=True)
    available_items = InventoryItem.objects.filter(is_available=True).exclude(
        id__in=booked_item_ids
    ).exclude(
        id__in=already_assigned_ids
    )

    return render(request, 'bookings/manage_booking.html', {
        'booking': booking,
        'assigned_items': assigned_items,
        'available_items': available_items
    })

# --- HOME ---
def home(request):
    upcoming_bookings = Booking.objects.filter(start_date__gte=now().date()).order_by('start_date')[:5]
    context = {
        'upcoming_bookings': upcoming_bookings
    }
    return render(request, 'bookings/home.html', context)

# --- BOOKING LIST ---
def booking_list(request):
    today = now().date()
    upcoming_bookings = Booking.objects.filter(end_date__gte=today).order_by('start_date')
    past_bookings = Booking.objects.filter(end_date__lt=today).order_by('-end_date')
    return render(request, 'bookings/booking_list.html', {
        'upcoming_bookings': upcoming_bookings,
        'past_bookings': past_bookings,
    })

# --- AVAILABLE ITEMS API ---
def available_items_api(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    items = []

    if start_date and end_date:
        overlapping_bookings = Booking.objects.filter(
            Q(start_date__lte=end_date) & Q(end_date__gte=start_date)
        )
        booked_item_ids = AssignedItem.objects.filter(
            booking__in=overlapping_bookings
        ).values_list('inventory_item_id', flat=True)
        available_items = InventoryItem.objects.exclude(id__in=booked_item_ids)
    else:
        available_items = InventoryItem.objects.all()

    for item in available_items:
        items.append({'id': item.pk, 'text': str(item)})

    return JsonResponse({'results': items})

# --- DELETE BOOKING ---
def delete_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if request.method == "POST":
        booking.delete()
        return redirect(reverse('home'))
    return redirect(reverse('bookings:manage_booking', args=[booking_id]))

# --- MANAGE CLIENTS ---
def manage_clients(request):
    clients = Client.objects.all().order_by('name')
    return render(request, 'bookings/manage_clients.html', {'clients': clients})

def client_detail(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    bookings = Booking.objects.filter(client=client).order_by('-start_date')
    return render(request, 'bookings/client_detail.html', {
        'client': client,
        'bookings': bookings
    })

def edit_client(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    if request.method == "POST":
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('bookings:client_detail', client_id=client.pk)
    else:
        form = ClientForm(instance=client)
    return render(request, 'bookings/edit_client.html', {'form': form, 'client': client})

def delete_client(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    if request.method == "POST":
        client.delete()
        return redirect('bookings:manage_clients')
    return redirect('bookings:client_detail', client_id=client.pk)

def add_client(request):
    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save()
            return redirect('bookings:client_detail', client_id=client.id)
    else:
        form = ClientForm()
    return render(request, 'bookings/add_client.html', {'form': form})