# Generated by Django 3.1.3 on 2021-06-14 02:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_file_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='status',
            field=models.CharField(default='PASS', max_length=50),
        ),
        migrations.AlterField(
            model_name='file',
            name='name',
            field=models.CharField(default='Untitled 06/14/21', max_length=100),
        ),
    ]
