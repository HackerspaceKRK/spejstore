from django.shortcuts import render, get_object_or_404
from storage.models import Item
from django.contrib.postgres.search import SearchVector
import shlex

def apply_smart_search(query, objects):
    general_term = []

    filters = {}

    for prop in shlex.split(query):
        if ':' not in prop:
            general_term.append(prop)
        else:
            key, value = prop.split(':', 1)
            if hasattr(Item, key):
                filters[key + '__search'] = value
            elif key == 'ancestor':
                objects = Item.objects.get(pk=value).get_children()
            elif key == 'prop' or value:
                if key == 'prop':
                    key, value = value.split(':', 1)

                if 'props__contains' not in filters:
                    filters['props__contains'] = {}
                filters['props__contains'] = {key: value}

            else:
                # "Whatever:"
                general_term.append(prop)

    if general_term:
        objects = objects.annotate(
            search=SearchVector('name', 'description', 'props'),
            )
        filters['search'] = ' '.join(general_term)

    objects = objects.filter(**filters)

    return objects

def index(request):
    return render(request, 'index.html')

def search(request):
    query = request.GET.get('q', '')

    results = apply_smart_search(query, Item.objects)
    return render(request, 'results.html', {
        'query': query,
        'results': results.all(),
        })

def item_display(request, pk):
    if not pk:
        return render(request, 'results.html', {
            'results': Item.get_roots()
            })
    item = get_object_or_404(Item, pk=pk)

    return render(request, 'item.html', {
        'item': item,
        'ancestors': item.get_ancestors(),
        'children': item.get_children(),
        })
