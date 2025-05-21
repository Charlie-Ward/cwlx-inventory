from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.graphics.barcode import code128
from reportlab.lib.units import cm

def generate_barcodes_pdf(filename="barcodes.pdf", start=1, count=100):
    # PDF setup
    page_width, page_height = A4
    c = canvas.Canvas(filename, pagesize=A4)

    barcode_width = 4 * cm
    barcode_height = 1 * cm
    margin_x = 1 * cm
    margin_y = 1 * cm
    spacing_x = 0.5 * cm
    spacing_y = 0.5 * cm

    # Calculate how many barcodes fit per row and column
    barcodes_per_row = int((page_width - 2 * margin_x + spacing_x) // (barcode_width + spacing_x))
    barcodes_per_col = int((page_height - 2 * margin_y + spacing_y) // (barcode_height + spacing_y))

    barcodes_per_page = barcodes_per_row * barcodes_per_col

    for i in range(count):
        page_num = i // barcodes_per_page
        position_in_page = i % barcodes_per_page

        if i > 0 and position_in_page == 0:
            c.showPage()  # Start a new page

        row = position_in_page // barcodes_per_row
        col = position_in_page % barcodes_per_row

        x = margin_x + col * (barcode_width + spacing_x)
        y = page_height - margin_y - (row + 1) * (barcode_height + spacing_y)

        number = f"{start + i:012d}"  # 12-digit padded number
        barcode = code128.Code128(number, barWidth=barcode_width / 100, barHeight=barcode_height)
        barcode.drawOn(c, x, y)

        # Optional: draw text below the barcode
        c.setFont("Helvetica", 6)
        c.drawCentredString(x + barcode_width / 2, y - 0.3 * cm, number)

    c.save()
    print(f"Saved PDF with {count} barcodes as {filename}")

# Example usage
generate_barcodes_pdf("generated_barcodes.pdf", start=1, count=200)
