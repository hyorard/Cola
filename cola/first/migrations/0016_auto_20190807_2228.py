# Generated by Django 2.1.3 on 2019-08-07 13:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first', '0015_auto_20190805_1927'),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='File',
            field=models.FileField(null=True, upload_to='board/'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='created_date',
            field=models.DateField(default=datetime.date(2019, 8, 7)),
        ),
    ]