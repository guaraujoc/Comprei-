# Generated by Django 5.1.4 on 2024-12-18 02:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Loja', '0007_ingredient_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]