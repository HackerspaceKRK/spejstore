# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from tree.operations import CreateTreeTrigger, DeleteTreeTrigger, RebuildPaths


class Migration(migrations.Migration):
    dependencies = [
        ("storage", "0004_auto_20170528_1945"),
    ]

    operations = [
        DeleteTreeTrigger("storage.Item"),
        CreateTreeTrigger("storage.Item"),
        RebuildPaths("storage.Item"),
    ]
