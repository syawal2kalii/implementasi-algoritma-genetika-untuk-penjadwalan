# Generated by Django 3.1.1 on 2020-09-26 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('penjadwalan', '0006_auto_20200926_1353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asisten',
            name='nim',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='asisten',
            name='no_hp',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='dosen',
            name='id_dosen',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='dosen',
            name='nama_dosen',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='dosen',
            name='no_hp',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='mata_praktikum',
            name='kode_praktikum',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='mata_praktikum',
            name='nama_praktikum',
            field=models.CharField(default='', max_length=100),
        ),
    ]
