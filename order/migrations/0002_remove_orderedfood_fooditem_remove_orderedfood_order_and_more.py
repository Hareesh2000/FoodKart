# Generated by Django 4.2.2 on 2023-07-07 06:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderedfood',
            name='fooditem',
        ),
        migrations.RemoveField(
            model_name='orderedfood',
            name='order',
        ),
        migrations.RemoveField(
            model_name='orderedfood',
            name='payment',
        ),
        migrations.RemoveField(
            model_name='orderedfood',
            name='user',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='user',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
        migrations.DeleteModel(
            name='OrderedFood',
        ),
        migrations.DeleteModel(
            name='Payment',
        ),
    ]
