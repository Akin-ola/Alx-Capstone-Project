# Generated by Django 5.1.7 on 2025-04-03 23:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0005_alter_maintenance_technician'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maintenance',
            name='technician',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task_record', to=settings.AUTH_USER_MODEL),
        ),
    ]
