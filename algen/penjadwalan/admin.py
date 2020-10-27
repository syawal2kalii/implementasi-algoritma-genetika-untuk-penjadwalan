from django.contrib import admin

from .models import (
    Asisten,
    Dosen,
    Group,
    Mata_kuliah,
    Ruangan,
    Waktu,
    MengajarByDosen,
    MengajarByAsisten,
)

# Register your models here.
admin.site.register(Asisten)
admin.site.register(Dosen)
admin.site.register(Waktu)
admin.site.register(MengajarByAsisten)
admin.site.register(Ruangan)
admin.site.register(Mata_kuliah)
admin.site.register(MengajarByDosen)
admin.site.register(Group)