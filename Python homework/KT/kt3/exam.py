"""KT3."""


def last_to_first(s):
    """
    Move last symbol to the beginning of the string.

    last_to_first("ab") => "ba"
    last_to_first("") => ""
    last_to_first("hello") => "ohell"
    """
    if len(s) > 0:
        return s[-1] + s[:-1]
    else:
        return ""


def only_one_pair(numbers: list) -> bool:
    """
    Whether the list only has one pair.

    Function returns True, if the list only has one pair (two elements have the same value).
    In other cases:
     there are no elements with the same value
     there are more than 2 elements with the same value
     there are several pairs
    returns False.

    only_one_pair([1, 2, 3]) => False
    only_one_pair([1]) => False
    only_one_pair([1, 2, 3, 1]) => True
    only_one_pair([1, 2, 1, 3, 1]) => False
    only_one_pair([1, 2, 1, 3, 1, 2]) => False
    """
    if len(set(numbers)) == len(numbers) - 1:
        return True
    else:
        return False


def pentabonacci(n: int) -> int:
    """
    Find the total number of odd values in the sequence up to the f(n) [included].

    The sequence is defined like this:
    f(0) = 0
    f(1) = 1
    f(2) = 1
    f(3) = 2
    f(4) = 4
    f(n) = f(n - 1) + f(n - 2) + f(n - 3) + f(n - 4) + f(n - 5)

    Keep in mind that 1 is the only value that is duplicated in the sequence
    and must be counted only once.

    pentabonacci(5) -> 1
    pentabonacci(10) -> 3
    pentabonacci(15) -> 5

    :param n: The last term to take into account.
    :return: Total number of odd values.
    """
    sequence = [0, 1, 1, 2, 4]
    if n < 1:
        return 0
    count = 1
    for number in range(5, n + 1):
        if sum(sequence[-5:]) % 2 == 1:
            count += 1
        sequence.append(sum(sequence[-5:]))
    return count


def swap_dict_keys_and_value_lists(d: dict) -> dict:
    """
    Swap keys and values in dict.

    Values are lists.
    Every element in this list should be a key,
    and current key will be a value for the new key.
    Values in the result are lists.

    Every list in input dict has at least 1 element.
    The order of the values in the result dict is not important.

    swap_dict_keys_and_value_lists({"a": ["b", "c"]}) => {"b": ["a"], "c": ["a"]}
    swap_dict_keys_and_value_lists({1: [2, 3], 4: [2, 5]}) => {2: [1, 4], 3: [1], 5: [4]}
    swap_dict_keys_and_value_lists({}) => {}
    swap_dict_keys_and_value_lists({1: [2]}) => {2: [1]}
    """
    new_dict = {}
    for key, value in d.items():
        for val in value:
            new_dict.setdefault(val, []).append(key)
    return new_dict


if __name__ == '__main__':
    print(last_to_first("ab"))
    print(last_to_first(""))
    print(last_to_first("hello"))

    print(only_one_pair([1, 2, 3]))
    print(only_one_pair([1]))
    print(only_one_pair([1, 2, 3, 1]))
    print(only_one_pair([1, 2, 1, 3, 1]))
    print(only_one_pair([1, 2, 1, 3, 1, 2]))

    print(pentabonacci(5))
    print(pentabonacci(10))
    print(pentabonacci(15))

    print(swap_dict_keys_and_value_lists({"a": ["b", "c"]}))
    print(swap_dict_keys_and_value_lists({1: [2, 3], 4: [2, 5]}))
    print(swap_dict_keys_and_value_lists({}))
    print(swap_dict_keys_and_value_lists({1: [2]}))
