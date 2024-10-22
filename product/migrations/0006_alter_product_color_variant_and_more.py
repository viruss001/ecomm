# Generated by Django 5.1 on 2024-08-31 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_coupon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='color_variant',
            field=models.ManyToManyField(to='product.colorvariant'),
        ),
        migrations.AlterField(
            model_name='product',
            name='size_variant',
            field=models.ManyToManyField(to='product.sizevarient'),
        ),
    ]
