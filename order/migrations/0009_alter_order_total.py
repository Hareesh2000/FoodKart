# Generated by Django 4.2.2 on 2023-07-08 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0008_order_total'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='total',
            field=models.FloatField(),
        ),
    ]