# Generated by Django 5.1.4 on 2025-02-07 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0006_subscriptionplan_stripe_price_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='stripe_customer_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
