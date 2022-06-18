# Generated by Django 4.0.5 on 2022-06-18 17:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('book', '0002_remove_board_image_board_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='description',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='is_public',
            field=models.BooleanField(default=0),
        ),
        migrations.AddField(
            model_name='book',
            name='password',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='board',
            name='data',
            field=models.DateTimeField(verbose_name='추억 날짜'),
        ),
        migrations.AlterField(
            model_name='board',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='게시물 등록 멤버'),
        ),
    ]
