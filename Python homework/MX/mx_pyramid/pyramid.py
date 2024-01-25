"""Program that creates beautiful pyramids."""


def make_pyramid(base: int, char: str) -> list:
    """
    Construct a pyramid with given base.

    Pyramid should consist of given chars, all empty spaces in the pyramid list are ' '. Pyramid height depends on base length. Lowest floor consists of base-number chars.
    Every floor has 2 chars less than the floor lower to it.
    make_pyramid(3, "A") ->
    [
        [' ', 'A', ' '],
        ['A', 'A', 'A']
    ]
    make_pyramid(6, 'a') ->
    [
        [' ', ' ', 'a', 'a', ' ', ' '],
        [' ', 'a', 'a', 'a', 'a', ' '],
        ['a', 'a', 'a', 'a', 'a', 'a']
    ]
    :param base: int
    :param char: str
    :return: list
    """
    height = [((base - (base % 2)) // 2) if base % 2 == 0 else ((base // 2) + (base % 2)) for i in range(1)][0]
    table = [[" " for x in range(base)] for i in range(height)]
    fill_tabel = [[char if a in range(x + 1, base - x - 1) else " " for a in range(base)] for x in
                  range(len(table) - 1)]
    return fill_tabel[::-1] + [[char] * base]


def join_pyramids(pyramid_a: list, pyramid_b: list) -> list:
    """
    Join together two pyramid lists.

    Get 2 pyramid lists as inputs. Join them together horizontally. If the pyramid heights are not equal, add empty lines on the top until they are equal.
    join_pyramids(make_pyramid(3, "A"), make_pyramid(6, 'a')) ->
    [
        [' ', ' ', ' ', ' ', ' ', 'a', 'a', ' ', ' '],
        [' ', 'A', ' ', ' ', 'a', 'a', 'a', 'a', ' '],
        ['A', 'A', 'A', 'a', 'a', 'a', 'a', 'a', 'a']
    ]

    :param pyramid_a: list
    :param pyramid_b: list
    :return: list
    """
    lowest = min([pyramid_a, pyramid_b], key=lambda x: len(x))
    highest = max([pyramid_a, pyramid_b], key=lambda x: len(x))
    # lowest = pyramid_a
    # highest = pyramid_b
    # if len(lowest) != len(highest):
    #     lowest = [sorted([pyramid_a, pyramid_b], key=lambda x: len(x))][0][0]
    #     highest = [sorted([pyramid_a, pyramid_b], key=lambda x: len(x))][-1][-1]
    # return [lowest[::-1][index] + x if index < len(lowest) else [" "] * len(lowest[0]) + x
    #         for index, x in enumerate(highest[::-1])][::-1]
    return [pyramid_a[::-1][index] + pyramid_b[::-1][index] if index < len(pyramid_a) and index < len(pyramid_b) else [" "] * len(lowest[0]) + highest[index]
            for index in range(len(highest))][::-1]


def to_string(pyramid: list) -> str:
    """
    Return pyramid list as a single string.

    Join pyramid list together into a string and return it.
    to_string(make_pyramid(3, 'A')) ->
    '''
     A
    AAA
    '''

    :param pyramid: list
    :return: str
    """
    pass


if __name__ == '__main__':
    pyramid_a = make_pyramid(3, "A")
    # print(pyramid_a)  # ->
    # """
    # [
    #     [' ', 'A', ' '],
    #     ['A', 'A', 'A']
    # ]
    # """

    pyramid_b = make_pyramid(9, 'a')
    # print(pyramid_b)  # ->
    # """
    # [
    #     [' ', ' ', 'a', 'a', ' ', ' '],
    #     [' ', 'a', 'a', 'a', 'a', ' '],
    #     ['a', 'a', 'a', 'a', 'a', 'a']
    # ]
    # """

    # joined = join_pyramids(pyramid_a, pyramid_b)
    # print(joined)  # ->
    print(join_pyramids(make_pyramid(6, 'a'), make_pyramid(12, "g")))
    """
    [
        [' ', ' ', ' ', ' ', ' ', 'a', 'a', ' ', ' '],
        [' ', 'A', ' ', ' ', 'a', 'a', 'a', 'a', ' '],
        ['A', 'A', 'A', 'a', 'a', 'a', 'a', 'a', 'a']
    ]
    """

    # pyramid_string = to_string(joined)
    # print(pyramid_string)  # ->
    # """
    #      aa
    #  A  aaaa
    # AAAaaaaaa
    # """
