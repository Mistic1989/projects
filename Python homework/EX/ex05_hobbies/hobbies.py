"""EX05 - Hobbies."""


def create_dictionary(data: str) -> dict:
    """
    Create dictionary about people and their hobbies ie. {name1: [hobby1, hobby2, ...], name2: [...]}.

    There should be no duplicate hobbies on 1 person.

    :param data: given string from database
    :return: dictionary where keys are people and values are lists of hobbies
    """
    split_hobbies = data.split("\n")
    names_and_hobbies_list = []
    names_list = []
    final_list = {}

    for name in split_hobbies:
        names_and_hobbies_list.append(name.split(":"))
    for name in names_and_hobbies_list:
        names_list.append(name[0])
    unique_names = list(set(names_list))

    for name in unique_names:
        hobbies = []
        for hobby in names_and_hobbies_list:
            if hobby[0] == name and hobby[1] not in hobbies:
                hobbies.append(hobby[1])
        final_list[name] = hobbies
    return final_list


def sort_dictionary(dic: dict) -> dict:
    """
    Sort dictionary values alphabetically.

    The order of keys is not important.

    sort_dictionary({"b":[], "a":[], "c": []})  => {"b":[], "a":[], "c": []}
    sort_dictionary({"": ["a", "f", "d"]})  => {"": ["a", "d", "f"]}
    sort_dictionary({"b":["d", "a"], "a":["c", "f"]})  => {"b":["a", "d"], "a":["c", "f"]}
    sort_dictionary({"Jack": ["swimming", "hiking"], "Charlie": ["games", "yoga"]})
        => {"Jack": ["hiking", "swimming"], "Charlie": ["games", "yoga"]}

    :param dic: dictionary to sort
    :return: sorted dictionary
    """
    for key, value in dic.items():
        dic[key] = sorted(value)
    return dic


def create_dictionary_with_hobbies(data: str) -> dict:
    """
    Create dictionary about hobbies and their hobbyists ie. {hobby1: [name1, name2, ...], hobby2: [...]}.

    :param data: given string from database
    :return: dictionary, where keys are hobbies and values are lists of people. Values are sorted alphabetically
    """
    all_the_names_hobbies = []
    final_dict = {}

    find_all_the_hobbies = []
    for name in data.split("\n"):
        find_all_the_hobbies.append(name.split(":"))
    all_hobbies = []
    for hobby in find_all_the_hobbies:
        all_hobbies += hobby[1:]

    split_names_hobbies = data.split("\n")
    for name_and_hobby in split_names_hobbies:
        all_the_names_hobbies.append(name_and_hobby.split(":"))

    unique_hobbies_list = list(set(all_hobbies))
    for hobby in unique_hobbies_list:
        names = []
        for name_and_hobby in all_the_names_hobbies:
            if name_and_hobby[1] == hobby and name_and_hobby[0] not in names:
                names.append(name_and_hobby[0])
        final_dict[hobby] = names
    return sort_dictionary(final_dict)


def find_people_with_most_hobbies(data: str) -> list:
    """
    Find the people who have the most hobbies.

    :param data: given string from database
    :return: list of people with most hobbies. Sorted alphabetically.
    """
    split_names_hobbies = data.split("\n")
    data_as_dict = create_dictionary_with_hobbies(data)
    all_the_names_hobbies = []
    names_list = []

    for name in split_names_hobbies:
        all_the_names_hobbies.append(name.split(":"))
    for name in all_the_names_hobbies:
        names_list.append(name[0])
    unique_names = list(set(names_list))

    names_for_each_hobby = []
    for index, name in enumerate(unique_names):
        names_for_each_hobby.append([name])
        for key, value in data_as_dict.items():
            if name in value:
                names_for_each_hobby[index].append(key)

    best_result = 0
    most_hobbies_persons = []
    persons = ""
    for i in names_for_each_hobby:
        if len(i[1:]) > best_result:
            best_result = len(i[1:])
            persons = i[0]

    most_hobbies_persons.append(persons)
    for i in names_for_each_hobby:
        if len(i[1:]) == best_result and i[0] not in most_hobbies_persons:
            most_hobbies_persons.append(i[0])
    return sorted(most_hobbies_persons)


def find_least_popular_hobbies(data: str) -> list:
    """
    Find the least popular hobbies.

    :param data: given string from database
    :return: list of least popular hobbies. Sorted alphabetically.
    """
    hobbies_dict = create_dictionary(data)
    names_dict = create_dictionary_with_hobbies(data)
    hobbies_count = {}

    for hobby, names in names_dict.items():
        count = 0
        for name, hobbies in hobbies_dict.items():
            if hobby in hobbies:
                count += 1
        hobbies_count[hobby] = count

    least_popular_hobbies = []
    for hobby, hobby_count in hobbies_count.items():
        if hobby_count == min(hobbies_count.values()):
            least_popular_hobbies.append(hobby)
    return sorted(least_popular_hobbies)


def sort_names_and_hobbies(data: str) -> tuple:
    """
    Create a tuple of sorted names and their hobbies.

    The structure of the tuple is as follows:
    (
        (name1, (hobby1, hobby2)),
        (name2, (hobby1, hobby2)),
         ...
    )

    For each person, there is a tuple, where the first element is the name (string)
    and the second element is an ordered tuple of hobbies (ordered alphabetically).
    All those person-tuples are ordered by the name of the person and are inside a tuple.
    """
    name_and_hobbies = create_dictionary(data)
    final_list = []
    person_list = []
    for name, hobby in name_and_hobbies.items():
        person_list.append([name])
        person_list[0].append(tuple(sorted(hobby)))
        final_list.append(tuple(person_list[0]))
        person_list = []
    return tuple(sorted(final_list))


def find_people_with_hobbies(data: str, hobbies: list) -> set:
    r"""
    Find all the different people with certain hobbies.

    It is recommended to use set here.

    Example:
        data="John:running\nMary:running\nJohn:dancing\nJack:dancing\nJack:painting\nSmith:painting"
        hobbies=["running", "dancing"]
    Result:
        {"John", "Mary", "Jack"}
    """
    data_as_dict = create_dictionary_with_hobbies(data)
    names = []
    for key, value in data_as_dict.items():
        if key in hobbies:
            names += value
    return set(names)


def find_two_people_with_most_common_hobbies(data: str) -> tuple:
    """
    Find a pair of people who have the highest ratio of common hobbies to different hobbies.

    Common hobbies are the ones which both people have.
    Different hobbies are the ones, which only one person has.

    Example:
    John has:
        running
        walking
    Mary has:
        dancing
        running
    Nora has:
        running
        singing
        dancing

    Pairs and corresponding common and different hobbies, ratio
    John and Mary; common: running; diff: walking, dancing; ratio: 1/2
    John and Nora; common: running; diff: walking, singing, dancing; ratio: 1/3
    Mary and Nora; common: running, dancing; diff: singing; ratio: 2/1

    So the best result is Mary and Nora. It doesn't matter in which order the names are returned.

    If multiple pairs have the same best ratio, it doesn't matter which pair (and in which order) is returned.

    If there are less than 2 people in the input, return None.
    """
    data_as_list = list(create_dictionary(data).items())
    if len(data_as_list) >= 2:
        ratios_with_diff = 0
        ratios_no_diff = 0
        best_pair = ""
        for name_hobby_1 in data_as_list[:-1]:
            for name_hobby_2 in data_as_list[1:]:
                name1 = name_hobby_1[0]
                name2 = name_hobby_2[0]
                if name_hobby_1[0] != name_hobby_2[0]:
                    pair = []
                    pair += name1, name2
                    common = set(name_hobby_1[1]).intersection(set(name_hobby_2[1]))
                    diff = set(name_hobby_1[1]).symmetric_difference(set(name_hobby_2[1]))
                    if len(diff) == 0 and len(common) > 0 and ratios_no_diff < len(common):
                        ratios_no_diff = len(common)
                        ratios_with_diff = ratios_no_diff
                        best_pair = pair
                    if len(diff) >= 1 and ratios_with_diff <= len(common) / len(diff) and ratios_no_diff == 0:
                        ratios_with_diff = len(common) / len(diff)
                        best_pair = pair
        return tuple(best_pair)
    return None
