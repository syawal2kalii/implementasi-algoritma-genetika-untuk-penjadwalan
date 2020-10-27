import random, copy
from math import ceil, log2

from penjadwalan.algoritma_genetika.classes import *
import penjadwalan.models as db


def inisialisasi():
    # tambah angkatan
    # Group.groups = [
    #     Group("a12018", 30),
    #     Group("b12018", 30),
    #     Group("a12019", 30),
    #     Group("b12019", 30),
    #     Group("a12020", 30),
    #     Group("b12020", 30),
    #     Group("a12021", 30),
    #     Group("b12021", 30),
    # ]
    Group.groups = []
    for group in db.Group.objects.all():
        Group.groups.append(Group(group.nama_group, int(group.size)))

    # tambah Mata Kuliah yang di ajar
    Professor.professors = []
    # Professor.professors = [
    #     Professor("Muhammad Arfah Asis, S.Kom.,M.T"),
    #     Professor("Ramdaniah, S.Kom.,M.T"),
    #     # Professor("Erick Irawadi Alwi, S.Kom.,M.Eng"),
    #     # Professor("Lutfi Budi Ilmawan, S.Kom.,M.Cs"),
    #     # Professor("Amaliah Faradibah S.Kom.,M.Kom"),
    # ]

    for dosen in db.Dosen.objects.all():
        Professor.professors.append(Professor(dosen.nama_dosen))

    # tambah untuk angkatan berapa
    # CourseClass.classes = [
    #     CourseClass("ap"),
    #     CourseClass("bd"),
    #     CourseClass("jarkom"),
    #     CourseClass("web"),
    #     CourseClass("sti"),
    #     CourseClass("str"),
    # ]

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
    # Slot.slots = [
    #     Slot("08:00", "09:40", "jumat"),
    #     Slot("09:40", "11:20", "jumat"),
    #     Slot("13:00", "14:40", "jumat"),
    #     Slot("14:40", "16:20", "jumat"),
    #     Slot("16:20", "18:00", "jumat"),
    # ]


max_score = None
result = None
cpg = []
lts = []
slots = []
bits_needed_backup_store = {}  # to improve performance
lec = None


def bits_needed(x):
    global bits_needed_backup_store
    r = bits_needed_backup_store.get(id(x))
    if r is None:
        r = int(ceil(log2(len(x))))
        bits_needed_backup_store[id(x)] = r
    return max(r, 1)


def join_cpg_pair(_cpg):
    res = []
    for i in range(0, len(_cpg), 3):
        res.append(_cpg[i] + _cpg[i + 1] + _cpg[i + 2])
    return res


def convert_input_to_bin():

    # [“ap”,”bd”,”jarkom”,”web”,”sti”,”str”] ->
    # [“1”,”2”,”3”,”4”,”5”,”6”] ->
    # [‘001’,’010’,’011’,’100’,’101’,’110’]

    ## gabung
    # [courseclass[i],professor[i],group[i]] - > [courseclass[0],professor[0],group[0]]
    # 					                                  [courseclass[1],professor[1],group[1]]
    # 					                                  [courseclass[2],professor[2],group[2]]
    # 					                                  [courseclass[n],professor[n],group[n]]
    #
    #

    # cpg->input->findid : [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 0, 5
    # cpg->binary : ['000', '000', '000', '001', '001', '001', '010', '010', '010', '011', '011', '011', '100', '100', '100', '101', '000', '101']
    # cpg gabung->binary [] [courseclass[i],professor[i],group[i]] : ['000000000', '001001001', '010010010', '011011011', '100100100', '101000101']

    # lts convert ['000', '001', '010', '011', '100', '101', '110']
    # slots : ['00000', '00001', '00010', '00011', '00100', '00101', '00110', '00111', '01000', '01001', '01010', '01011', '01100', '01101', '01110', '01111', '10000', '10001', '10010', '10011', '10100', '10101', '10110', '10111', '11000']

    # chromosone = cpg + lts + slots
    # cpg : ['000000000', '001001001', '010010010', '011011011', '100100100', '101000101']
    # lts : ['000', '001', '010', '011', '100', '101', '110']
    # slots : ['00000', '00001', '00010', '00011', '00100', '00101', '00110', '00111', '01000', '01001', '01010', '01011', '01100', '01101', '01110', '01111', '10000', '10001', '10010', '10011', '10100', '10101', '10110', '10111', '11000']

    # chromosomes : [
    #  ['00000000000111010', '00100100101010000', '01001001000001110', '01101101101001010', '10010010010100011', '10100010110011001'], # Populasi 1
    #   ['00000000010101000', '00100100101110000', '01001001000001011', '01101101110110000', '10010010001100001', '10100010101010110'], # Populasi 2
    #   ['00000000010110101', '00100100100001100', '01001001001111010', '01101101101110001', '10010010010100110', '10100010111000010']] # Populasi 3

    # slots convert ['00000', '00001', '00010', '00011', '00100', '00101', '00110', '00111', '01000', '01001', '01010', '01011', '01100', '01101', '01110', '01111', '10000', '10001', '10010', '10011', '10100', '10101', '10110', '10111', '11000']
    #####init Population (3)
    # cpg : ['000000000', '001001001', '010010010', '011011011', '100100100', '101000101']
    # lts : ['000', '001', '010', '011', '100', '101', '110']
    # slots : ['00000', '00001', '00010', '00011', '00100', '00101', '00110', '00111', '01000', '01001', '01010', '01011', '01100', '01101', '01110', '01111', '10000', '10001', '10010', '10011', '10100', '10101', '10110', '10111', '11000']

    print("#####convert input to bin")
    global cpg, lts, slots, max_score

    # mendapatkan gen terbanyak
    max1 = int(
        max(len(CourseClass.classes), len(Professor.professors), len(Group.groups))
    )

    # jika gen prof tidak sama panjang dengan gen terpanjang tambahkan gen[1] -> untuk memastikan semua gen ada dalam populasi
    if len(Professor.professors) != max1:
        selisih = max1 - int(len(Professor.professors))
        for i in range(selisih):
            Professor.professors.append(Professor.professors[0])

    if len(CourseClass.classes) != max1:
        selisih = max1 - len(CourseClass.classes)
        for i in range(selisih):
            CourseClass.classes.append(CourseClass.classes[0])

    if len(Group.groups) != max1:
        selisih = max1 - len(Group.groups)
        for i in range(selisih):
            Group.groups.append(Group.groups[0])

    #
    cpg = []

    for i in range(
        max(len(CourseClass.classes), len(Professor.professors), len(Group.groups))
    ):
        cpg.extend(
            [
                CourseClass.find(CourseClass.classes[i].code),
                Professor.find(Professor.professors[i].name),
                Group.find(Group.groups[i].name),
            ]
        )
        print("cpg->input->findid :", cpg)
        # cpg->input->findid : [0, 0, 0]
        # cpg->input->findid : [0, 0, 0, 1, 1, 1]
        # cpg->input->findid : [0, 0, 0, 1, 1, 1, 2, 2, 2]
        # cpg->input->findid : [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3]
        # cpg->input->findid : [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4]
        # cpg->input->findid : [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 0, 5]

    for _c in range(len(cpg)):
        # print("nilai _c perulangan :",_c)

        if _c % 3 == 0:
            cpg[_c] = (bin(cpg[_c])[2:]).rjust(bits_needed(CourseClass.classes), "0")
            # print("cpg->binary(courseclass) :",cpg[_c])
        elif _c % 3 == 1:  # Professor
            cpg[_c] = (bin(cpg[_c])[2:]).rjust(bits_needed(Professor.professors), "0")
            # print("cpg->binary(prof) :",cpg[_c])
        else:  # Group
            # print("else")
            cpg[_c] = (bin(cpg[_c])[2:]).rjust(bits_needed(Group.groups), "0")
            # print("cpg->binary(group) :",cpg[_c])
    print("cpg->binary :", cpg)

    cpg = join_cpg_pair(cpg)
    for r in range(len(Room.rooms)):
        lts.append((bin(r)[2:]).rjust(bits_needed(Room.rooms), "0"))

    for t in range(len(Slot.slots)):
        slots.append((bin(t)[2:]).rjust(bits_needed(Slot.slots), "0"))

    print("lts convert", lts)
    print("slots convert", slots)
    max_score = (len(cpg) - 1) * 3 + len(cpg) * 3


def init_population(n):
    print("#####init Population ({})".format(n))
    global cpg, lts, slots
    print("cpg :", cpg)
    print("lts :", lts)
    print("slots :", slots)

    chromosomes = []
    for _n in range(n):
        chromosome = []
        for _c in cpg:
            chromosome.append(_c + random.choice(slots) + random.choice(lts))
            print("chromosone ke ", _n, " =", chromosome)
        chromosomes.append(chromosome)
    print("chromosomes :", chromosomes)
    return chromosomes


# evaluate
def course_bits(chromosome):
    i = 0

    return chromosome[i : i + bits_needed(CourseClass.classes)]


def professor_bits(chromosome):
    i = bits_needed(CourseClass.classes)

    return chromosome[i : i + bits_needed(Professor.professors)]


def group_bits(chromosome):
    i = bits_needed(CourseClass.classes) + bits_needed(Professor.professors)

    return chromosome[i : i + bits_needed(Group.groups)]


def slot_bits(chromosome):
    # menetukan letak slot bit dari chromosome -> 00000000011101 -> 111
    i = (
        bits_needed(CourseClass.classes)
        + bits_needed(Professor.professors)
        + bits_needed(Group.groups)
    )

    return chromosome[i : i + bits_needed(Slot.slots)]


def lt_bits(chromosome):

    i = (
        bits_needed(CourseClass.classes)
        + bits_needed(Professor.professors)
        + bits_needed(Group.groups)
        + bits_needed(Slot.slots)
    )

    return chromosome[i : i + bits_needed(Room.rooms)]


def slot_clash(a, b):
    if slot_bits(a) == slot_bits(b):
        return 1
    return 0


# checks that a faculty member teaches only one course at a time.
def faculty_member_one_class(chromosome):
    scores = 0
    for i in range(len(chromosome) - 1):  # select one cpg pair
        clash = False
        for j in range(i + 1, len(chromosome)):  # check it with all other cpg pairs
            if slot_clash(chromosome[i], chromosome[j]) and professor_bits(
                chromosome[i]
            ) == professor_bits(chromosome[j]):
                clash = True
                # print("These prof. have clasches")
                # print_chromosome(chromosome[i])
                # print_chromosome(chromosome[j])
        if not clash:
            scores = scores + 1
    return scores


# check that a group member takes only one class at a time.
def group_member_one_class(chromosomes):
    scores = 0

    for i in range(len(chromosomes) - 1):
        clash = False
        for j in range(i + 1, len(chromosomes)):
            if slot_clash(chromosomes[i], chromosomes[j]) and group_bits(
                chromosomes[i]
            ) == group_bits(chromosomes[j]):
                # print("These classes have slot/lts clash")
                # print_chromosome(chromosomes[i])
                # print_chromosome(chromosomes[j])
                # print("____________")
                clash = True
                break
        if not clash:
            # print("These classes have no slot/lts clash")
            # print_chromosome(chromosomes[i])
            # print_chromosome(chromosomes[j])
            # print("____________")
            scores = scores + 1
    return scores


# checks that a course is assigned to an available classroom.
def use_spare_classroom(chromosome):
    scores = 0
    for i in range(len(chromosome) - 1):  # select one cpg pair
        clash = False
        for j in range(i + 1, len(chromosome)):  # check it with all other cpg pairs
            if slot_clash(chromosome[i], chromosome[j]) and lt_bits(
                chromosome[i]
            ) == lt_bits(chromosome[j]):
                # print("These classes have slot/lts clash")
                # printChromosome(chromosome[i])
                # printChromosome(chromosome[j])
                clash = True
        if not clash:
            scores = scores + 1
    return scores


# checks that the classroom capacity is large enough for the classes that
# are assigned to that classroom.
def classroom_size(chromosomes):
    scores = 0
    for _c in chromosomes:
        if (
            Group.groups[int(group_bits(_c), 2)].size
            <= Room.rooms[int(lt_bits(_c), 2)].size
        ):
            scores = scores + 1
    return scores


# check that room is appropriate for particular class/lab
def appropriate_room(chromosomes):
    scores = 0
    for _c in chromosomes:
        if (
            CourseClass.classes[int(course_bits(_c), 2)].is_lab
            == Room.rooms[int(lt_bits(_c), 2)].is_lab
        ):
            scores = scores + 1
    return scores


# check that lab is allocated appropriate time slot
def appropriate_timeslot(chromosomes):
    scores = 0
    for _c in chromosomes:
        if (
            CourseClass.classes[int(course_bits(_c), 2)].is_lab
            == Slot.slots[int(slot_bits(_c), 2)].is_lab_slot
        ):
            scores = scores + 1
    return scores


def evaluate(chromosomes):
    global max_score
    score = 0
    score = score + use_spare_classroom(chromosomes)
    score = score + faculty_member_one_class(chromosomes)
    score = score + classroom_size(chromosomes)
    score = score + group_member_one_class(chromosomes)
    score = score + appropriate_room(chromosomes)
    score = score + appropriate_timeslot(chromosomes)
    return score / max_score


hasil = []


def print_hasil():
    global hasil
    return hasil


def setNullHasil():
    global hasil
    hasil = []
    # print("hasil sudah kosong =", hasil)


# kembalikan dari binary ke id
def print_chromosome(chromosome):
    global hasil
    # hasil.clear
    hasil.append(
        (
            CourseClass.classes[int(course_bits(chromosome), 2)],
            " | ",
            Professor.professors[int(professor_bits(chromosome), 2)],
            " | ",
            Group.groups[int(group_bits(chromosome), 2)],
            " | ",
            Slot.slots[int(slot_bits(chromosome), 2)],
            " | ",
            Room.rooms[int(lt_bits(chromosome), 2)],
        )
    )
    print("chromosoome di print:", chromosome)
    print(
        CourseClass.classes[int(course_bits(chromosome), 2)],
        " | ",
        Professor.professors[int(professor_bits(chromosome), 2)],
        " | ",
        Group.groups[int(group_bits(chromosome), 2)],
        " | ",
        Slot.slots[int(slot_bits(chromosome), 2)],
        " | ",
        Room.rooms[int(lt_bits(chromosome), 2)],
    )


# crossover
def crossover(population):
    print("######Crossover")
    a = random.randint(0, len(population) - 1)
    b = random.randint(0, len(population) - 1)
    cut = random.randint(0, len(population[0]))  # assume all chromosome are of same len
    population.append(population[a][:cut] + population[b][cut:])


# Seleksi
# sort -> reverse -> pop
def selection(population, n):
    population.sort(key=evaluate, reverse=True)
    while len(population) > n:
        population.pop()


# Modified Combination of Row_reselect, Column_reselect
def mutate(chromosome):
    # print("Before mutation: ", end="")
    # printChromosome(chromosome)

    rand_slot = random.choice(slots)
    rand_lt = random.choice(lts)

    a = random.randint(0, len(chromosome) - 1)

    chromosome[a] = (
        course_bits(chromosome[a])
        + professor_bits(chromosome[a])
        + group_bits(chromosome[a])
        + rand_slot
        + rand_lt
    )

    # print("After mutation: ", end="")
    # printChromosome(chromosome)


def algo():
    print("b")
    generation = 0
    inisialisasi()
    convert_input_to_bin()
    population = init_population(3)

    # print("Original population:")
    # print(population)
    print("\n------------- Genetic Algorithm --------------\n")
    while True:

        # if termination criteria are satisfied, stop.
        if evaluate(max(population, key=evaluate)) == 1 or generation == 5000:
            print("Generations:", generation)
            print(
                "Best Chromosome fitness value", evaluate(max(population, key=evaluate))
            )
            print("Best Chromosome: ", max(population, key=evaluate))
            for lec in max(population, key=evaluate):
                print("nilai lec :", lec)
                print("tipe:", type(lec))
                # global result
                # result = lec
                print_chromosome(lec)
                # print("nilai a:", a)
                # return a
            break

        # Otherwise continue
        else:
            for _c in range(len(population)):
                crossover(population)
                selection(population, 5)

                # selection(population[_c], len(cpg))
                mutate(population[_c])

        # print("result lec 1:", lec)
        generation = generation + 1
        print("result akhir :", result)
        # return print
        # print("Gen: ", generation)

    # print("Population", len(population))
