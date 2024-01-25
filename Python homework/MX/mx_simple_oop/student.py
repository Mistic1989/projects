"""Simple OOP exercise."""


class Student:
    """Student class."""

    def __init__(self, name, finished=False):
        """
        Class constructor.

        :param name:
        :param finished:
        """
        self.name = name
        self.finished = finished
