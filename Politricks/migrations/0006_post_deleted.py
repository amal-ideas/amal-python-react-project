# Generated by Django 3.1 on 2020-09-13 23:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Politricks', '0005_auto_20200910_1044'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='deleted',
            field=models.BooleanField(default=0),
        ),
    ]
