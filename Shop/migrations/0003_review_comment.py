# Generated by Django 4.1 on 2022-08-11 23:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Shop', '0002_product_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='comment',
            field=models.TextField(default='x'),
            preserve_default=False,
        ),
    ]
