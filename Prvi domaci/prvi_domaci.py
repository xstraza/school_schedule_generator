import math
import random
import matplotlib.pyplot as plt


# Cost Function
def trosak(x, y):
    prvi_deo = math.sin(3 * x * math.pi) ** 2
    drugi_deo = (x - 1) ** 2 * (1 + math.sin(3 * y * math.pi) ** 2)
    treci_deo = (y - 1) ** 2 * (1 + math.sin(2 * y * math.pi) ** 2)
    return prvi_deo + drugi_deo + treci_deo


# Parameters
number_of_starts = 5  # broj pokretanja
max_iterations = 500  # broj iteracija
precision = 5  # preciznost resenja
left_bound_x = -10  # leva granica x
right_bound_x = 10  # desna granica x
num_bits_x = int(math.ceil(math.log2((right_bound_x - left_bound_x) * math.pow(10, precision))))  # ovo ne dirati
left_bound_y = -10  # leva granica y
right_bound_y = 10  # desna granica y
num_bits_y = int(math.ceil(math.log2((right_bound_y - left_bound_y) * math.pow(10, precision))))  # ovo ne dirati
population_size = 20  # velicina populacije
new_population_size = int(population_size / 2)  # velicina nove populacije
tournament_size = 3  # broj ucesnika turnira
inversion_length = 5  # duzina inverzije
convergence_limit = 100  # ogranicenje konvergencije
cost_function = trosak  # funkcija troska


# Algorithm
def genetski():
    pop_vel = population_size
    npop_vel = new_population_size
    best_ever_loss = None
    avg_loss_points = []
    best_loss_points = []

    def iscrtaj(avg_loss_points, best_loss_points):

        count_list = range(0, len(avg_loss_points[0]))
        plt.plot(count_list, avg_loss_points[0], color='red', label='Run 1')
        count_list = range(0, len(avg_loss_points[1]))
        plt.plot(count_list, avg_loss_points[1], color='green', label='Run 2')
        count_list = range(0, len(avg_loss_points[2]))
        plt.plot(count_list, avg_loss_points[2], color='blue', label='Run 3')
        count_list = range(0, len(avg_loss_points[3]))
        plt.plot(count_list, avg_loss_points[3], color='orange', label='Run 4')
        count_list = range(0, len(avg_loss_points[4]))
        plt.plot(count_list, avg_loss_points[4], color='purple', label='Run 5')
        plt.axis([0, 150, 0, 10])
        plt.xlabel('Generacija')
        plt.ylabel('Prosecni trosak')
        plt.legend()
        title = 'Grafik prosecnog troska sa populacijom velicine ' + str(population_size)
        plt.title(title)
        plt.show()

        count_list = range(0, len(best_loss_points[0]))
        plt.plot(count_list, best_loss_points[0], color='red', label='Run 1')
        count_list = range(0, len(best_loss_points[1]))
        plt.plot(count_list, best_loss_points[1], color='green', label='Run 2')
        count_list = range(0, len(best_loss_points[2]))
        plt.plot(count_list, best_loss_points[2], color='blue', label='Run 3')
        count_list = range(0, len(best_loss_points[3]))
        plt.plot(count_list, best_loss_points[3], color='orange', label='Run 4')
        count_list = range(0, len(best_loss_points[4]))
        plt.plot(count_list, best_loss_points[4], color='purple', label='Run 5')
        plt.axis([0, 150, 0, 10])
        plt.xlabel('Generacija')
        plt.ylabel('Najbolji trosak')
        plt.legend()
        title = 'Grafik najboljeg troska sa populacijom velicine ' + str(population_size)
        plt.title(title)
        plt.show()

    def kodiraj(x, y):
        x = int(x * math.pow(10, precision))
        y = int(y * math.pow(10, precision))
        x = bin(int(x + right_bound_x * math.pow(10, precision)))
        y = bin(int(y + right_bound_y * math.pow(10, precision)))
        chromosome_x = list(x[2:].zfill(num_bits_x))
        chromosome_y = list(y[2:].zfill(num_bits_y))
        chromosome = list(map(int, chromosome_x + chromosome_y))
        return chromosome

    def dekodiraj(hromozom):
        def bin_to_dec(bitlist):
            out = 0
            for bit in bitlist:
                out = (out << 1) | bit
            return out

        og_x = bin_to_dec(hromozom[:num_bits_x])
        og_y = bin_to_dec(hromozom[num_bits_x:])
        og_x = og_x - right_bound_x * math.pow(10, precision)
        og_y = og_y - right_bound_y * math.pow(10, precision)
        og_x = og_x / math.pow(10, precision)
        og_y = og_y / math.pow(10, precision)
        tup = (og_x, og_y)
        return tup

    def jednotackasto(otac, majka, tacka=1):
        prvo_dete = otac[:tacka] + majka[tacka:]
        drugo_dete = otac[tacka:] + majka[:tacka]
        return prvo_dete, drugo_dete

    def inverzija(hromozom, duzina=1):
        mutirani = hromozom
        pocetak = random.randint(0, len(hromozom) - duzina)
        for i in range(pocetak, pocetak + duzina):
            mutirani[i] = 1 - mutirani[i]
        return mutirani

    def is_valid_chromosome(hromozom):
        if left_bound_x <= hromozom[0] <= right_bound_x:
            if left_bound_y <= hromozom[1] <= right_bound_y:
                return True
        return False

    def turnir(fja, population, vel):
        takmicari = []
        while len(takmicari) < vel:
            takmicari.append(random.choice(population))
        najbolji = None
        najbolji_trosak = None
        for tak in takmicari:
            ff = fja(tak[0], tak[1])
            if najbolji is None or ff < najbolji_trosak:
                najbolji = tak
                najbolji_trosak = ff
        return najbolji

    for k in range(number_of_starts):
        print('Pokretanje: ', k + 1)
        best = None
        best_f = None
        t = 0
        pop = []
        loss_points = []
        best_points = []
        convergence_counter = 0
        for h in range(pop_vel):
            x = random.uniform(left_bound_x, right_bound_x)
            y = random.uniform(left_bound_y, right_bound_y)
            pop.append((x, y))

        while t < max_iterations:
            n_pop = pop[:]
            while len(n_pop) < pop_vel + npop_vel:
                roditelj1 = turnir(cost_function, pop, tournament_size)
                roditelj2 = turnir(cost_function, pop, tournament_size)
                kodirani_roditelj1 = kodiraj(roditelj1[0], roditelj1[1])
                kodirani_roditelj2 = kodiraj(roditelj2[0], roditelj2[1])
                dete1, dete2 = jednotackasto(kodirani_roditelj1, kodirani_roditelj2,
                                             random.randrange(0, num_bits_x + num_bits_y))
                mutant1 = inverzija(dete1, inversion_length)
                mutant2 = inverzija(dete2, inversion_length)
                obican1 = dekodiraj(mutant1)
                obican2 = dekodiraj(mutant2)
                if is_valid_chromosome(obican1):
                    n_pop.append(obican1)
                if is_valid_chromosome(obican2):
                    n_pop.append(obican2)
            pop = sorted(n_pop, key=lambda tup: cost_function(tup[0], tup[1]))[:pop_vel]
            f = cost_function(pop[0][0], pop[0][1])
            mapirano = []
            for p in pop:
                mapirano.append(cost_function(p[0], p[1]))
            average_f = sum(mapirano) / pop_vel
            loss_points.append(average_f)
            best_points.append(trosak(pop[0][0], pop[0][1]))
            print('Iter:', t + 1, ', best cost:', f, ', average cost:', average_f)
            if best_f is None or best_f > f:
                best_f = f
                best = pop[0]
            else:
                convergence_counter += 1
                if convergence_counter == convergence_limit:
                    break
            t += 1

        avg_loss_points.append(loss_points)
        best_loss_points.append(best_points)
        best_loss = trosak(pop[0][0], pop[0][1])
        if best_ever_loss is None or best_loss < best_ever_loss:
            best_ever_loss = best_loss
        print('Najbolji trosak za pokretanje', k + 1, ':', best_f, ', sastav najboljeg hromozoma:',
              kodiraj(best[0], best[1]), ', dekodirano: (', best[0], best[1], ')')

    iscrtaj(avg_loss_points, best_loss_points)


genetski()
