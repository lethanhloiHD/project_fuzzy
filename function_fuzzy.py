

#TRAFFIC

def red(arg) :
    if arg <= 4 :
        return 1.0
    elif arg > 4 :
        return (6 - arg) / 2


def very_red(arg) :
    if arg < 6 :
        return (arg-4) / 2
    elif arg  >= 6 :
        return 1.0


def green(arg) :
    if arg <= 4 :
        return 1.0
    elif arg > 4 :
        return (6 - arg) / 2


def very_green(arg) :
    if arg < 6 :
        return (arg - 4) / 2
    elif arg  >= 6 :
        return 1.0


# DISTANCE_TRAFFIC


def traffic_near(arg) :
    if arg <= 80 :
        return 1.0
    elif arg > 80 :
        return (140 - arg) / 60


def traffic_medium(arg) :
    if arg < 140 :
        return (arg -80) / 60
    elif arg <= 170 and arg >= 140 :
        return 1.0
    elif arg > 170 :
        return (170 - arg) / 50



def traffic_far(arg) :
    if arg < 220 :
        return (arg - 170)/ 50
    elif arg >= 220 :
        return 1.0

#DISTANCE STONE

def stone_near(arg) :
    if arg <= 60 :
        return 1.0
    elif arg > 60 :
        return (120 - arg) / 60


def stone_medium(arg) :
    if arg < 120 :
        return (arg -60) / 60
    elif arg <= 150 and arg >= 120 :
        return 1.0
    elif arg > 150 :
        return (150 - arg) / 50



def stone_far(arg) :
    if arg < 200 :
        return (arg - 150)/ 50
    elif arg >= 200 :
        return 1.0

# ANGLE

def angle_small(arg) :
    if arg <= 30 :
        return 1.0
    elif arg > 30 :
        return (60 - arg) / 30
def angle_big(arg) :
    if ( arg >= 60 ):
        return 1.0
    elif arg < 60 :
        return (arg - 30)/30