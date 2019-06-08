import random

import schedule_parser as parse


class Gene:
    list_of_slots = None
    slots_len = None
    group_dict = None
    group_len = None
    prof_dict = None
    prof_len = None
    rooms_dict = None
    rooms_len = None
    rooms_translation_dict = None
    path = None

    def __init__(self, path='ulaz1.txt'):
        if Gene.path is None:
            Gene.path = path
        if Gene.group_dict is None:
            Gene.group_dict, Gene.group_len, Gene.prof_dict, Gene.prof_len = parse.group_profs(Gene.path)
        if Gene.rooms_dict is None:
            Gene.rooms_dict, Gene.rooms_len, Gene.rooms_translation_dict = parse.classrooms(Gene.path)
        if Gene.list_of_slots is None:
            Gene.fill_list_of_slots(Gene, Gene.path)
        print(Gene.group_len, Gene.prof_len)
        self.checker = Checker(Gene.path)
        self.genes = list()
        for i in range(Gene.slots_len):
            curr_slot = Gene.list_of_slots[i]
            new_gene = Gene.Genome(curr_slot.rooms, curr_slot.duration)
            self.genes.append(new_gene)
            self.checker.add(new_gene, i)

    def fill_list_of_slots(self, path):
        classes = parse.all_slots(path)

        Gene.list_of_slots = list()
        for clazz in classes:
            Gene.list_of_slots.append(Gene.Slot(clazz))
        Gene.slots_len = len(self.list_of_slots)

    class Genome:

        def __init__(self, rooms, duration):
            self.room = random.choice(rooms)
            day = 12 * random.randrange(5)
            hour = random.randrange(13 - duration)
            self.time = day + hour

    class Slot:

        def __init__(self, slot_dict):
            self.name = slot_dict['Predmet']
            self.tip = 2 if slot_dict['Tip'] == 'L' else 1 if slot_dict['Tip'] == 'V' else 0
            self.prof = Gene.prof_dict[slot_dict['Nastavnik']]
            self.rooms = list()
            for room in Gene.rooms_translation_dict[slot_dict['Ucionica']]:
                self.rooms.append(Gene.rooms_dict[room])
            self.groups = list()
            for group in slot_dict['Grupe']:
                self.groups.append(Gene.group_dict[group])
            self.duration = int(slot_dict['Trajanje'])

    def export(self):
        prof_d = {v: k for k, v in self.prof_dict.items()}
        group_d = {v: k for k, v in self.group_dict.items()}
        rooms_d = {v: k for k, v in self.rooms_dict.items()}
        tip_d = {0: 'P', 1: 'V', 2: 'L'}
        lista = list()
        for i, slot in enumerate(self.list_of_slots):
            recnik = dict()
            recnik['Predmet'] = slot.name
            recnik['Tip'] = tip_d[slot.tip]
            recnik['Nastavnik'] = prof_d[slot.prof]
            grupe = list()
            for group in slot.groups:
                grupe.append(group_d[group])
            recnik['Grupe'] = grupe
            gene = self.genes[i]
            recnik['Ucionica'] = rooms_d[gene.room]
            recnik['Trajanje'] = slot.duration
            recnik['Vreme'] = gene.time
            lista.append(recnik)
        data = dict()
        data['Raspored'] = lista
        return data

    def mutate(self):
        problem_list = list()
        for i in range(self.slots_len):
            genome = self.genes[i]
            if self.checker.check_correct_room(genome, i) == 0:
                problem_list.append(i)
                continue
            if self.checker.check_only_class_for_group(genome, i) == 0:
                problem_list.append(i)
                continue
            if self.checker.check_only_class_for_prof(genome, i) == 0:
                problem_list.append(i)
                continue
            if self.checker.check_only_class_in_room(genome) == 0:
                problem_list.append(i)
                continue
        if len(problem_list) > 0:
            choice = random.choice(problem_list)
        else:
            choice = random.randrange(self.slots_len)
        gene = self.genes[choice]
        slot = self.list_of_slots[choice]
        self.checker.remove(gene, choice)
        rooms = slot.rooms
        list_of_starts = list()
        for room in rooms:
            for day in range(5):
                for hour in range(13 - slot.duration):
                    empty = True
                    for t in range(slot.duration):
                        if self.checker.rooms[room][day * 12 + hour + t] > 0:
                            empty = False
                            break
                    if empty:
                        tup = (room, day * 12 + hour)
                        list_of_starts.append(tup)
        if len(list_of_starts) > 0:
            tup = random.choice(list_of_starts)
            gene.time = tup[1]
            gene.room = tup[0]
        self.checker.add(gene, choice)

    def cost_function(self):
        score = 0
        for i in range(self.slots_len):
            genome = self.genes[i]
            val = self.checker.check_correct_room(genome, i)
            score += val
            val = self.checker.check_only_class_for_group(genome, i)
            score += val
            val = self.checker.check_only_class_for_prof(genome, i)
            score += val
            val = self.checker.check_only_class_in_room(genome)
            score += val
        final_score = score / (4 * self.slots_len)
        if final_score == 1:
            final_score += self.checker.check_for_order()
            final_score += self.checker.check_pauses_for_groups() ** 2
            final_score += self.checker.check_hours_groups() ** 2
            final_score += self.checker.check_pauses_for_profs() ** 3
            final_score += self.checker.check_hours_profs() ** 3
            final_score += (1 if self.checker.check_empty_hour() > 0 else 0) * 0.05
        return final_score


class Checker:

    def __init__(self, path):
        stuff = parse.data_for_checker(path)
        self.groups = list()
        self.group_classes = list()
        for i in range(stuff[0]):
            self.groups.append([])
            for j in range(60):
                self.groups[i].append(0)
            classes = dict()
            for slot in Gene.list_of_slots:
                if i in slot.groups and slot.name in classes:
                    if classes[slot.name][slot.tip] is None:
                        classes[slot.name][slot.tip] = -1
                else:
                    classes[slot.name] = [None, None, None]
            self.group_classes.append(classes)
        self.profs = list()
        for i in range(stuff[1]):
            self.profs.append([])
            for j in range(60):
                self.profs[i].append(0)
        self.rooms = list()
        for i in range(stuff[2]):
            self.rooms.append([])
            for j in range(60):
                self.rooms[i].append(0)

    def add(self, genome, ind):
        time = genome.time
        room = genome.room
        slot = Gene.list_of_slots[ind]
        for t in range(slot.duration):
            for group in slot.groups:
                self.groups[group][time + t] += 1
            self.rooms[room][time + t] += 1
            self.profs[slot.prof][time + t] += 1
        for group in slot.groups:
            self.group_classes[group][slot.name][slot.tip] = time

    def remove(self, genome, ind):
        time = genome.time
        room = genome.room
        slot = Gene.list_of_slots[ind]
        for t in range(slot.duration):
            for group in slot.groups:
                self.groups[group][time + t] -= 1
            self.rooms[room][time + t] -= 1
            self.profs[slot.prof][time + t] -= 1

    def check_only_class_in_room(self, genome):
        room = genome.room
        time = genome.time
        if self.rooms[room][time] == 1:
            return 1
        return 0

    def check_only_class_for_prof(self, genome, ind):
        slot = Gene.list_of_slots[ind]
        prof = slot.prof
        time = genome.time
        if self.profs[prof][time] == 1:
            return 1
        return 0

    def check_only_class_for_group(self, genome, ind):
        slot = Gene.list_of_slots[ind]
        groups = slot.groups
        time = genome.time
        for group in groups:
            if self.groups[group][time] > 1:
                return 0
        return 1

    def check_correct_room(self, genome, ind):
        slot = Gene.list_of_slots[ind]
        rooms = slot.rooms
        room = genome.room
        if room in rooms:
            return 1
        return 0

    def check_hours_groups(self):
        maximal_pauses = 5 * len(self.groups)
        cnt = 0
        for group in self.groups:
            for day in range(5):
                counter = 0
                for hour in range(day * 12, (day + 1) * 12):
                    if group[hour] == 1:
                        counter += 1
                if counter > 6:
                    cnt += 1
        final_score = 1 - (cnt / maximal_pauses)
        return final_score

    def six_hours_groups(self):
        cnt = 0
        for day in range(5):
            for group in self.groups:
                counter = 0
                for hour in range(day * 12, (day + 1) * 12):
                    if group[hour] == 1:
                        counter += 1
                if counter > 6:
                    cnt += 1
        return cnt

    def check_hours_profs(self):
        maximal_pauses = 5 * len(self.profs)
        cnt = 0
        for prof in self.profs:
            for day in range(5):
                counter = 0
                for hour in range(day * 12, (day + 1) * 12):
                    if prof[hour] == 1:
                        counter += 1
                if counter > 6:
                    cnt += 1
        final_score = 1 - (cnt / maximal_pauses)
        return final_score

    def six_hours_prof(self):
        cnt = 0
        for day in range(5):
            for prof in self.profs:
                counter = 0
                for hour in range(day * 12, (day + 1) * 12):
                    if prof[hour] == 1:
                        counter += 1
                if counter > 6:
                    cnt += 1
        return cnt

    def check_pauses_for_groups(self):
        maximal_pauses = 50 * len(self.groups)
        pauses_sum = 0
        for group in self.groups:
            for day in range(5):
                active = False
                counter = 0
                for hour in range(day * 12, (day + 1) * 12):
                    if group[hour] == 1:
                        if active:
                            pauses_sum += counter
                            counter = 0
                        else:
                            active = True
                    else:
                        if active:
                            counter += 1
        final_score = 1 - (pauses_sum / maximal_pauses)
        return final_score

    def group_pause_stats(self):
        max_pause = 0
        avg_pauses_sum = 0
        for group in self.groups:
            pause_sum = 0
            for day in range(5):
                active = False
                counter = 0
                for hour in range(day * 12, (day + 1) * 12):
                    if group[hour] == 1:
                        if active:
                            pause_sum += counter
                            if counter > max_pause:
                                max_pause = counter
                            counter = 0
                        else:
                            active = True
                    else:
                        if active:
                            counter += 1
            avg_pauses_sum += pause_sum / 5
        avg_pause = avg_pauses_sum / len(self.groups)
        return max_pause, avg_pause

    def check_pauses_for_profs(self):
        maximal_pauses = 50 * len(self.profs)
        pauses_sum = 0
        for prof in self.profs:
            for day in range(5):
                active = False
                counter = 0
                for hour in range(day * 12, (day + 1) * 12):
                    if prof[hour] == 1:
                        if active:
                            pauses_sum += counter
                            counter = 0
                        else:
                            active = True
                    else:
                        if active:
                            counter += 1
        final_score = 1 - (pauses_sum / maximal_pauses)
        return final_score

    def prof_pause_stats(self):
        max_pause = 0
        pauses_sum = 0
        for prof in self.profs:
            for day in range(5):
                active = False
                counter = 0
                for hour in range(day * 12, (day + 1) * 12):
                    if prof[hour] == 1:
                        if active:
                            pauses_sum += counter
                            if counter > max_pause:
                                max_pause = counter
                            counter = 0
                        else:
                            active = True
                    else:
                        if active:
                            counter += 1
        avg_pause = pauses_sum / len(self.profs)
        return max_pause, avg_pause

    def check_empty_hour(self):
        counter = 0
        for i in range(60):
            flag = True
            for room in self.rooms:
                if room[i] == 1:
                    flag = False
                    break
            if flag:
                counter += 1
        return counter

    def check_for_order(self):
        maximum_inversions = 0
        inversions = 0
        for group_class in self.group_classes:
            for class_name in group_class:
                start_times = list()
                for tip in range(3):
                    if group_class[class_name][tip] is not None:
                        start_times.append(group_class[class_name][tip])
                if len(start_times) > 1:
                    maximum_inversions += len(start_times)
                    if len(start_times) == 2:
                        if start_times[0] > start_times[1]:
                            inversions += 1
                    else:
                        for i in range(3):
                            for j in range(i + 1, 3):
                                if start_times[i] > start_times[j]:
                                    inversions += 1
        final_score = 1 - (inversions / maximum_inversions)
        return final_score

    def check_for_inversions(self):
        maximum_inversions = 0
        inversions = 0
        for group_class in self.group_classes:
            for class_name in group_class:
                start_times = list()
                for tip in range(3):
                    if group_class[class_name][tip] is not None:
                        start_times.append(group_class[class_name][tip])
                print(start_times)
                if len(start_times) > 1:
                    maximum_inversions += len(start_times)
                    if len(start_times) == 2:
                        if start_times[0] > start_times[1]:
                            inversions += 1
                    else:
                        for i in range(3):
                            for j in range(i + 1, 3):
                                if start_times[i] > start_times[j]:
                                    inversions += 1
        return inversions
