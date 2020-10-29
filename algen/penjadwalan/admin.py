from django.contrib import admin

from .models import (
    Asisten,
    Dosen,
    Group,
    Mata_kuliah,
    Ruangan,
    Waktu,
    DosenByMatkul,
    AsistenByMatkul,
    GroupByMatkul,
)

# Register your models here.
admin.site.register(Asisten)
admin.site.register(Dosen)
admin.site.register(Waktu)
admin.site.register(GroupByMatkul)
admin.site.register(Ruangan)
admin.site.register(Mata_kuliah)
admin.site.register(DosenByMatkul)
admin.site.register(Group)
admin.site.register(AsistenByMatkul)