# Generated by Django 3.1.7 on 2021-03-11 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0012_cart_finished'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата создания'),
        ),
    ]
