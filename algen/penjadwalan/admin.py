from django.contrib import admin
from .models import Asisten, Dosen, Hari, Jam, Ruangan, Mata_praktikum

# Register your models here.
admin.site.register(Asisten)
admin.site.register(Dosen)
admin.site.register(Hari)
admin.site.register(Jam)
admin.site.register(Ruangan)
admin.site.register(Mata_praktikum)