# Generated by Django 3.1.1 on 2020-09-26 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('penjadwalan', '0002_asisten'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asisten',
            name='nama_asisten',
            field=models.CharField(max_length=100),
        ),
    ]
