# Generated by Django 3.1.7 on 2021-03-01 09:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartproduct',
            name='product',
        ),
        migrations.AddField(
            model_name='cartproduct',
            name='content_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='contenttypes.contenttype'),
        ),
        migrations.AddField(
            model_name='cartproduct',
            name='object_id',
            field=models.PositiveIntegerField(null=True),
        ),
    ]