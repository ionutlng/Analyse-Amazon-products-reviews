from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q, Count, F
from .models import Item
from django.views.generic import DetailView


def index(request):
    return render(request, 'interface/search_item.html')


class ItemDV(DetailView):
    model = Item
    context_object_name = 'item'
    template_name = 'interface/snippets/item_details.html'
    http_method_names = ['get']


def get_items(request, search_input):
    if request.method == "GET":
        inputs = search_input.lower().split("_")
        items_filter = []

        for string in inputs:
            items_filter.append(Q(name__icontains=string))

        items_query = items_filter.pop()

        for item in range(0, len(inputs) - 1):
            items_query |= items_filter[item]

        filters = items_query  # let this as it is just because maybe in the future there will be more than 1 filter

        qs = (Item.objects
                  .filter(filters)
                  .annotate(name_filter_cnt=Count('id', filter=items_query))
                  .annotate(total_filter_cnt=F('name_filter_cnt'))
                  .order_by('-total_filter_cnt')[:6])

        response = JsonResponse([f'{item.id},{item.name}' for item in qs], safe=False)
        return response
