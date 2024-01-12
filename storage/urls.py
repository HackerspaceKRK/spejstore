from django.urls import re_path, include
from storage.views import (
    index,
    search,
    item_display,
    label_lookup,
    apitoken,
    ItemSelectView,
    PropSelectView,
)

urlpatterns = [
    re_path(r"^$", index),
    re_path(r"^search$", search),
    re_path(r"^apitoken$", apitoken),
    re_path(r"^item/(?P<pk>.*)$", item_display, name="item-display"),
    re_path(r"^autocomplete.json$", ItemSelectView.as_view(), name="item-complete"),
    re_path(
        r"^autocomplete_prop.json$", PropSelectView.as_view(), name="prop-complete"
    ),
    re_path(r"^(?P<pk>[^/]*)$", label_lookup, name="label-lookup"),
    re_path("", include("social_django.urls", namespace="social")),
]
