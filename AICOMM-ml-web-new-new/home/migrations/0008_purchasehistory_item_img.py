# Generated by Django 5.0 on 2024-02-28 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_purchasehistory_item_cat'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchasehistory',
            name='item_img',
            field=models.ImageField(default=0, upload_to=''),
            preserve_default=False,
        ),
    ]