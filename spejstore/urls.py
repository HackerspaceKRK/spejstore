"""spejstore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import routers

from storage import apiviews

from auth.views import auth_redirect


router = routers.DefaultRouter()
router.register(r'items', apiviews.ItemViewSet)
router.register(r'labels', apiviews.LabelViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^admin/login/.*', auth_redirect),
    url(r'^admin/', admin.site.urls),
    url(r'^select2/', include('django_select2.urls')),

    url(r'^', include('storage.urls')),
    url(r'^api/1/', include(router.urls)),
] \
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
