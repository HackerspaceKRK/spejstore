from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.decorators import detail_route

from storage.models import Item
from storage.serializers import ItemSerializer
from django.shortcuts import get_object_or_404


class ItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows items to be viewed or edited.
    """
    queryset = Item.objects
    serializer_class = ItemSerializer

    def get_queryset(self):
        return Item.get_roots()

    def get_object(self):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        obj = get_object_or_404(Item, pk=self.kwargs[lookup_url_kwarg])
        self.check_object_permissions(self.request, obj)

        return obj

    @detail_route()
    def children(self, request, pk):
        """
        Returns a list of all the group names that the given
        user belongs to.
        """
        item = self.get_object()
        return Response(self.serializer_class(item.get_children().all(), many=True).data)
