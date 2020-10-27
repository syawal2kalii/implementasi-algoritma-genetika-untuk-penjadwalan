from django.shortcuts import render
from penjadwalan.algoritma_genetika.classes import *
from penjadwalan.algoritma_genetika.tes import Tes
from .models import Dosen
from penjadwalan.algoritma_genetika.algen import (
    algo,
    print_chromosome,
    print_hasil,
    setNullHasil,
)
import random
from penjadwalan.algoritma_genetika.classes import Group

# Create your views here.
def generate(request):
    random.seed()
    algo()
    hasil = print_hasil()
    setNullHasil()
    dosen = Dosen.objects.all()
    nm_dosen = []
    for a in dosen:
        # print(a.nama_dosen)
        nm_dosen.append(a.nama_dosen)
    print("nm_dosen :", nm_dosen)
    print("dosen =", dosen)

    # print(result)
    # convert_input_to_bin()
    # context = {"cpg": convert_input_to_bin}
    return render(request, "generate.html", {"hasil": hasil, "dosen": nm_dosen})


def tes(request):
    Professor.professors
    for dosen in Dosen.objects.all():
        Professor.professors.append(Professor(dosen.nama_dosen))

    print(Professor.professors[2])
    # context = {"nm_dosen": nm_dosen}
    return render(request, "tes.html")
