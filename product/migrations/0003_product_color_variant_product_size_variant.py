# Generated by Django 5.1 on 2024-08-30 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_colorvariant_sizevarient'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='color_variant',
            field=models.ManyToManyField(to='product.colorvariant'),
        ),
        migrations.AddField(
            model_name='product',
            name='size_variant',
            field=models.ManyToManyField(to='product.sizevarient'),
        ),
    ]
