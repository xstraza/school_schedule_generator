import json


def open_json(path):
    with open(path) as f:
        data = json.load(f)
    return data


def group_profs(path):
    data = open_json(path)
    a, b, c, d = get_groups_profs(data)
    return a, b, c, d


def get_groups_profs(data):
    classes = data['Casovi']
    group_set = set()
    prof_set = set()
    for clazz in classes:
        for group in clazz["Grupe"]:
            group_set.add(group)
        prof_set.add(clazz['Nastavnik'])

    group_len = len(group_set)
    group_dict = dict(zip(group_set, list(range(group_len))))

    prof_len = len(prof_set)
    prof_dict = dict(zip(prof_set, list(range(prof_len))))

    return group_dict, group_len, prof_dict, prof_len


def classrooms(path):
    data = open_json(path)
    a, b, c = get_classrooms(data)
    return a, b, c


def get_classrooms(data):
    rooms_translation_dict = data['Ucionice']
    rooms_list = list()
    for key in rooms_translation_dict:
        for room in rooms_translation_dict[key]:
            rooms_list.append(room)

    rooms_len = len(rooms_list)
    rooms_dict = dict(zip(rooms_list, list(range(rooms_len))))

    return rooms_dict, rooms_len, rooms_translation_dict


def data_for_checker(path):
    data = open_json(path)
    _, g_l, _, p_l = get_groups_profs(data)
    _, r_l, _ = get_classrooms(data)
    return [g_l, p_l, r_l]


def all_slots(path):
    data = open_json(path)
    return data['Casovi']
