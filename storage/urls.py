from django.conf.urls import include, url
from storage.views import index, search, item_display, label_lookup

urlpatterns = [
    url(r'^$', index),
    url(r'^search$', search),
    url(r'^item/(?P<pk>.*)$', item_display, name='item-display'),
    url(r'^(?P<pk>[^/]*)$', label_lookup, name='label-lookup'),
]
