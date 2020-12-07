from django.shortcuts import render


def index(request):
    return render(request, 'interface/search_item.html')
