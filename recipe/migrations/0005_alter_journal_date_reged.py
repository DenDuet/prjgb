# Generated by Django 5.0.4 on 2024-05-04 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0004_alter_category_description_alter_recipe_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journal',
            name='date_reged',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
