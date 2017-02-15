from django import forms
from django.contrib import admin
from .models import Item, ItemImage, Category

class ItemForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput())

    class Meta:
        model = Item
        exclude = []

class ItemImageInline(admin.TabularInline):
    model = ItemImage
    extra = 1

class ItemAdmin(admin.ModelAdmin):
    list_display = ('_name', 'uuid', 'props', 'path')
    list_filter = ('categories',)
    form = ItemForm
    inlines = [ItemImageInline]

    def _name(self, obj):
        return '-' * obj.get_level() + '> ' + obj.name


admin.site.register(Item, ItemAdmin)
admin.site.register(Category)
