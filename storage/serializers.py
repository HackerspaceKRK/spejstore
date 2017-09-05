from storage.models import Item, Label
from rest_framework import serializers
from rest_framework_hstore.serializers import HStoreSerializer


class ItemSerializer(HStoreSerializer):
    class Meta:
        model = Item
        fields = ('uuid', 'name', 'description', 'props', 'state', 'parent')

class LabelSerializer(serializers.ModelSerializer):
    item = ItemSerializer()
    item_id = serializers.PrimaryKeyRelatedField(queryset=Item.objects, source='item')
    class Meta:
        model = Label
        fields = ('id', 'item', 'item_id', 'style')
