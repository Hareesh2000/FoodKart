# Generated by Django 4.2.2 on 2023-07-07 09:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='country',
        ),
        migrations.RemoveField(
            model_name='order',
            name='payment_method',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='payment_method',
        ),
    ]
