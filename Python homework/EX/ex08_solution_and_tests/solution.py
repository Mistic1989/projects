"""Solution."""


def students_study(time: int, coffee_needed: bool) -> bool:
    """
    Return True if students study in given circumstances.

    (19, False) -> True
    (1, True) -> False.
    """
    if time in range(18, 25) and coffee_needed is False:
        return True
    if time in range(18, 25) and coffee_needed is True:
        return True
    if time in range(5, 18) and coffee_needed is True:
        return True
    if time in range(5, 18) and coffee_needed is False:
        return False
    if time in range(1, 5) and coffee_needed is True:
        return False
    if time in range(1, 5) and coffee_needed is False:
        return False


def lottery(a: int, b: int, c: int) -> int:
    """
    Return Lottery victory result 10, 5, 1, or 0 according to input values.

    (5, 5, 5) -> 10
    (2, 2, 1) -> 0
    (2, 3, 1) -> 1
    """
    if a == 5 and b == 5 and c == 5:
        return 10
    if a == b and a == c:
        return 5
    if b != a and c != a:
        return 1
    if a == b or a == c:
        return 0


def fruit_order(small_baskets: int, big_baskets: int, ordered_amount: int) -> int:
    """
    Return number of small fruit baskets if it's possible to finish the order, otherwise return -1.

    (4, 1, 9) -> 4
    (3, 1, 10) -> -1
    """
    if ordered_amount == 0 or ordered_amount - (big_baskets * 5) == 0:
        return 0
    if ordered_amount > (big_baskets * 5):
        if small_baskets > (ordered_amount - (big_baskets * 5)):
            return small_baskets - (small_baskets % (ordered_amount - (big_baskets * 5)))
        if small_baskets == (ordered_amount - (big_baskets * 5)):
            return small_baskets
    if ordered_amount < (big_baskets * 5):
        if small_baskets == 0:
            if ((big_baskets * 5) % ordered_amount) > 0:
                if ((big_baskets * 5) % ordered_amount) == 5:
                    return 0
                else:
                    return -1
        if small_baskets != 0 and small_baskets >= (ordered_amount % 5):
            return ordered_amount % 5
        return -1
    else:
        return -1
