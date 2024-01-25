"""File handling."""
import csv
import os
from datetime import datetime
from datetime import date


def read_file_contents(filename: str) -> str:
    """
    Read file contents into string.

    In this exercise, we can assume the file exists.

    :param filename: File to read.
    :return: File contents as string.
    """
    with open(filename, "r") as file:
        return file.read()


def read_file_contents_to_list(filename: str) -> list:
    r"""
    Read file contents into list of lines.

    In this exercise, we can assume the file exists.
    Each line from the file should be a separate element.
    The order of the list should be the same as in the file.

    List elements should not contain new line (\n).

    :param filename: File to read.
    :return: List of lines.
    """
    with open(filename, "r") as file:
        return file.read().splitlines()


def read_csv_file(filename: str, set_delimiter=",") -> list:
    """
    Read CSV file into list of rows.

    Each row is also a list of "columns" or fields.

    CSV (Comma-separated values) example:
    name,age
    john,12
    mary,14

    Should become:
    [
      ["name", "age"],
      ["john", "12"],
      ["mary", "14"]
    ]

    Use csv module.

    :param set_delimiter:
    :param filename: File to read.
    :return: List of lists.
    """
    data_list = []
    with open(filename, "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=set_delimiter)
        for row in csv_reader:
            data_list.append(row)
    return data_list


def write_contents_to_file(filename: str, contents: str) -> None:
    """
    Write contents to file.

    If the file does not exist, create it.

    :param filename: File to write to.
    :param contents: Content to write to.
    :return: None
    """
    with open(filename, "w") as file:
        file.write(contents)


def write_lines_to_file(filename: str, lines: list) -> None:
    """
    Write lines to file.

    Lines is a list of strings, each represents a separate line in the file.

    There should be no new line in the end of the file.
    Unless the last element itself ends with the new line.

    :param filename: File to write to.
    :param lines: List of string to write to the file.
    :return: None
    """
    with open(filename, "w") as file:
        file.writelines("\n".join(lines))


def write_csv_file(filename: str, data: list) -> None:
    """
    Write data into CSV file.

    Data is a list of lists.
    List represents lines.
    Each element (which is list itself) represents columns in a line.

    [["name", "age"], ["john", "11"], ["mary", "15"]]
    Will result in csv file:

    name,age
    john,11
    mary,15

    Use csv module here.

    :param filename: Name of the file.
    :param data: List of lists to write to the file.
    :return: None
    """
    with open(filename, "w", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerows(data)


def merge_dates_and_towns_into_csv(dates_filename: str, towns_filename: str, csv_output_filename: str) -> None:
    """
    Merge information from two files into one CSV file.

    Dates file contains result and dates. Separated by colon.
    john:01.01.2001
    mary:06.03.2016

    You don't have to validate the date.
    Every row contains name, colon and date.

    Towns file contains result and towns. Separated by colon.
    john:london
    mary:new york

    Every row contains name, colon and town name.
    There are no headers in the input files.

    Those two files should be merged by result.
    The result should be a csv file:

    name,town,date
    john,london,01.01.2001
    mary,new york,06.03.2016

    Applies for the third part:
    If information about a person is missing, it should be "-" in the output file.

    The order of the lines should follow the order in dates input file.
    Names which are missing in dates input file, will follow the order
    in towns input file.
    The order of the fields is: name,town,date

    name,town,date
    john,-,01.01.2001
    mary,new york,-

    Hint: try to reuse csv reading and writing functions.
    When reading csv, delimiter can be specified.

    :param dates_filename: Input file with result and dates.
    :param towns_filename: Input file with result and towns.
    :param csv_output_filename: Output CSV-file with result, towns and dates.
    :return: None
    """
    header = ["name", "town", "date"]
    dates = read_csv_file(dates_filename, set_delimiter=":")
    towns = read_csv_file(towns_filename, set_delimiter=":")
    result = [header]
    for date_times in dates:
        result.append([date_times[0], "-", date_times[1]])
    town_was_added = False
    for town in towns:
        for row in result[1:]:
            if town[0] in row:
                row[1] = town[1]
                town_was_added = True
                break
        if town_was_added is False:
            result.append([town[0], town[1], "-"])
    write_csv_file(csv_output_filename, result)


def get_data_type(header, list_of_values: list) -> str:
    """Find the data type for each column."""
    result = None
    for row in list_of_values:
        if row[header] == "-":
            row[header] = None
            continue
        if str(row[header]).isdigit() and (result is None or result == "int"):
            result = "int"
            continue
        else:
            if result != "int":
                try:
                    if datetime.strptime(str(row[header]), "%d.%m.%Y"):
                        result = "date"
                        continue
                except ValueError:
                    return "str"
            return "str"
    return result


def normalize_items(fieldnames: list, data_list: list, change_time_format=False) -> None:
    """Normalize all the items."""
    for name in fieldnames:
        data_type = get_data_type(name, data_list)
        for row in data_list:
            if data_type == 'int':
                if row[name] is None:
                    continue
                else:
                    row[name] = int(str(row[name]))
            else:
                if data_type == 'date':
                    if row[name] is None:
                        continue
                    else:
                        date_object = datetime.strptime(row[name], "%d.%m.%Y")
                        # if change_time_format is True:
                        #     row[name] = date_object.date().strftime("%Y-%m-%d")
                        row[name] = date_object.date()
                else:
                    if row[name] is None or row[name] == "-":
                        row[name] = None
                        continue
                    row[name] = str(row[name])


def read_csv_file_into_list_of_dicts(filename: str, data_types=False, change_time_format=False) -> list:
    """
    Read csv file into list of dictionaries.

    Header line will be used for dict keys.

    Each line after header line will result in a dict inside the result list.
    Every line contains the same number of fields.

    For example:

    name,age,sex
    John,12,M
    Mary,13,F

    Header line will be used as keys for each content line.
    The result:
    [
      {"name": "John", "age": "12", "sex": "M"},
      {"name": "Mary", "age": "13", "sex": "F"},
    ]

    If there are only header or no rows in the CSV-file,
    the result is an empty list.

    The order of the elements in the list should be the same
    as the lines in the file (the first line becomes the first element etc.)

    :param change_time_format:
    :param data_types:
    :param filename: CSV-file to read.
    :return: List of dictionaries where keys are taken from the header.
    """
    data_list = []
    with open(filename, "r") as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=",")
        for rows in csv_reader:
            data_list.append(rows)
        if data_types is True:
            fieldnames = csv_reader.fieldnames
            if fieldnames:
                normalize_items(fieldnames, data_list, change_time_format=True)
            else:
                return []
    return data_list

# print(read_csv_file_into_list_of_dicts("input.csv", True))
def write_list_of_dicts_to_csv_file(filename: str, data: list, not_none=False) -> None:
    """
    Write list of dicts into csv file.

    Data contains a list of dictionaries.
    Dictionary key represents the field.

    Example data:
    [
      {"name": "john", "age": "23"}
      {"name": "mary", "age": "44"}
    ]
    Will become:
    name,age
    john,23
    mary,44

    The order of fields/headers is not important.
    The order of lines is important (the same as in the list).

    Example:
    [
      {"name": "john", "age": "12"},
      {"name": "mary", "town": "London"}
    ]
    Will become:
    name,age,town
    john,12,
    mary,,London

    Fields which are not present in one line will be empty.

    The order of the lines in the file should be the same
    as the order of elements in the list.

    :param not_none:
    :param filename: File to write to.
    :param data: List of dictionaries to write to the file.
    :return: None
    """
    fieldnames = []
    for dictionary in data:
        for key in dictionary.keys():
            if key not in fieldnames:
                fieldnames.append(key)
    data_as_list = []
    for dict_group in data:
        result = []
        for name in fieldnames:
            if name in dict_group:
                if not_none is True and dict_group[name] is None:
                    result.append("-")
                if not_none is True and type(dict_group[name]) is int:
                    result.append(str(dict_group[name]))
                else:
                    result.append(dict_group[name])
            if name not in dict_group:
                if not_none is True:
                    result.append("-")
                else:
                    result.append("")
        data_as_list.append(result)
    for row in data:
        if "birth" in row.keys() and row["birth"] != "-":
            date_object = datetime.strptime(str(row["birth"]), "%Y-%m-%d")
            date_format = date_object.date().strftime("%d.%m.%Y")
            row["birth"] = date_format
        if "death" in row.keys() and row["death"] != "-":
            date_object = datetime.strptime(str(row["death"]), "%Y-%m-%d")
            date_format = date_object.date().strftime("%d.%m.%Y")
            row["death"] = date_format
    if not_none is True:
        with open(filename, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data[:-1])
        with open(filename, "a") as file:
            last_key = list(data[-1].keys())[-1]
            index = 0
            for a in list(data[-1].values()):
                if index < len(list(data[-1].values())) - 1:
                    file.write(str(a) + ",")
                    index += 1
            file.write(str(data[-1][last_key]))
    else:
        with open(filename, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if len(data_as_list) >= 1:
                writer.writeheader()
                writer.writerows(data[:-1])
        if len(data_as_list) >= 1:
            with open(filename, "a") as file:
                for a in data_as_list[-1][:-1]:
                    file.write(str(a) + ",")
                file.write(str(data_as_list[-1][-1]))


# print(write_list_of_dicts_to_csv_file("example_report.csv", [{'name': 'john', 'age': '12'}, {'town': 'London'}, {'age': '16', 'sex': 'F'}, {'name': 'mary', 'sex': 'F'}]))
def read_csv_file_into_list_of_dicts_using_datatypes(filename: str) -> list:
    """
    Read data from file and cast values into different datatypes.

    If a field contains only numbers, turn this into int.
    If a field contains only dates (in format dd.mm.yyyy), turn this into date.
    Otherwise the datatype is string (default by csv reader).

    Example:
    name,age
    john,11
    mary,14

    Becomes ('age' is int):
    [
      {'name': 'john', 'age': 11},
      {'name': 'mary', 'age': 14}
    ]

    But if all the fields cannot be cast to int, the field is left to string.
    Example:
    name,age
    john,11
    mary,14
    ago,unknown

    Becomes ('age' cannot be cast to int because of "ago"):
    [
      {'name': 'john', 'age': '11'},
      {'name': 'mary', 'age': '14'},
      {'name': 'ago', 'age': 'unknown'}
    ]

    Example:
    name,date
    john,01.01.2020
    mary,07.09.2021

    Becomes:
    [
      {'name': 'john', 'date': datetime.date(2020, 1, 1)},
      {'name': 'mary', 'date': datetime.date(2021, 9, 7)},
    ]

    Example:
    name,date
    john,01.01.2020
    mary,late 2021

    Becomes:
    [
      {'name': 'john', 'date': "01.01.2020"},
      {'name': 'mary', 'date': "late 2021"},
    ]

    Value "-" indicates missing value and should be None in the result
    Example:
    name,date
    john,-
    mary,07.09.2021

    Becomes:
    [
      {'name': 'john', 'date': None},
      {'name': 'mary', 'date': datetime.date(2021, 9, 7)},
    ]

    None value also doesn't affect the data type
    (the column will have the type based on the existing values).

    The order of the elements in the list should be the same
    as the lines in the file.

    For date, strptime can be used:
    https://docs.python.org/3/library/datetime.html#examples-of-usage-date
    """
    return read_csv_file_into_list_of_dicts(filename, data_types=True)


def find_ids_and_unique_keys(directory: str) -> dict:
    """Find all id values and unique keys."""
    all_ids = {}
    for file in os.scandir(directory):
        data_as_dict = read_csv_file_into_list_of_dicts(file, True)
        for row in data_as_dict:
            for key, value in row.items():
                all_ids.setdefault(key, []).append(value)
                all_ids.setdefault("all_keys", set()).add(key)
    return all_ids


def status_dead_or_alive(key, value, result_dict) -> None:
    """Check if status is dead or alive."""
    if value is None or value == "":
        result_dict.setdefault(key, "-")
    else:
        result_dict.setdefault(key, value)
    if key == "death" and value is None:
        result_dict.setdefault("status", "alive")


def read_people_data(directory: str, not_none=False, change_time_format=False) -> dict:
    """
    Read people data from files.

    Files are inside directory. Read all *.csv files.

    Each file has an int field "id" which should be used to merge information.

    The result should be one dict where the key is id (int) and value is
    a dict of all the different values across the the files.
    Missing keys should be in every dictionary.
    Missing value is represented as None.

    File: a.csv
    id,name
    1,john
    2,mary
    3,john

    File: births.csv
    id,birth
    1,01.01.2001
    2,05.06.1990

    File: deaths.csv
    id,death
    2,01.02.2020
    1,-

    Becomes:
    {
        1: {"id": 1, "name": "john", "birth": datetime.date(2001, 1, 1), "death": None},
        2: {"id": 2, "name": "mary", "birth": datetime.date(1990, 6, 5),
            "death": datetime.date(2020, 2, 1)},
        3: {"id": 3, "name": "john", "birth": None, "death": None},
    }


    :param change_time_format:
    :param not_none:
    :param directory: Directory where the csv files are.
    :return: Dictionary with id as keys and data dictionaries as values.
    """
    all_ids = find_ids_and_unique_keys(directory)
    all_ids_and_values = list(all_ids.values())[0]
    all_keys = list(all_ids["all_keys"])
    new_dict = {}
    for unique_id in all_ids_and_values:
        result_dict = {}
        for file in os.scandir(directory):
            file_as_dict = read_csv_file_into_list_of_dicts(file, True, change_time_format)
            for dictionary in file_as_dict:
                if dictionary["id"] == unique_id:
                    for key, value in dictionary.items():
                        if not_none is True:
                            status_dead_or_alive(key, value, result_dict)
                        else:
                            result_dict.setdefault(key, value)
        if not_none is True:
            for keys in all_keys:
                if keys not in result_dict:
                    result_dict.setdefault(keys, "-")
                    if keys == "death":
                        result_dict["status"] = "alive"
                if keys in result_dict and keys == "death" and result_dict[keys] != "-":
                    result_dict["status"] = "dead"
                else:
                    continue
        if change_time_format is True:
            result_dict.setdefault("age", "-")
        new_dict[unique_id] = result_dict
    return new_dict


def sort_report(list_of_dicts: list) -> list:
    """Sort keys in the list of dicts."""
    try:
        return sorted(list_of_dicts, key=lambda item: (
            (item.get("age") if item.get("age") != "-" and item.get("age") >= 0 else item.get("age") + 1000),
            (-item.get("birth").year, -item.get("birth").month, -item.get("birth").day),
            (item.get("name") if item.get("name") == "-" else item.get("name")),
            item.get("id")))
    except AttributeError:
        return sorted(list_of_dicts, key=lambda item: (
            (item.get("age") if item.get("age") >= 0 else item.get("age") + 1000),
            (item.get("name") if item.get("name") == "-" else item.get("name")),
            item.get("id")))
    except TypeError:
        return sorted(list_of_dicts, key=lambda item: item["id"])


def generate_people_report(person_data_directory: str, report_filename: str) -> None:
    """
    Generate report about people data.

    Data should be read using read_people_data().

    The input files contain fields "birth" and "death" which are dates. Those can be in different files. There are no duplicate headers in the files (except for the "id").

    The report is a CSV file where all the fields are written to
    (along with the headers).
    In addition, there should be two fields:
    - "status" this is either "dead" or "alive" depending on whether
    there is a death date
    - "age" - current age or the age when dying.
    The age is calculated as full years.
    Birth 01.01.1940, death 01.01.2020 - age: 80
    Birth 02.01.1940, death 01.01.2020 - age: 79

    If there is no birth date, then the age is -1.

    When calculating age, dates can be compared.

    The lines in the files should be ordered:
    - first by the age ascending (younger before older);
      if the age cannot be calculated, then those lines will come last
    - if the age is the same, then those lines should be ordered
      by birthdate descending (newer birth before older birth)
    - if both the age and birth date are the same,
      then by name ascending (a before b). If name is not available, use "" (people with missing name should be before people with  name)
    - if the names are the same or name field is missing,
      order by id ascending.

    Dates in the report should in the format: dd.mm.yyyy
    (2-digit day, 2-digit month, 4-digit year).

    :param person_data_directory: Directory of input data.
    :param report_filename: Output file.
    :return: None
    """
    people_data = read_people_data(person_data_directory, True, change_time_format=True)

    for key, value in people_data.items():
        birth_in_data = False
        for item in list(people_data.values()):
            if "birth" in item:
                birth_in_data = True
                break
        if birth_in_data is True:
            if value["death"] != "-" and value["birth"] != "-":
                birth = datetime.strptime(str(value["birth"]), "%Y-%m-%d")
                death = datetime.strptime(str(value["death"]), "%Y-%m-%d")
                death2 = (death.month, death.day)
                age = death.year - birth.year - 1
                birthday = (birth.month, birth.day)
                if birthday <= death2:
                    age += 1
                value["age"] = age
            if value["birth"] == "-":
                value["age"] = -1
            if value["birth"] != "-" and value["death"] == "-":
                datetime_object = datetime.today()
                birth = datetime.strptime(str(value["birth"]), "%Y-%m-%d")
                current_date = datetime_object.date()
                current_date_tuple = (current_date.year, current_date.month, current_date.day)
                birthday = (birth.year, birth.month, birth.day)
                age = (current_date.year - birth.year - 1)
                if birthday < current_date_tuple:
                    age += 1
                value["age"] = age
    # print(sort_report(list(people_data.values())))
    write_list_of_dicts_to_csv_file(report_filename, sort_report(list(people_data.values())), not_none=True)

# print(generate_people_report("uus", "example_report.csv"))