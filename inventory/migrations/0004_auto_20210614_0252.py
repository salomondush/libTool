# Generated by Django 3.1.3 on 2021-06-14 02:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_auto_20210614_0251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='name',
            field=models.CharField(default='Untitled-06/14/21', max_length=100),
        ),
    ]
