# Generated by Django 3.1.3 on 2021-06-14 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0005_auto_20210614_0254'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='not_found',
            field=models.IntegerField(default=0),
        ),
    ]
