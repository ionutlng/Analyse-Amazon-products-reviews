from django.shortcuts import render


def home_page(request):
    return render(request, 'big_project/home_page.html')
