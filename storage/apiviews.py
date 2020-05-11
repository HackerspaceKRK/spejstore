from rest_framework import viewsets, generics, filters
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from rest_framework.permissions import AllowAny

from storage.models import Item, Label
from storage.serializers import ItemSerializer, LabelSerializer
from django.shortcuts import get_object_or_404

from storage.views import apply_smart_search


class SmartSearchFilterBackend(filters.BaseFilterBackend):
    """
    Filters query using smartsearch filter
    """

    def filter_queryset(self, request, queryset, view):
        search_query = request.query_params.get('smartsearch', None)
        if search_query:
            return apply_smart_search(search_query, queryset)

        return queryset


class LabelViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows items to be viewed or edited.
    """
    queryset = Label.objects
    serializer_class = LabelSerializer

    @detail_route(methods=['post'], permission_classes=[AllowAny])
    def print(self, request, pk):
        quantity = min(int(request.query_params.get('quantity', 1)), 5)
        obj = self.get_object()
        for _ in range(quantity):
            obj.print()
        return obj


class ItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows items to be viewed or edited.
    """
    queryset = Item.objects
    serializer_class = ItemSerializer
    filter_backends = (SmartSearchFilterBackend, filters.OrderingFilter)
    ordering_fields = '__all__'


    def get_queryset(self):
        return Item.get_roots()

    def get_object(self):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        obj = get_object_or_404(Item, pk=self.kwargs[lookup_url_kwarg])
        self.check_object_permissions(self.request, obj)

        return obj

    @detail_route()
    def children(self, request, pk):
        item = self.get_object()
        return Response(self.serializer_class(item.get_children().all(), many=True).data)

    @detail_route()
    def ancestors(self, request, pk):
        item = self.get_object()
        return Response(self.serializer_class(item.get_ancestors().all(), many=True).data)

    @detail_route()
    def descendants(self, request, pk):
        item = self.get_object()
        return Response(self.serializer_class(item.get_descendants().all(), many=True).data)

    @detail_route()
    def siblings(self, request, pk):
        item = self.get_object()
        return Response(self.serializer_class(item.get_siblings().all(), many=True).data)
