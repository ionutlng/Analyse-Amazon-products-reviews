from django.shortcuts import render


def home_page(request):
    return render(request, 'scraper_interface/home_page.html')
