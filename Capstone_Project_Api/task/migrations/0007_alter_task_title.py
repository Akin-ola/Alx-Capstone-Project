# Generated by Django 5.1.7 on 2025-04-04 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0006_alter_maintenance_technician'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='title',
            field=models.CharField(choices=[('Periodic maintenance', 'Periodic maintenance'), ('Preventive maintenance', 'Preventive maintenance'), ('Category A maintenance', 'Category A maintenance'), ('Category B maintenance', 'Category B maintenance'), ('Category C maintenance', 'Category C maintenance'), ('Category D maintenance', 'Category D maintenance')], max_length=200),
        ),
    ]
