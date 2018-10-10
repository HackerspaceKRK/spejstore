from django import forms
from django.contrib import admin

from django_select2.forms import ModelSelect2Widget, Select2MultipleWidget


from .models import Item, ItemImage, Category, Label
from .widgets import ItemSelectWidget, PropsSelectWidget


class ItemForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput())

    class Meta:
        model = Item
        exclude = []
        widgets = {
            'parent': ItemSelectWidget(model=Item),
            'categories': Select2MultipleWidget,
            'props': PropsSelectWidget
            }


class ItemImageInline(admin.TabularInline):
    model = ItemImage
    extra = 1


class LabelInline(admin.TabularInline):
    model = Label


class StaffModelAdmin(admin.ModelAdmin):

    def has_add_permission(self, request, obj=None):
        return request.user.is_staff or request.user.is_superuser

    has_change_permission = has_add_permission
    has_delete_permission = has_add_permission
    has_module_permission = has_add_permission


class ItemAdmin(StaffModelAdmin):
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
        css = {
            'all': ('css/admin.css',)
            }

    def response_action(self, request, queryset):
        with Item.disabled_tree_trigger():
            return super(ItemAdmin, self).response_action(request, queryset)


admin.site.register(Item, ItemAdmin)
admin.site.register(Category, StaffModelAdmin)

from django.contrib.auth.models import User
from django.contrib.auth.models import Group

User.add_to_class('get_short_name', User.get_username)
User.add_to_class('get_full_name', User.get_username)

admin.site.unregister(User)
admin.site.unregister(Group)

from social_django.admin import UserSocialAuth, Nonce, Association
admin.site.unregister(UserSocialAuth)
admin.site.unregister(Nonce)
admin.site.unregister(Association)
