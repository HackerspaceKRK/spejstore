# Generated by Django 3.2.20 on 2023-07-11 19:35

from django.db import migrations
import tree.fields
from tree.operations import (
    RebuildPaths,
)


class Migration(migrations.Migration):
    dependencies = [
        ("storage", "0009_migrate_tree_fields"),
    ]

    operations = [
        migrations.AlterField(
            model_name="item",
            name="path",
            field=tree.fields.PathField(),
        ),
        RebuildPaths("item"),
    ]
