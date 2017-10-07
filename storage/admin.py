from django import forms
from django.contrib import admin
from .models import Item, ItemImage, Category, Label
from django_select2.forms import Select2Widget, Select2MultipleWidget


class ItemForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput())

    class Meta:
        model = Item
        exclude = []
        widgets = {
            'parent': Select2Widget,
            'categories': Select2MultipleWidget
            }

class ItemImageInline(admin.TabularInline):
    model = ItemImage
    extra = 1

class LabelInline(admin.TabularInline):
    model = Label

class ItemAdmin(admin.ModelAdmin):
    list_display = ('_name',)
    list_filter = ('categories',)
    form = ItemForm
    inlines = [ItemImageInline, LabelInline]
    save_on_top = True

    def _name(self, obj):
        return '-' * obj.get_level() + '> ' + obj.name

    def save_model(self, request, obj, form, change):
        super(ItemAdmin, self).save_model(request, obj, form, change)

        # Store last input parent to use as default on next creation
        if obj.parent:
            request.session['last-parent'] = str(obj.parent.uuid)
        else:
            request.session['last-parent'] = str(obj.uuid)

    def get_changeform_initial_data(self, request):
        data = {
            'parent': request.GET.get('parent') or request.session.get('last-parent')
            }

        data.update(super(ItemAdmin, self).get_changeform_initial_data(request))
        return data

    class Media:
        js = (
            # Required by select2
            'https://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            )

    def response_action(self, request, queryset):
        with Item.disabled_tree_trigger():
            return super(ItemAdmin, self).response_action(request, queryset)

admin.site.register(Item, ItemAdmin)
admin.site.register(Category)
