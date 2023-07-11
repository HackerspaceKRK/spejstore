from pkg_resources import parse_version

from django_select2.forms import ModelSelect2Widget, HeavySelect2Widget
from django_hstore.forms import DictionaryFieldWidget

from django import get_version
from django.urls import reverse
from django.conf import settings
from django.utils.safestring import mark_safe
from django.template import Context
from django.template.loader import get_template
from django.contrib.admin.widgets import AdminTextareaWidget


class ItemSelectWidget(ModelSelect2Widget):
    def __init__(self, *args, **kwargs):
        kwargs["data_view"] = "item-complete"
        super(ItemSelectWidget, self).__init__(*args, **kwargs)

    def label_from_instance(self, obj):
        return obj.name


class PropsSelectWidget(DictionaryFieldWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        if attrs is None:
            attrs = {}
        # it's called "original" because it will be replaced by a copy
        attrs["class"] = "hstore-original-textarea"
        w = HeavySelect2Widget(
            data_view="prop-complete", attrs={"data-tags": "true", "class": "hs-key"}
        )

        # get default HTML from AdminTextareaWidget
        html = AdminTextareaWidget.render(self, name, value, attrs)
        # prepare template context
        template_context = {
            "field_name": name,
            "STATIC_URL": settings.STATIC_URL,
            "use_svg": parse_version(get_version())
            >= parse_version("1.9"),  # use svg icons if django >= 1.9
            "ajax_url": reverse("prop-complete"),
            "w": w.build_attrs(base_attrs=w.attrs),
        }
        # get template object
        template = get_template("hstore_%s_widget.html" % self.admin_style)
        # render additional html
        additional_html = template.render(template_context)

        # append additional HTML and mark as safe
        html = html + additional_html
        html = mark_safe(html)

        return html
