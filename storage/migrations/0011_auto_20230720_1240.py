# Generated by Django 3.2.20 on 2023-07-20 12:40

from django.db import migrations, models
import django.db.models.deletion
import storage.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('storage', '0010_alter_item_path'),
    ]

    operations = [
        migrations.CreateModel(
            name='StaffProxyModel',
            fields=[
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('auth.user',),
            managers=[
                ('objects', storage.models.StaffManager()),
            ],
        ),
        migrations.AlterField(
            model_name='item',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='owned_items', to='storage.staffproxymodel'),
        ),
        migrations.AlterField(
            model_name='item',
            name='taken_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='taken_items', to='storage.staffproxymodel'),
        ),
    ]
