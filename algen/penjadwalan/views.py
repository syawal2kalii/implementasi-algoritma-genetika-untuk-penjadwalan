from django.shortcuts import render
from penjadwalan.algoritma_genetika.classes import *
from penjadwalan.algoritma_genetika.tes import Tes
from penjadwalan.algoritma_genetika.algen import (
    algo,
    print_chromosome,
    print_hasil,
    setNullHasil,
)
import random

# Create your views here.
def generate(request):
    random.seed()
    algo()
    hasil = print_hasil()
    setNullHasil()
    # print(result)
    # convert_input_to_bin()
    # context = {"cpg": convert_input_to_bin}
    return render(request, "generate.html", {"hasil": hasil})
