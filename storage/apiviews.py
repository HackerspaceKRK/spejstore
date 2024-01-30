from rest_framework import viewsets, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from storage.authentication import LanAuthentication

from storage.models import Item, Label
from storage.serializers import ItemSerializer, LabelSerializer
from django.http import Http404

from storage.views import apply_smart_search


def api_print(quantity, obj):
    amount = min(int(quantity), 5)
    for _ in range(amount):
        obj.print()
    return Response({"status": "success"})


class SmartSearchFilterBackend(filters.BaseFilterBackend):
    """
    Filters query using smartsearch filter
    """

    def filter_queryset(self, request, queryset, view):
        search_query = request.query_params.get("smartsearch", None)
        if search_query:
            return apply_smart_search(search_query, queryset)

        return queryset


class LabelViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows items to be viewed or edited.
    """

    queryset = Label.objects.all()
    serializer_class = LabelSerializer


class ItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows items to be viewed or edited.
    """

    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    filter_backends = (SmartSearchFilterBackend, filters.OrderingFilter)
    ordering_fields = "__all__"

    def get_queryset(self):
        return Item.objects.filter(**{"path__level": 1})

    def get_object(self):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        obj = self.get_item_by_id_or_label(self.kwargs[lookup_url_kwarg])
        self.check_object_permissions(self.request, obj)

        return obj

    def get_item_by_id_or_label(self, id):
        try:
            item = Item.objects.get(uuid__startswith=id)  # look up by short id
            return item
        except Item.DoesNotExist:
            try:
                label = Label.objects.get(pk=id)
                return label.item
            except Label.DoesNotExist:
                raise Http404()

    @action(
        detail=True,
        methods=["post"],
        # AllowAny is correct here, as we require LanAuthentication anyways
        permission_classes=[AllowAny],
        authentication_classes=[LanAuthentication],
    )
    def print(self, request, pk):
        return api_print(request.query_params.get("quantity", 1), self.get_object())

    @action(detail=True, authentication_classes=[LanAuthentication])
    def children(self, request, pk):
        item = self.get_object()
        return Response(
            self.serializer_class(item.get_children().all(), many=True).data
        )

    @action(detail=True, authentication_classes=[LanAuthentication])
    def ancestors(self, request, pk):
        item = self.get_object()
        return Response(
            self.serializer_class(item.get_ancestors().all(), many=True).data
        )

    @action(detail=True, authentication_classes=[LanAuthentication])
    def descendants(self, request, pk):
        item = self.get_object()
        return Response(
            self.serializer_class(item.get_descendants().all(), many=True).data
        )

    @action(detail=True, authentication_classes=[LanAuthentication])
    def siblings(self, request, pk):
        item = self.get_object()
        return Response(
            self.serializer_class(item.get_siblings().all(), many=True).data
        )
