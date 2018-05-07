import math

# ANGLE_SMALL = "angle_small"

def muy_angle_small(arg) :
    if arg <= 7 :
        return 1
    elif arg >7 :
        return (14 - arg) / 7


def muy_angle_medium(arg) :
    if arg <= 12 :
        return (arg -7) / 5
    elif arg <=16 and arg >=12 :
        return 1
    elif arg > 16 :
        return (21-arg) / 5

def muy_angle_big(arg) :
    if arg < 21 :
        return (arg - 14)/7
    elif arg >= 21 :
        return 1


# DISTANCE_NEAR = "dis_near"


def muy_angle_near(arg) :
    if arg <= 50 :
        return 1
    elif arg > 50 :
        return (150 - arg) / 50


def muy_angle_medium(arg) :
    if arg < 80 :
        return (arg -7) / 5
    elif arg <=16 and arg >=12 :
        return 1
    elif arg > 16 :
        return (21-arg) / 5

def muy_angle_far(arg) :
    if arg < 21 :
        return (arg - 14)/7
    elif arg >= 21 :
        return 1