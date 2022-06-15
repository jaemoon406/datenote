# Generated by Django 4.0.5 on 2022-06-15 20:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_alter_user_last_login'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='last_login',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 15, 20, 43, 17, 799737), verbose_name='date last work'),
        ),
        migrations.AlterField(
            model_name='user',
            name='profile_image',
            field=models.ImageField(blank=True, max_length=1000, null=True, upload_to='', verbose_name='profile_image'),
        ),
    ]
