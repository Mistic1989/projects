"""Regex, I think."""
import re


class Entry:
    """Entry class."""

    def __init__(self, first_name: str, last_name: str, id_code: str, phone_number: str, date_of_birth: str,
                 address: str):
        """Init."""
        self.first_name = first_name
        self.last_name = last_name
        self.id_code = id_code
        self.phone_number = phone_number
        self.date_of_birth = date_of_birth
        self.address = address

    def format_date(self):
        """
        Return the date in the following format: 'Day: {day}, Month: {month}, Year: {year}'.

        Just for fun, no points gained or lost from this.

        Example: 'Day: 06, Month: 11, Year: 1995'
        If the object doesn't have date of birth given, return None.
        :return:
        """
        if self.date_of_birth:
            return f'Day: {self.date_of_birth[0:2]}, Month: {self.date_of_birth[3:5]}, Year: {self.date_of_birth[6:10]}'

    def __repr__(self) -> str:
        """
        Object representation.

        This method makes printing the object actually readable in the console.
        This method is perfect. It's not necessary to edit.
        """
        return f"Name: {self.first_name} {self.last_name}\n" \
               f"ID code: {self.id_code}\n" \
               f"Phone number: {self.phone_number}\n" \
               f"Date of birth: {self.format_date()}\n" \
               f"Address: {self.address}"

    def __eq__(self, other) -> bool:
        """
        Compare two Entry objects.

        This method assists in comparing two different objects.
        This method is perfect. Don't touch it.
        """
        return self.first_name == other.first_name and self.last_name == other.last_name and \
            self.id_code == other.id_code and self.phone_number == other.phone_number and \
            self.date_of_birth == other.date_of_birth and self.address == other.address


def parse(row: str) -> Entry:
    """
    Parse data from input string.

    :param row: String representation of the data.
    :return: Entry object with filled values
    """
    pattern = r'([A-ZÕÄÖÜ][a-zõäöü]+)?([A-ZÕÄÖÜ][a-zõäöü]+)?' \
              r'((?<!\d)\d{11})((?:[\+]\d{3})*\s*(?:\d{7,8})?)(\d{2}\-\d{2}\-\d{4})?(.*)'
    result = re.findall(pattern, row)
    final_result = []
    for match in result[0]:
        if match == "":
            final_result.append(None)
        else:
            final_result.append(match)
    return Entry(final_result[0], final_result[1], final_result[2], final_result[3],
                 final_result[4], final_result[5])
