from __future__ import unicode_literals
import os

import uuid
import re

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from tree.fields import PathField
from tree.models import TreeModelMixin
from django.contrib.postgres.fields import HStoreField
from django.contrib.auth.models import UserManager


import requests


STATES = (
    ("present", "Present"),
    ("taken", "Taken"),
    ("broken", "Broken"),
    ("missing", "Missing"),
    ("depleted", "Depleted"),
)


def api_print(item):
    resp = requests.post(
        "{}/api/2/print".format(settings.LABEL_API),
        params={
            "id": item.short_id,
            "name": item.name,
            "owner": item.owner,
        }
    )
    resp.raise_for_status()


class Category(models.Model):
    name = models.CharField(max_length=127)

    icon_id = models.CharField(max_length=64, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "categories"


# TODO label versioning
# Zapisywać w URL na naklejce jej wersję, aby można było łatwo wyłapać
# przedawnione informacje
# Also przechowywać "id" z qrkodów/barkodów w historycznej bazie.
# also qrcody w stylu //s/ID (żeby się resolvowało w sieci lokalnej)
# Also ID zawierające część name


class StaffManager(UserManager):
    pass


class StaffProxyModel(User):
    objects = StaffManager()

    class Meta:
        proxy = True
        verbose_name = "User"
        verbose_name_plural = "Users"


class Item(models.Model, TreeModelMixin):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)
    path = PathField()

    name = models.TextField()

    wiki_link = models.TextField(null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    state = models.CharField(max_length=31, choices=STATES, default=STATES[0][0])
    categories = models.ManyToManyField(Category, blank=True)
    owner = models.ForeignKey(
        StaffProxyModel,
        null=True,
        blank=True,
        related_name="owned_items",
        on_delete=models.CASCADE,
    )

    taken_by = models.ForeignKey(
        StaffProxyModel,
        null=True,
        blank=True,
        related_name="taken_items",
        on_delete=models.CASCADE,
    )
    taken_on = models.DateTimeField(blank=True, null=True)
    taken_until = models.DateTimeField(blank=True, null=True)

    props = HStoreField(blank=True)

    def short_id(self):
        # let's just hope we never have 4 294 967 296 things :)
        return str(self.pk)[:8]  # collisions? what collisions?

    def __str__(self):
        return "- " * (self.get_level() or 0) + self.name

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("item-display", kwargs={"pk": str(self.pk)})

    def get_or_create_label(self, **kwargs):
        defaults = {
            "id": re.sub("[^A-Z0-9]", "", self.name.upper())[:16],
        }

        defaults.update(kwargs)

        obj, created = self.labels.get_or_create(**kwargs, defaults=defaults)

        return obj

    @property
    def primary_category(self):
        return next((c for c in self.categories.all() if c.icon_id), None)

    def print(self):
        api_print(self)

    class Meta:
        ordering = ("path",)


class ImageFieldWithUuid(models.ImageField):
    def generate_filename(self, instance, filename):
        ext = filename.split(".")[-1]
        filename = "%s.%s" % (uuid.uuid4(), ext)
        return super().generate_filename(instance, filename)


class ItemImage(models.Model):
    item = models.ForeignKey(Item, related_name="images", on_delete=models.CASCADE)
    image = ImageFieldWithUuid()

    def __str__(self):
        return "{}".format(self.image.name)


# Deprecated, left in db due to legacy reasons
class Label(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    item = models.ForeignKey(Item, related_name="labels", on_delete=models.CASCADE)
    style = models.CharField(
        max_length=32,
        choices=(("basic_99012_v1", "Basic Dymo 89x36mm label"),),
        default="basic_99012_v1",
    )
    created = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return "{}".format(self.id)
