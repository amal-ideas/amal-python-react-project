# Generated by Django 3.1 on 2020-09-25 00:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Politricks', '0008_auto_20200925_1155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='picture',
            field=models.ImageField(blank=True, default='default.jpg', upload_to='post_photos'),
        ),
    ]
