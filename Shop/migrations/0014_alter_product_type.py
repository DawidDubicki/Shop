# Generated by Django 4.1 on 2022-08-29 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Shop', '0013_alter_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='type',
            field=models.CharField(choices=[('Komputer', 'Komputer'), ('Biurko', 'Biurko'), ('Klawiatura', 'Klawiatura'), ('Myszka', 'Myszka')], max_length=100),
        ),
    ]
