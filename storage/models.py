from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django_hstore import hstore
import uuid

from tree.fields import PathField
from tree.models import TreeModelMixin


STATES = (
    ('present', 'Present'),
    ('taken', 'Taken'),
    ('broken', 'Broken'),
    ('missing', 'Missing'),
)


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=127)

    def __str__(self):
        return self.name


class Item(models.Model, TreeModelMixin):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    parent = models.ForeignKey('self', null=True, blank=True)
    path = PathField()

    name = models.TextField()

    description = models.TextField(blank=True, null=True)
    state = models.CharField(max_length=31, choices=STATES, default=STATES[0][0])
    categories = models.ManyToManyField(Category, blank=True)
    owner = models.ForeignKey(User, null=True, blank=True, related_name='owned_items')

    taken_by = models.ForeignKey(User, null=True, blank=True, related_name='taken_items')
    taken_on = models.DateTimeField(blank=True, null=True)
    taken_until = models.DateTimeField(blank=True, null=True)

    props = hstore.DictionaryField(blank=True)

    objects = hstore.HStoreManager()

    def __str__(self):
        return '- ' * (self.get_level() or 0) + self.name

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('item-display', kwargs={'pk': str(self.pk)})

    class Meta:
        ordering = ('path',)


class ItemImage(models.Model):
    item = models.ForeignKey(Item, related_name='images')
    image = models.ImageField()
