from django.conf.urls import include, url
from storage.views import (
    index, search, item_display, label_lookup, apitoken, ItemSelectView,
    PropSelectView
)

urlpatterns = [
    url(r'^$', index),
    url(r'^search$', search),
    url(r'^apitoken$', apitoken),
    url(r'^item/(?P<pk>.*)$', item_display, name='item-display'),
    url(r'^autocomplete.json$', ItemSelectView.as_view(), name='item-complete'),
    url(r'^autocomplete_prop.json$', PropSelectView.as_view(), name='prop-complete'),
    url(r'^(?P<pk>[^/]*)$', label_lookup, name='label-lookup'),
    url('', include('social_django.urls', namespace='social')),
]
