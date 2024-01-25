"""Car inventory."""


def list_of_cars(all_cars: str) -> list:
    """
    Return list of cars.

    The input string contains of car makes and models, separated by comma.
    Both the make and the model do not contain spaces (both are one word).

    "Audi A4,Skoda Superb,Audi A4" => ["Audi A4", "Skoda Superb", "Audi A4"]
    """
    if all_cars:
        return all_cars.split(",")
    else:
        return []


def car_makes(all_cars: str) -> list:
    """
    Return list of unique car makes.

    The order of the elements should be the same as in the input string (first appearance).

    "Audi A4,Skoda Superb,Audi A4" => ["Audi", "Skoda"]
    """
    unique_cars_list = []
    if all_cars:
        for car in list_of_cars(all_cars):
            if car.split()[0] not in unique_cars_list:
                unique_cars_list.append(car.split()[0])
        return unique_cars_list
    else:
        return []


def car_models(all_cars: str) -> list:
    """
    Return list of unique car models.

    The order of the elements should be the same as in the input string (first appearance).

    "Audi A4,Skoda Superb,Audi A4,Audi A6" => ["A4", "Superb", "A6"]
    """
    unique_car_models_list = []
    if all_cars:
        for model in list_of_cars(all_cars):
            car_model = model.strip().lstrip(model.split()[0]).strip()
            if car_model not in unique_car_models_list:
                unique_car_models_list.append(car_model.strip())
        return unique_car_models_list
    else:
        return []


def search_by_make(all_cars: str, car_make: str) -> list:
    """Search car makes from all cars."""
    searched_cars = []
    all_the_cars = list_of_cars(all_cars)
    all_the_cars_lower = list_of_cars(all_cars.lower())
    if car_make and all_cars:
        car_make_split = car_make.split()[0]
        for index, car in enumerate(all_the_cars_lower):
            if car_make_split.lower() in car.split() and car_make_split.lower() \
                    not in all_the_cars_lower[index].split()[1:]:
                searched_cars.append(all_the_cars[index].strip())
        return searched_cars
    else:
        return []


def search_by_model(all_cars: str, model: str) -> list:
    """Search car models from all cars."""
    searched_models = []
    all_the_cars = list_of_cars(all_cars)
    all_the_cars_lower = list_of_cars(all_cars.lower())
    if model and all_cars:
        for index, model_name in enumerate(all_the_cars_lower):
            split_model_elements = model_name.strip().lstrip(model_name.split()[0]).strip()
            print(split_model_elements)
            if model.lower() in split_model_elements.split():
                searched_models.append(all_the_cars[index].strip())
        return searched_models
    else:
        return []


def car_make_and_models(all_cars: str) -> list:
    """
    Create a list of structured information about makes and models.

    For each different car make in the input string an element is created in the output list.
    The element itself is a list, where the first position is the name of the make (string),
    the second element is a list of models for the given make (list of strings).

    No duplicate makes or models should be in the output.

    The order of the makes and models should be the same os in the input list (first appearance).

    "Audi A4,Skoda Super,Skoda Octavia,BMW 530,Seat Leon Lux,Skoda Superb,Skoda Superb,BMW x5" =>
    [['Audi', ['A4']], ['Skoda', ['Super', 'Octavia', 'Superb']], ['BMW', ['530', 'x5']], ['Seat', ['Leon Lux']]]
    """
    all_the_cars = list_of_cars(all_cars)
    all_the_cars_as_str = ",".join(all_the_cars)  # All car makes and models as string
    unique_car_makes = car_makes(all_cars)  # All unique car makes
    makes_and_models_list = []  # Output list of car makes and models

    if all_cars:
        for index, make in enumerate(unique_car_makes):
            # Add car make to the list
            makes_and_models_list.append([unique_car_makes[index]])
            # Get the list of specific car make and all of its models
            make_and_model = search_by_make(all_the_cars_as_str, unique_car_makes[index])
            # For each unique car make, the models list is set to empty
            car_models_only = []
            # Loop through make_and_model list
            for i in make_and_model:
                # Add all the models of unique car make to the car_models_list
                car_models_only += i.split(" ", 1)[1:]

            car_models_unique = []
            # Sort out the duplicates and add to the car_models_unique list
            for make_and_model in car_models_only:
                if make_and_model not in car_models_unique:
                    car_models_unique.append(make_and_model)
            # Finally add all the models that belong to specific car make, to that list
            makes_and_models_list[index].append(car_models_unique)
        return makes_and_models_list
    else:
        return []


def add_cars(car_list: list, all_cars: str) -> list:
    """
    Add cars from the list into the existing car list.

    The first parameter is in the same format as the output of the previous function.
    The second parameter is a string of comma separated cars (as in all the previous functions).
    The task is to add cars from the string into the list.

    Hint: This and car_make_and_models are very similar functions. Try to use one inside another.

    [['Audi', ['A4']], ['Skoda', ['Superb']]]
    and
    "Audi A6,BMW A B C,Audi A4"

    =>

    [['Audi', ['A4', 'A6']], ['Skoda', ['Superb']], ['BMW', ['A B C']]]
    """
    cars_to_add = car_make_and_models(all_cars)
    list_of_car_list = []
    for sublist in car_list:
        for make in sublist:
            list_of_car_list.append(make)

    for i in cars_to_add:
        if i[0] in list_of_car_list:
            for index, element in enumerate(car_list):
                if element[0] == i[0]:
                    car_list[index][1].extend(x for x in i[1] if x not in element[1])
        else:
            car_list.append(i)
    return car_list


def number_of_cars(all_cars: str) -> list:
    """
    Create a list of tuples with make quantities.

    The result is a list of tuples.
    Each tuple is in the form: (make_name: str, quantity: int).
    The order of the tuples (makes) is the same as the first appearance in the list.
    """
    unique_car_makes = car_makes(all_cars)
    all_cars_as_list = list_of_cars(all_cars)
    all_car_makes = []
    final_list = []

    if all_cars:
        for car in all_cars_as_list:
            all_car_makes.append(car.split()[0])

        for i in unique_car_makes:
            car_make_and_count = [i] + [all_car_makes.count(i)]
            final_list.append(tuple(car_make_and_count))
        return final_list
    else:
        return []


def car_list_as_string(cars: list) -> str:
    """
    Create a list of cars.

    The input list is in the same format as the result of car_make_and_models function.
    The order of the elements in the string is the same as in the list.
    [['Audi', ['A4']], ['Skoda', ['Superb']]] =>
    "Audi A4,Skoda Superb"
    """
    car_makes_list = []
    final_list = []
    for sublist in cars:
        for element in sublist:
            if isinstance(element, list):
                for i in element:
                    final_list.append(car_makes_list[-1] + " " + "".join(i))
            else:
                car_makes_list.append(element)
    return ",".join(final_list)
