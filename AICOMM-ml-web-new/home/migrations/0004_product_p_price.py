# Generated by Django 5.0 on 2024-01-03 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_product_p_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='p_price',
            field=models.FloatField(null=True),
        ),
    ]
