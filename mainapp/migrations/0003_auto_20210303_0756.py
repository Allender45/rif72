# Generated by Django 3.1.7 on 2021-03-03 02:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_auto_20210301_1423'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartproduct',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='cartproduct',
            name='object_id',
        ),
        migrations.AddField(
            model_name='cartproduct',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='mainapp.product', verbose_name='Товар в корзине'),
        ),
    ]