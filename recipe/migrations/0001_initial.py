# Generated by Django 4.2.5 on 2023-10-25 15:12

from django.db import migrations, models
import django.db.models.deletion
import pathlib


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=50, unique=True)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('description', models.TextField()),
                ('steps', models.TextField()),
                ('add_date', models.DateTimeField(auto_now_add=True)),
                ('image', models.ImageField(upload_to=pathlib.PureWindowsPath('D:/Final/project/myproject/media'))),
                ('author', models.CharField(max_length=150)),
                ('ingredients', models.TextField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Journal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_reged', models.DateTimeField()),
                ('category', models.ManyToManyField(to='recipe.category')),
                ('recipe_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipe.recipe')),
            ],
        ),
    ]
