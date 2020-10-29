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
import penjadwalan.models as db


def inisialisasi():
    Group.groups = []
    for group in db.Group.objects.all():
        Group.groups.append(
            Group(group.nama_group, int(group.semester), int(group.size))
        )

    # tambah Mata Kuliah yang di ajar
    Professor.professors = []

    for dosen in db.Dosen.objects.all():
        Professor.professors.append(Professor(dosen.nama_dosen))

    CourseClass.classes = []
    for course in db.Mata_kuliah.objects.all():
        CourseClass.classes.append(CourseClass(course.nama_matkul))

    Room.rooms = []
    for room in db.Ruangan.objects.all():
        Room.rooms.append(Room(room.nama_ruangan, int(room.kapasitas)))
        # Room.rooms = [Room("lab rpl", 30), Room("lab jarkom", 30)]

    Slot.slots = []
    for slot in db.Waktu.objects.all():
        Slot.slots.append(Slot(slot.mulai, slot.berakhir, slot.hari))


def deinisialisasi():
    Group.groups = []
    Professor.professors = []
    CourseClass.classes = []
    Room.rooms = []
    Slot.slots = []


# Create your views here.
def generate(request):
    random.seed()
    setNullHasil()
    inisialisasi()
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
    deinisialisasi()

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
