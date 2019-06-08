from genome import Gene
import copy
import json

number_of_runs = 5
first_phase_generations = 500
second_phase_generations = 2000
initial_pool_size = 5


def one_plus_one(input_file):
    for i in range(number_of_runs):
        pool = list()
        for j in range(initial_pool_size):
            pool.append(Gene(path=input_file))
        generations = 0
        while generations < first_phase_generations:
            new_pool = list()
            for gene in pool:
                child = copy.deepcopy(gene)
                child.mutate()
                if child.cost_function() >= gene.cost_function():
                    new_pool.append(child)
                else:
                    new_pool.append(gene)
            pool = new_pool
            generations += 1
        winner = None
        for gene in pool:
            if winner is None or winner.cost_function() < gene.cost_function():
                winner = gene
        generations = 0
        while generations < second_phase_generations:
            child = copy.deepcopy(winner)
            child.mutate()
            if child.cost_function() >= winner.cost_function():
                winner = copy.deepcopy(child)
            generations += 1
        data = winner.export()
        max_groups, avg_groups = winner.checker.group_pause_stats()
        hours_groups = winner.checker.six_hours_groups()
        max_profs, avg_profs = winner.checker.prof_pause_stats()
        hours_profs = winner.checker.six_hours_prof()
        empty = winner.checker.check_empty_hour()
        print("Pokretanje", str(i + 1))
        print('Trosak nakon algoritma:', winner.cost_function() / 6.05)
        print('Pogresnih rasporeda:', winner.checker.check_for_inversions())
        print('Maksimalan prazan hod za grupu:', max_groups)
        print('Prosecan prazan hod za grupu:', avg_groups)
        print('Broj dana sa vise od 6 sati nastave za grupe:', hours_groups)
        print('Maksimalan prazan hod za profesora:', max_profs)
        print('Prosecan prazan hod za profesora:', avg_profs)
        print('Broj dana sa vise od 6 sati nastave za profesore:', hours_profs)
        print('Slobodnih sata:', empty, '\n')
        file = 'run' + str(i + 1) + '.txt'
        with open(file, 'w') as outfile:
            json.dump(data, outfile, indent=4)


one_plus_one('ulaz1.txt')
# one_plus_one('ulaz2.txt')
# one_plus_one('ulaz3.txt')
