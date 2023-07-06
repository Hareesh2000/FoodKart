# Generated by Django 4.2.2 on 2023-07-06 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0006_alter_openinghour_unique_together'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='openinghour',
            options={'ordering': ('day', '-from_hour')},
        ),
        migrations.AlterField(
            model_name='openinghour',
            name='day',
            field=models.IntegerField(choices=[(1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'), (4, 'Thursday'), (5, 'Friday'), (6, 'Saturday'), (7, 'Sunday')]),
        ),
    ]
