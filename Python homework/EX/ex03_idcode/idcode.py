"""EX03 ID code."""


def find_id_code(text: str) -> str:
    """
    Find ID-code from given text.

    Given string may include any number of numbers, characters and other symbols mixed together.
    The numbers of ID-code may be between other symbols - they must be found and concatenated.
    ID-code contains of exactly 11 numbers. If there are not enough numbers, return 'Not enough numbers!',
    if there are too many numbers, return 'Too many numbers!' If ID-code can be found, return that code.
    You don't have to validate the ID-code here. If it has 11 numbers, then it is enough for now.

    :param text: string
    :return: string
    """
    numbers = ""

    for char in text:
        if char.isdigit():
            numbers += char
    if len(numbers) < 11:
        return "Not enough numbers!"
    elif len(numbers) > 11:
        return "Too many numbers!"
    return numbers


def the_first_control_number_algorithm(text: str) -> str:
    """
    Check if given value is correct for control number in ID code only with the first algorithm.

    The first algorithm can be calculated with ID code's first 10 numbers.
    Each number must be multiplied with its corresponding digit
    (in this task, corresponding digits are: 1 2 3 4 5 6 7 8 9 1), after which all the values are summarized
    and divided by 11. The remainder of calculation should be the control number.

    If the remainder is less than 10 and equal to the last number of ID code,
    then that's the correct control number and the function should return the ID code.
    Otherwise, the control number is either incorrect or the second algorithm should be used.
    In this case, return "Needs the second algorithm!".

    If the string contains more or less than 11 numbers, return "Incorrect ID code!".
    In other case use the previous algorithm to get the code number out of the string
    and find out, whether its control number is correct.

    :param text: string
    :return: string
    """
    id_code = ""
    first_degree_weight = 0

    for char in text:
        if char.isdigit():
            id_code += char
    if len(id_code) < 11 or len(id_code) > 11:
        return "Incorrect ID code!"
    elif len(id_code) > 11:
        return "Incorrect ID code!"

    for number in range(10):
        if number == 9:
            first_degree_weight += int(id_code[number]) * 1
        else:
            first_degree_weight += int(id_code[number]) * (number + 1)

    first_degree_weight = int(first_degree_weight % 11)

    if first_degree_weight < 10 and first_degree_weight == int(id_code[-1]):
        return id_code
    elif first_degree_weight >= 10:
        return "Needs the second algorithm!"
    return "Incorrect ID code!"


def is_valid_gender_number(first_number: int) -> bool:
    """Check if given value is correct gender number."""
    if first_number in range(1, 7):
        return True
    return False


def get_gender(first_number: int) -> str:
    """Check if given value's gender is male or female."""
    if first_number % 2 != 0 and first_number in range(1, 7):
        return "male"
    elif first_number % 2 == 0 and first_number in range(1, 7):
        return "female"


def is_valid_year_number(year_number: int) -> bool:
    """Check if given value is correct for year number in ID code."""
    if year_number in range(0, 100):
        return True
    return False


def is_valid_month_number(month_number: int) -> bool:
    """Check if given value is correct for month number in ID code."""
    if month_number in range(1, 13):
        return True
    return False


def is_valid_birth_number(birth_number: int) -> bool:
    """Check if given value is correct for birth number in ID code."""
    if birth_number in range(1, 1000):
        return True
    return False


def is_leap_year(year_number: int) -> bool:
    """Check if given value is leap year or not."""
    if year_number % 400 == 0 or (year_number % 4 == 0 and year_number % 100 != 0):
        return True
    return False


def get_full_year(gender_number: int, year_number: int) -> int:
    """Define the 4-digit year when given person was born."""
    full_year = ""
    if gender_number in range(1, 3):
        full_year += "18"
    elif gender_number in range(3, 5):
        full_year += "19"
    elif gender_number in range(5, 7):
        full_year += "20"

    if year_number in range(0, 10):
        return int(full_year + "0" + str(year_number))
    else:
        return int(full_year + str(year_number))


def get_birth_place(birth_number: int) -> str:
    """Find the place where the person was born."""
    if is_valid_birth_number(birth_number):
        if birth_number in range(1, 11):
            return "Kuressaare"
        elif birth_number in range(11, 21) or birth_number in range(271, 371):
            return "Tartu"
        elif birth_number in range(21, 221) or birth_number in range(471, 711):
            return "Tallinn"
        elif birth_number in range(221, 271):
            return "Kohtla-Järve"
        elif birth_number in range(371, 421):
            return "Narva"
        elif birth_number in range(421, 471):
            return "Pärnu"
        elif birth_number in range(711, 1000):
            return "undefined"
    else:
        return "Wrong input!"


def is_valid_control_number(id_code: str) -> bool:
    """Check if given value is correct for control number in ID code."""
    second_degree_weight = 0
    first_control_result = the_first_control_number_algorithm(id_code)

    if id_code.isdigit() and len(id_code) == 11:
        if first_control_result == id_code:
            return True

        if first_control_result == "Needs the second algorithm!":
            for number in range(len(id_code)):
                if number > 6:
                    second_degree_weight += int(id_code[number]) * (number - 6)
                else:
                    second_degree_weight += int(id_code[number]) * (number + 3)
            second_degree_weight = second_degree_weight % 11
            if second_degree_weight < 10:
                return True
            elif second_degree_weight >= 10 and int(id_code[-1]) == 0:
                return True
    return False


def is_valid_day_number(gender_number: int, year_number: int, month_number: int, day_number: int) -> bool:
    """Check if given value is correct for day number in ID code."""
    month_length_is_31 = [1, 3, 5, 7, 8, 10, 12]
    month_length_is_30 = [4, 6, 9, 11]

    if month_number in month_length_is_31 and day_number in range(1, 32):
        for month in month_length_is_31:
            if month == month_number:
                return True
    if month_number in month_length_is_30 and day_number in range(1, 31):
        for month in month_length_is_30:
            if month == month_number:
                return True
    elif is_leap_year(get_full_year(gender_number, year_number)) and month_number == 2 and day_number in range(1, 30):
        return True
    elif month_number == 2 and day_number in range(1, 29):
        return True
    return False


def is_id_valid(id_code: str) -> bool:
    """Check if given ID code is valid and return the result (True or False)."""
    if id_code.isdigit() and len(id_code) == 11:
        if is_valid_gender_number(int(id_code[0])) and \
           is_valid_year_number(int(id_code[1:3])) and \
           is_valid_month_number(int(id_code[3:5])) and \
           is_valid_birth_number(int(id_code[7:10])) and \
           is_valid_control_number(id_code) and \
           is_valid_day_number(int(id_code[0]), int(id_code[1:3]),
                               int(id_code[3:5]), int(id_code[5:7])):
            return True
    return False


def get_data_from_id(id_code: str) -> str:
    """Get possible information about the person."""
    if is_id_valid(id_code):
        return f"This is a " \
               f"{get_gender(int(id_code[0]))} " \
               f"born on " \
               f"{id_code[5:7]}.{id_code[3:5]}." \
               f"{get_full_year(int(id_code[0]), int(id_code[1:3]))} " \
               f"in " \
               f"{get_birth_place(int(id_code[7:10]))}."
    return "Given invalid ID code!"


if __name__ == '__main__':
    print("\nFind ID code:")
    print(find_id_code(""))  # -> "Not enough numbers!"
    print(find_id_code("123456789123456789"))  # -> "Too many numbers!"
    print(find_id_code("ID code is: 49403136526"))  # -> "49403136526"
    print(find_id_code("efs4  9   #4aw0h 3r 1a36g5j2!!6-"))  # -> "49403136526"

    print(the_first_control_number_algorithm(""))  # -> "Incorrect ID code!"
    print(the_first_control_number_algorithm("123456789123456789"))  # -> "Incorrect ID code!"
    print(the_first_control_number_algorithm("ID code is: 49403136526"))  # -> "49403136526"
    print(the_first_control_number_algorithm("efs4  9   #4aw0h 3r 1a36g5j2!!6-"))  # -> "49403136526"
    print(the_first_control_number_algorithm("50412057633"))  # -> "50412057633"
    print(the_first_control_number_algorithm("Peeter's ID is euf50weird2fs0fsk51ef6t0s2yr7fyf4"))  # -> "Needs
    # the second algorithm!"
    print("\nGender number:")
    for i in range(9):
        print(f"{i} {is_valid_gender_number(i)}")
        # 0 -> False
        # 1...6 -> True
        # 7...8 -> False

    print("\nGet gender:")
    print(get_gender(2))  # -> "female"
    print(get_gender(5))  # -> "male"

    print("\nYear number:")
    print(is_valid_year_number(100))  # -> False
    print(is_valid_year_number(50))  # -> True

    print("\nMonth number:")
    print(is_valid_month_number(2))  # -> True
    print(is_valid_month_number(15))  # -> False

    print("\nBorn order number:")
    print(is_valid_birth_number(0))  # -> False
    print(is_valid_birth_number(1))  # -> True
    print(is_valid_birth_number(850))  # -> True

    print("\nLeap year:")
    print(is_leap_year(1804))  # -> True
    print(is_leap_year(1800))  # -> False

    print("\nGet full year:")
    print(get_full_year(1, 28))  # -> 1828
    print(get_full_year(4, 85))  # -> 1985
    print(get_full_year(5, 1))  # -> 2001

    print("\nChecking where the person was born")
    print(get_birth_place(0))  # -> "Wrong input!"
    print(get_birth_place(1))  # -> "Kuressaare"
    print(get_birth_place(273))  # -> "Tartu"
    print(get_birth_place(220))  # -> "Tallinn"

    print("\nControl number:")
    print(is_valid_control_number("49808270244"))  # -> True
    print(is_valid_control_number("60109200187"))  # -> False, it must be 6

    print("\nDay number:")
    print(is_valid_day_number(4, 5, 12, 25))  # -> True
    print(is_valid_day_number(3, 10, 8, 32))  # -> False
    print("\nFebruary check:")
    print(
        is_valid_day_number(4, 96, 2, 30))  # -> False (February cannot contain more than 29 days in any circumstances)
    print(is_valid_day_number(4, 99, 2, 29))  # -> False (February contains 29 days only during leap year)
    print(is_valid_day_number(4, 8, 2, 29))  # -> True
    print("\nMonth contains 30 or 31 days check:")
    print(is_valid_day_number(4, 22, 4, 31))  # -> False (April contains max 30 days)
    print(is_valid_day_number(4, 18, 10, 31))  # -> True
    print(is_valid_day_number(4, 15, 9, 31))  # -> False (September contains max 30 days)

    print("\nOverall ID check::")
    print(is_id_valid("49808270244"))  # -> True
    print(is_id_valid("12345678901"))  # -> False

    print("\nFull message:")
    print(get_data_from_id("49808270244"))  # -> "This is a female born on 27.08.1998 in Tallinn."
    print(get_data_from_id("60109200187"))  # -> "Given invalid ID code!"

    print("\nTest now your own ID code:")
    personal_id = input()  # type your own id in command prompt
    print(is_id_valid(personal_id))  # -> True
