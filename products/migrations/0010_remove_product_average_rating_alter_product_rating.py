# Generated by Django 5.1.4 on 2025-02-09 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_alter_review_unique_together_product_average_rating_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='average_rating',
        ),
        migrations.AlterField(
            model_name='product',
            name='rating',
            field=models.FloatField(default=0),
        ),
    ]
