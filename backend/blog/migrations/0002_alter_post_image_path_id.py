# Generated by Django 5.0 on 2023-12-26 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image_path_id',
            field=models.IntegerField(unique=True),
        ),
    ]
