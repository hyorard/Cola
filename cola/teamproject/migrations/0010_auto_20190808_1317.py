# Generated by Django 2.1.3 on 2019-08-08 04:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teamproject', '0009_commenttb'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commenttb',
            name='created_date',
            field=models.DateField(default=datetime.date(2019, 8, 8)),
        ),
    ]