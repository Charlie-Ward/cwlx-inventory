#!/bin/bash
cd /Users/charlieward/Documents/lighting-inventory
source venv/bin/activate
export DJANGO_DEBUG=False
export DJANGO_SECRET_KEY='jd=bjl3&!ui$b*^@p(n-!+*&4*h#3615fn2zl^oem4!e(3lief'
gunicorn lighting_inventory_manager.wsgi --bind 127.0.0.1:8000