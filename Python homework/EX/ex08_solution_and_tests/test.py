"""Tests for solution."""


from solution import students_study
from solution import lottery
from solution import fruit_order


def test_students_study_evening_coffee():
    """Test students study.

    In the evening coffee is not necessary.
    """
    assert students_study(20, True) is True
    assert students_study(20, False) is True


def test_students_study_night_coffee():
    """
    Test students study.

    At night student should sleep.
    """
    assert students_study(2, True) is False
    assert students_study(2, False) is False


def test_students_study_day_time_coffee():
    """
    Test students study.

    Coffee is important on day time.
    """
    assert students_study(10, True) is True
    assert students_study(10, False) is False


def test_students_study_evening_coffee_edge_case():
    """
    Test students study.

    In the evening coffee is not necessary.
    Testing 18:00 and 24:00
    """
    assert students_study(24, True) is True
    assert students_study(24, False) is True
    assert students_study(18, True) is True
    assert students_study(18, False) is True


def test_students_study_night_coffee_edge_case():
    """
    Test students study.

    At night student should sleep.
    Testing 01:00 and 04:00
    """
    assert students_study(1, True) is False
    assert students_study(1, False) is False
    assert students_study(4, True) is False
    assert students_study(4, False) is False


def test_students_study_day_time_coffee_edge_case():
    """
    Test students study.

    Coffee is important on day time.
    Testing 05:00 and 17:00
    """
    assert students_study(5, True) is True
    assert students_study(5, False) is False
    assert students_study(17, True) is True
    assert students_study(17, False) is False


def test_lottery_all_fives():
    """Test lottery only fives."""
    assert lottery(5, 5, 5) == 10


def test_lottery_all_same_positive():
    """Test lottery all same positive numbers."""
    assert lottery(3, 3, 3) == 5


def test_lottery_all_diff():
    """Test lottery all different numbers."""
    assert lottery(1, 2, 3) == 1


def test_lottery_a_b_same_c_diff():
    """Test lottery a and b are same but c is different."""
    assert lottery(2, 2, 1) == 0


def test_lottery_all_same_negative():
    """Test lottery all same negative numbers."""
    assert lottery(-3, -3, -3) == 5


def test_lottery_all_same_zero():
    """Test lottery all zeros."""
    assert lottery(0, 0, 0) == 5


def test_lottery_a_c_same_b_diff():
    """Test lottery a and c are same but b is different."""
    assert lottery(2, 1, 2) == 0


def test_lottery_b_c_same_a_diff():
    """Test lottery b and c are same but a is different."""
    assert lottery(1, 2, 2) == 1


def test_fruit_order_all_zero():
    """Test fruit order all zeros."""
    assert fruit_order(0, 0, 0) == 0


def test_fruit_order_zero_amount_zero_small():
    """Test fruit order, small buckets and order quantity zero."""
    assert fruit_order(0, 2, 0) == 0


def test_fruit_order_zero_amount_zero_big():
    """Test fruit order, big buckets and order quantity zero."""
    assert fruit_order(2, 0, 0) == 0


def test_fruit_order_zero_amount_others_not_zero():
    """Test fruit order, order quantity zero, others not."""
    assert fruit_order(3, 2, 0) == 0


def test_fruit_order_only_big_exact_match():
    """Test fruit order, small buckets zero, big buckets have exact match."""
    assert fruit_order(0, 2, 10) == 0


def test_fruit_order_only_big_not_enough():
    """Test fruit order, small buckets zero, not enough big buckets."""
    assert fruit_order(0, 2, 11) == -1


def test_fruit_order_only_big_not_enough_but_multiple_fives():
    """
    Test fruit order.

    No small buckets but not enough big buckets.
    Using only multiple fives.
    """
    assert fruit_order(0, 5, 30) == -1


def test_fruit_order_only_small_match_more_than_5_smalls():
    """Test fruit order.

    No big buckets.
    Small buckets match with more than 5 smalls.
    """
    assert fruit_order(6, 0, 6) == 6


def test_fruit_order_small_and_big_exact_match():
    """Test fruit order.

    Exactly enough big and small buckets.
    """
    assert fruit_order(1, 1, 6) == 1


def test_fruit_order_only_small_not_enough_more_than_5_smalls():
    """Test fruit order.

    No big buckets.
    Order quantity is larger than small buckets.
    More than 5 small buckets.
    """
    assert fruit_order(6, 0, 7) == -1


def test_fruit_order_only_small_not_enough():
    """Test fruit order.

    No big buckets.
    Order quantity is larger than small buckets.
    Testing with numbers less than 5.
    """
    assert fruit_order(3, 0, 4) == -1


def test_fruit_order_only_small_more_than_required():
    """Test fruit order.

    No big buckets.
    Order quantity is smaller than small buckets.
    """
    assert fruit_order(4, 0, 3) == 3


def test_fruit_order_match_with_more_than_5_smalls():
    """Test fruit order.

    Match with more than 5 small buckets.
    """
    assert fruit_order(7, 1, 11) == 6


def test_fruit_order_use_all_smalls_some_bigs():
    """Test fruit order.

    Use some of big buckets and all the small buckets.
    """
    assert fruit_order(1, 6, 21) == 1


def test_fruit_order_use_some_smalls_all_bigs():
    """Test fruit order.

    Use all the big buckets and some of small buckets.
    """
    assert fruit_order(7, 3, 21) == 6


def test_fruit_order_use_some_smalls_some_bigs():
    """Test fruit order.

    Use some small and big buckets.
    """
    assert fruit_order(7, 5, 21) == 1


def test_fruit_order_not_enough():
    """Test fruit order.

    Not enough small and big buckets.
    """
    assert fruit_order(2, 1, 15) == -1


def test_fruit_order_enough_bigs_not_enough_smalls():
    """Test fruit order.

    Enough big buckets but not enough small buckets.
    """
    assert fruit_order(2, 3, 13) == -1


def test_fruit_order_not_enough_with_more_than_5_smalls():
    """Test fruit order.

    Having more than 5 small buckets, there is not enough buckets.
    """
    assert fruit_order(6, 2, 17) == -1


def test_fruit_order_only_big_more_than_required_match():
    """Test fruit order.

    No small buckets.
    More big buckets than required.
    """
    assert fruit_order(0, 3, 10) == 0


def test_fruit_order_only_big_more_than_required_no_match():
    """Test fruit order.

    No small buckets.
    Big buckets more than required but no match.
    """
    assert fruit_order(0, 4, 11) == -1


def test_fruit_order_enough_bigs_not_enough_smalls_large_numbers():
    """Test fruit order.

    Enough big buckets, not enough small buckets.
    Testing with large numbers.
    """
    assert fruit_order(1, 159251, 500002) == -1


def test_fruit_order_match_large_numbers():
    """Test fruit order.

    Match with small and big buckets.
    Using large numbers.
    """
    assert fruit_order(796255, 159251, 1592510) == 796255
