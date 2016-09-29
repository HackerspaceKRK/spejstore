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
    list_display = ('name', 'uuid', 'props')
    list_filter = ('categories',)
    form = ItemForm
    inlines = [ItemImageInline]


admin.site.register(Item, ItemAdmin)
admin.site.register(Category)
