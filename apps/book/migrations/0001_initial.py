# Generated by Django 4.0.5 on 2022-06-18 01:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('storage', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('name', models.CharField(max_length=12, null=True, verbose_name='게시물 제목')),
                ('data', models.DateTimeField(verbose_name='날짜')),
                ('locate', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'db_table': 'boards',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('content', models.CharField(max_length=55)),
                ('parents', models.IntegerField(null=True, verbose_name='부모 댓글 id')),
                ('board', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.board', verbose_name='내용')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='유저')),
            ],
            options={
                'db_table': 'comments',
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('name', models.CharField(max_length=25, verbose_name='그룹 이름')),
                ('description', models.CharField(max_length=125, null=True, verbose_name='그룹 설명')),
                ('user', models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='멤버')),
            ],
            options={
                'db_table': 'books',
            },
        ),
        migrations.AddField(
            model_name='board',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.book', verbose_name='책'),
        ),
        migrations.AddField(
            model_name='board',
            name='image',
            field=models.ManyToManyField(db_table='board_image', max_length=255, to='storage.image', verbose_name='게시물 사진'),
        ),
    ]
