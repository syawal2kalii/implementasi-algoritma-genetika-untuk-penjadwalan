# Generated by Django 3.1.1 on 2020-09-26 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('penjadwalan', '0005_auto_20200926_1327'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mata_praktikum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama_praktikum', models.CharField(default='', max_length=50)),
                ('kode_praktikum', models.CharField(default='', max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='asisten',
            name='nim',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='asisten',
            name='no_hp',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='dosen',
            name='id_dosen',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='dosen',
            name='no_hp',
            field=models.CharField(default='', max_length=50),
        ),
    ]
