"""Math."""


def average(a: int, b: int, c: int, d: int) -> float:
    """
    Implement a function that has 4 numeric parameters.

    Each parameter must be multiplied by number of its position in the function (x, y, z = 1, 2, 3).
    Calculate and return the average.

    Examples:
    average(0, 0, 0, 4) === 4
    average(1, 2, 3, 4) == 7.5
    average(5, 0, 5, 1) == 6
    """
    return (a * 1 + b * 2 + c * 3 + d * 4) / 4


def school_pressure(ects: int, weeks: int) -> float:
    """
    Implement a function to know how many hours are needed per week if each ECTS is 26 hours.

    If it's not possible in time then return -1.

    Examples:
    school_pressure(30, 12) == 65
    school_pressure(1, 1) == 26
    school_pressure(1, 0) == -1
    """
    if weeks <= 0 or ects * 26 / weeks > 168:  # There is 168 hours in one week
        return -1
    else:
        return ects * 26 / weeks


def add_fractions(a: int, b: int, c: int, d: int) -> str:
    """
    Implement a function that takes 4 parameters.

    Parameters a and b denote the first fraction like a/b.
    Parameters c and d denote the second fraction like c/d.

    Find and return a fraction in string format that is the sum of a/b and c/d.

    NB! the fraction does not have to be in the simplest form.
    NB! the answer should not contain any commas.

    Examples:
    add_fractions(1, 3, 1, 3) # 1/3 + 1/3 => there are many correct answers like "2/3" and "6/9"
    add_fractions(2, 5, 1, 5) # 2/5 + 1/5 => there are many correct answers like "3/5" and "15/25"
    """
    if b == d:
        # Kui nimetajad on võrdsed
        numerator = a + c  # Lugeja
        denominator = b  # Nimetaja
        return f"{numerator}/{denominator}"
    else:
        # Kui nimetajad ei ole võrdsed
        numerator = a * d + c * b  # Ristkorrutis
        denominator = b * d  # Nimetajad korrutada
        return f"{numerator}/{denominator}"
