# Generated by Django 3.1.7 on 2021-03-04 04:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_auto_20210304_0912'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='name',
            field=models.CharField(default='User', max_length=250, verbose_name='Имя'),
        ),
    ]
