# Generated by Django 5.0.4 on 2024-05-13 13:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0019_remove_purchasehistory_item_clothing_id'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['p_category', 'p_name']},
        ),
    ]