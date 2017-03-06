from storage.models import Item
from rest_framework import serializers
from rest_framework_hstore.serializers import HStoreSerializer


class ItemSerializer(HStoreSerializer):
    class Meta:
        model = Item
        fields = ('uuid', 'name', 'description', 'props', 'state', 'parent')
