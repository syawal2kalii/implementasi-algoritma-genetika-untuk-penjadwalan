from django.db import models

# Create your models here.

class Dosen(models.Model):
    nama_dosen = models.CharField(max_length=100)
    id_dosen = models.CharField(default='', max_length=100)
    no_hp = models.CharField(default='', max_length=100)

    def __str__(self):
        return self.nama_dosen

class Asisten(models.Model):
    nama_asisten = models.CharField(max_length=100, default='')
    no_hp = models.CharField(default='', max_length=100)
    nim = models.CharField(default='', max_length=100)

    def __str__(self):
        return self.nama_asisten
    


class Mata_praktikum(models.Model):
    nama_praktikum = models.CharField(default='', max_length=100)
    kode_praktikum = models.CharField(default='', max_length=100)

    def __str__(self):
        return self.nama_praktikum
    
class Hari(models.Model):
    nama_hari = models.CharField(default='', max_length=100)

    def __str__(self):
        return self.nama_hari
    

class Jam(models.Model):
    keterangan = models.CharField(default='', max_length=100)

    def __str__(self):
        return self.keterangan
    

class Ruangan(models.Model):
    nama_ruangan = models.CharField(default='', max_length=100)

    def __str__(self):
        return self.nama_ruangan
    