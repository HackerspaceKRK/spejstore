from django.conf.urls import include, url
from storage.views import index, search, item_display, label_lookup, ItemSelectView

urlpatterns = [
    url(r'^$', index),
    url(r'^search$', search),
    url(r'^item/(?P<pk>.*)$', item_display, name='item-display'),
    url(r'^autocomplete.json$', ItemSelectView.as_view(), name='item-complete'),
    url(r'^(?P<pk>[^/]*)$', label_lookup, name='label-lookup'),
]
