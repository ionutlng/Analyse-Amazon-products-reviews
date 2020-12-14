from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q, Count, F
from .models import Item


def index(request):
    return render(request, 'interface/search_item.html')


def get_items(request, search_input):
    if request.method == "GET":
        inputs = search_input.lower().split("_")
        items_filter = []

        for string in inputs:
            items_filter.append(Q(name=string))

        items_query = items_filter.pop()

        for item in range(0, len(inputs) - 1):
            items_query |= items_filter[item]

        filters = items_query  # let this as it is just because maybe in the future there will be more than 1 filter

        qs = (Item.objects
                  .filter(filters)
                  .annotate(name=Count('id', filter=items_query))
                  .annotate(total_filter_cnt=F('name'))
                  .order_by('-total_filter_cnt')[:10])

        response = JsonResponse([f'{item.name}' for item in qs], safe=False)
        return response
