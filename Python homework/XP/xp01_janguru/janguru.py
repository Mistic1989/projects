def meet_me(pos1, jump_distance1, sleep1, pos2, jump_distance2, sleep2) -> int:
    """Calculate the meeting position of 2 jangurus.

    @:param pos1: position of first janguru
    @:param jump_distance1: jump distance of first janguru
    @:param sleep1: sleep time of first janguru
    @:param pos2: position of second janguru
    @:param jump_distance2: jump distance of second janguru
    @:param sleep2: sleep time of second janguru

    @:return positions where jangurus first meet
    """
    pos1 += jump_distance1
    pos2 += jump_distance2
    count_sleep_pos1 = 0
    count_sleep_pos2 = 0
    # speed1 = pos1 // sleep1
    # speed2 = pos2 // sleep2
    # if speed2 > speed1 or speed1 > speed2:
    #     return -1
    i = 0
    while i < 10000000:
        if count_sleep_pos1 != sleep1:  # Check if jangurus are resting
            count_sleep_pos1 += 1
            if pos1 == pos2:
                return pos1
        if count_sleep_pos2 != sleep2:
            count_sleep_pos2 += 1
            if pos1 == pos2:
                return pos1
        if count_sleep_pos1 == sleep1:  # Pos1 making the jump
            pos1 += jump_distance1
            count_sleep_pos1 = 0
        if count_sleep_pos2 == sleep2:  # Pos2 making the jump
            pos2 += jump_distance2
            count_sleep_pos2 = 0
        i += 1


if __name__ == "__main__":
    print(meet_me(1, 2, 1, 2, 1, 1))  # => 3
    print(meet_me(10, 7, 7, 5, 8, 6))  # => 45
    print(meet_me(100, 7, 4, 300, 8, 6))  # => 940
    print(meet_me(1, 7, 1, 15, 5, 1))  #  => 50
    print(meet_me(1, 1, 1, 1, 1, 1))  # => 2
    print(meet_me(1, 1, 1000, 10, 1, 9000))  # => 12
    print(meet_me(1, 1, 1000, 10, 1, 9001))  # => 11
    print(meet_me(1, 2, 3, 4, 5, 5))  # => -1
    print(meet_me(0, 1, 1, 1, 1, 1))  # => -1
    print(meet_me(1, 2, 1, 1, 3, 1))  # => -1
