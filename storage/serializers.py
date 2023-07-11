from django.contrib.auth.models import User
from storage.models import Item, Label, Category
from rest_framework import serializers
from rest_framework_hstore.serializers import HStoreSerializer


class ItemSerializer(HStoreSerializer):
    categories = serializers.SlugRelatedField(
        queryset=Category.objects, many=True, slug_field="name"
    )
    owner = serializers.SlugRelatedField(queryset=User.objects, slug_field="username")
    taken_by = serializers.SlugRelatedField(
        queryset=User.objects, slug_field="username"
    )

    class Meta:
        model = Item
        fields = (
            "uuid",
            "short_id",
            "name",
            "description",
            "props",
            "state",
            "parent",
            "labels",
            "owner",
            "taken_by",
            "taken_on",
            "taken_until",
            "categories",
        )


class LabelSerializer(serializers.ModelSerializer):
    item = ItemSerializer(required=False)
    item_id = serializers.PrimaryKeyRelatedField(queryset=Item.objects, source="item")

    class Meta:
        model = Label
        fields = ("id", "item", "item_id", "style")
