from django.shortcuts import render, redirect
from django.urls import reverse
import csv
from django.conf import settings
from django.core.paginator import Paginator

def index(request):
    return redirect(reverse(bus_stations))


def bus_stations(request):
    with open(settings.BUS_STATION_CSV, encoding='cp1251') as f:
        contents = csv.DictReader(f)
        stops_list = list(contents)
    if request.GET.get('page'):
        page_number = int(request.GET.get('page'))
    else:
        page_number = 1
    paginator = Paginator(stops_list, 10)
    if page_number in range(1, paginator.num_pages):
        stops_page = paginator.page(page_number)
    else:
        stops_page = paginator.page(paginator.num_pages)
    current_page = stops_page.number
    prev_page_url = f'?page={stops_page.previous_page_number()}'\
        if stops_page.has_previous() else None
    next_page_url = f'?page={stops_page.next_page_number()}'\
        if stops_page.has_next() else None
    return render(request, 'index.html', context={
        'bus_stations': stops_page,
        'current_page': current_page,
        'prev_page_url': prev_page_url,
        'next_page_url': next_page_url,
    })


