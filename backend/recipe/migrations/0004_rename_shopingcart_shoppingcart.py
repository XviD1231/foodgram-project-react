# Generated by Django 3.2 on 2023-08-15 17:13

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipe', '0003_shopingcart'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ShopingCart',
            new_name='ShoppingCart',
        ),
    ]
