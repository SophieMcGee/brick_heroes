# Generated by Django 5.1.4 on 2025-02-09 11:54

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='is_read',
        ),
        migrations.AddField(
            model_name='notification',
            name='category',
            field=models.CharField(choices=[('subscription', 'Subscription'), ('borrowing', 'Borrowing'), ('review', 'Review')], default='subscription', max_length=20),
        ),
        migrations.AlterField(
            model_name='notification',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
