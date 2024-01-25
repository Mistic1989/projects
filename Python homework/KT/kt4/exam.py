"""KT4."""


def two_digits_into_list(nr: int) -> list:
    """
    Return list of digits of 2-digit number.

    two_digits_into_list(11) => [1, 1]
    two_digits_into_list(71) => [7, 1]

    :param nr: 2-digit number
    :return: list of length 2
    """
    return [int(str(nr)[0]), int(str(nr)[1])]


def sum_elements_around_last_three(nums: list) -> int:
    """
    Find sum of elements before and after last 3 in the list.

    If there is no 3 in the list or list is too short
    or there is no element before or after last 3 return 0.

    Note if 3 is last element in the list you must return
    sum of elements before and after 3 which is before last.


    sum_elements_around_last_three([1, 3, 7]) -> 8
    sum_elements_around_last_three([1, 2, 3, 4, 6, 4, 3, 4, 5, 3, 4, 5, 6]) -> 9
    sum_elements_around_last_three([1, 2, 3, 4, 6, 4, 3, 4, 5, 3, 3, 2, 3]) -> 5
    sum_elements_around_last_three([1, 2, 3]) -> 0

    :param nums: given list of ints
    :return: sum of elements before and after last 3
    """
    if 3 not in nums:
        return 0
    if len(nums) < 3:
        return 0
    for i in range(len(nums[::-1])):
        if nums[::-1][i] == 3 and len(nums) > 2:
            if nums[::-1][i] == 3 and i == 0:
                continue
            if nums[::-1][i] == 3:
                if len(nums) == i + 1:
                    return 0
                return nums[::-1][i - 1] + nums[::-1][i + 1]
    return 0


# print(sum_elements_around_last_three([3, 4, 3]))


def max_block(s: str) -> int:
    """
    Given a string, return the length of the largest "block" in the string.

    A block is a run of adjacent chars that are the same.

    max_block("hoopla") => 2
    max_block("abbCCCddBBBxx") => 3
    max_block("") => 0
    """
    best = 0
    for start in range(len(s)):
        for end in range(start, len(s)):
            subs = s[start:end + 1]
            if len(set(subs)) == 1:
                if len(subs) > best:
                    best = len(subs)
    return best


# print(max_block("abbCCCddBBBxx"))


def create_dictionary_from_directed_string_pairs(pairs: list) -> dict:
    """
    Create dictionary from directed string pairs.

    One pair consists of two strings and "direction" symbol ("<" or ">").
    The key is the string which is on the "larger" side,
    the value is the string which is on the "smaller" side.

    For example:
    ab>cd => "ab" is the key, "cd" is the value
    kl<mn => "mn" is the key, "kl" is the value

    The input consists of list of such strings.
    The output is a dictionary, where values are lists.
    Each key cannot contain duplicate elements.
    The order of the elements in the values should be
    the same as they appear in the input list.

    create_dictionary_from_directed_string_pairs([]) => {}

    create_dictionary_from_directed_string_pairs(["a>b", "a>c"]) =>
    {"a": ["b", "c"]}

    create_dictionary_from_directed_string_pairs(["a>b", "a<b"]) =>
    {"a": ["b"], "b": ["a"]}

    create_dictionary_from_directed_string_pairs(["1>1", "1>2", "1>1"]) =>
    {"1": ["1", "2"]}
    """
    result = {}
    for i in pairs:
        if ">" in i:
            splitted = i.split(">")
            if splitted[0] not in result:
                result[splitted[0]] = []
            if splitted[1] not in result[splitted[0]]:
                result.setdefault(splitted[0], []).append(splitted[1])
        if "<" in i:
            splitted2 = i.split("<")
            if splitted2[1] not in result:
                result[splitted2[1]] = []
            if splitted2[0] not in result[splitted2[1]]:
                result.setdefault(splitted2[1], []).append(splitted2[0])
    return result


# print(create_dictionary_from_directed_string_pairs(["a>b", "a>c"]))