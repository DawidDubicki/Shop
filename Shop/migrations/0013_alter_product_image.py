# Generated by Django 4.1 on 2022-08-22 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Shop', '0012_alter_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(upload_to='images/'),
        ),
    ]
