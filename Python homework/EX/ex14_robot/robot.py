"""Robot."""


from FollowerBot import FollowerBot


def test_run(robot: FollowerBot):
    """
    Make the robot move, doesn't matter how much, just as long as it has moved from the starting position.

    :param FollowerBot robot: instance of the robot that you need to make move
    """
    robot.set_wheels_speed(30)
    robot.sleep(2)
    robot.set_wheels_speed(0)
    robot.done()


def drive_to_line(robot: FollowerBot):
    """
    Drive the robot until it meets a perpendicular black line, then drive forward 25cm.

    There are 100 pixels in a meter.

    :param FollowerBot robot: instance of the robot that you need to make move
    """
    while True:
        if robot.get_left_line_sensor() == 0 and robot.get_right_line_sensor() == 0:
            for a in range(13):
                robot.set_wheels_speed(15)
                robot.sleep(0.2)
            robot.done()
            break
        else:
            robot.set_wheels_speed(30)
            robot.sleep(0.1)


def follow_the_line(robot: FollowerBot):
    """
    Create a FollowerBot that will follow a black line until the end of that line.

    The robot's starting position will be just short of the start point of the line.

    :param FollowerBot robot: instance of the robot that you need to make move
    """
    while robot.get_left_line_sensor() == 1024 and robot.get_right_line_sensor() == 1024:
        robot.set_wheels_speed(30)
        robot.sleep(0.1)
        if robot.get_left_line_sensor() != 1024 and robot.get_right_line_sensor() != 1024:
            break
    while True:
        if robot.get_left_line_sensor() != 0 and robot.get_right_line_sensor() == 0:
            robot.set_right_wheel_speed(-2)
            robot.set_left_wheel_speed(20)
        elif robot.get_left_line_sensor() == 0 and robot.get_right_line_sensor() != 0:
            robot.set_right_wheel_speed(20)
            robot.set_left_wheel_speed(-2)
        elif robot.get_second_line_sensor_from_right() == 0 or robot.get_third_line_sensor_from_right() == 0:
            robot.set_right_wheel_speed(-17)
            robot.set_left_wheel_speed(12)
        elif robot.get_second_line_sensor_from_left() == 0 and robot.get_left_line_sensor() != 0 and\
                robot.get_right_line_sensor() != 0:
            robot.set_left_wheel_speed(-8)
            robot.set_right_wheel_speed(22)
        elif robot.get_left_line_sensor() == 1024 and robot.get_right_line_sensor() == 1024:
            break
        else:
            robot.set_wheels_speed(80)
        robot.sleep(0.01)
    robot.done()


def robot_move_when_white(robot: FollowerBot):
    """Change moving parameters when white area is encountered."""
    for a in range(13):
        robot.set_right_wheel_speed(-2)
        robot.set_left_wheel_speed(12)
        robot.set_wheels_speed(30)
        robot.sleep(0.01)
    for a in range(30):
        robot.set_wheels_speed(30)
        robot.sleep(0.01)


def robot_move_when_grey(robot: FollowerBot):
    """Turn around when reaching to grey area."""
    for a in range(50):
        robot.set_left_wheel_speed(25)
        robot.sleep(0.01)
    robot.set_right_wheel_speed(-50)
    robot.set_left_wheel_speed(50)
    robot.sleep(3)


def robot_make_sharp_turn(robot: FollowerBot):
    """Make sharp turn to left (90 degrees)."""
    for a in range(44):
        robot.set_wheels_speed(10)
        robot.set_right_wheel_speed(-14)
        robot.set_left_wheel_speed(20)
        robot.sleep(0.05)


def robot_make_another_sharp_turn(robot: FollowerBot):
    """Make second sharp turn to left (90 degrees)."""
    robot.set_left_wheel_speed(-8)
    robot.set_right_wheel_speed(22)


def robot_stay_on_black_line(robot: FollowerBot):
    """Robot should stay away from white area."""
    if robot.get_left_line_sensor() != 0 and robot.get_right_line_sensor() == 0:
        robot.set_right_wheel_speed(-2)
        robot.set_left_wheel_speed(20)
    elif robot.get_left_line_sensor() == 0 and robot.get_right_line_sensor() != 0:
        robot.set_right_wheel_speed(20)
        robot.set_left_wheel_speed(-2)


def robot_stay_on_black_line2(robot: FollowerBot):
    """Robot should stay on the black line."""
    robot.set_right_wheel_speed(-17)
    robot.set_left_wheel_speed(12)


def the_true_follower(robot: FollowerBot):
    """
    Create a FollowerBot that will follow the black line on the track and make it ignore all possible distractions.

    :param FollowerBot robot: instance of the robot that you need to make move
    """
    while True:
        if (robot.get_left_line_sensor() != 0 and robot.get_right_line_sensor() == 0) or\
                (robot.get_left_line_sensor() == 0 and robot.get_right_line_sensor() != 0):
            robot_stay_on_black_line(robot)
        elif robot.get_second_line_sensor_from_right() == 642:
            robot_move_when_grey(robot)
        elif robot.get_second_line_sensor_from_right() == 0 and robot.get_second_line_sensor_from_left() == 0:
            robot.set_wheels_speed(80)
        elif robot.get_second_line_sensor_from_right() == 0 or robot.get_third_line_sensor_from_right() == 0:
            robot_stay_on_black_line2(robot)
        elif robot.get_second_line_sensor_from_left() == 0 and robot.get_left_line_sensor() != 0 and\
                robot.get_right_line_sensor() != 0:
            robot_make_another_sharp_turn(robot)
        elif robot.get_position() == (374, 228):
            robot_make_sharp_turn(robot)
            continue
        elif robot.get_left_line_sensor() == 1024 and robot.get_right_line_sensor() == 1024:
            robot_move_when_white(robot)
        elif robot.get_position() == (264, 299):
            break
        else:
            robot.set_wheels_speed(75)
        robot.sleep(0.01)
    robot.done()


if __name__ == '__main__':
    # follow_the_line - u-shape
    # robot = FollowerBot(track_image="u-shape.png", start_x=122, start_y=254, starting_orientation=90)
    # follow_the_line(robot)

    # follow_the_line - sharp-turn
    # robot = FollowerBot(track_image="track2.png", start_x=354, start_y=365, starting_orientation=90)
    # follow_the_line(robot)

    robot = FollowerBot(track_image="advanced.png", start_x=265, start_y=310, starting_orientation=90, timeout=140)
    the_true_follower(robot)

    # robot = FollowerBot(track_image="line.png", start_x=82, start_y=117, starting_orientation=90)
    # drive_to_line(robot)
    # robot.set_wheels_speed(30)
    # robot.sleep(1)
    # print(robot.get_position())
    # robot.set_wheels_speed(0)
    # robot.done()
