# Generated by Django 4.2.2 on 2023-07-08 09:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0009_alter_order_total'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='total',
        ),
    ]
