import numpy as np
import matplotlib.pyplot as plt
import skfuzzy as fuzz
from function_fuzzy import *

DOMAIN=[0,100]

RULE_TRAFFIC_LIGHTS=[["big","near","very_red","fast"],
["big","near","red","fast"],
["big","medium","red","fast"],
["big","medium","very_red","fast"],
["big","far","red","fast"],
["big","far","very_red","fast"],
["big","medium","green","fast"],
["big","medium","very_green","fast"],
["big","far","green","fast"],
["big","far","very_green","fast"],
["big","near","green","fast"],
["big","near","very_green","fast"],

["small","near","very_red","stop"],
["small","near","red","stop"],
["small","medium","red","slow"],
["small","medium","very_red","slow"],
["small","far","red","normal"],
["small","far","very_red","normal"],
["small","medium","green","fast"],
["small","medium","very_green","normal"],
["small","far","green","fast"],
["small","far","very_green","fast"],
["small","near","green","normal"],
["small","near","very_green","slow"]
]

RULE_TRAFFIC_LIGHT=[
["near","very_red","stop"],
["near","red","stop"],
["medium","red","slow"],
["medium","very_red","normal"],
["far","red","fast"],
["far","very_red","fast"],
["medium","green","normal"],
["medium","very_green","normal"],
["far","green","fast"],
["far","very_green","fast"],
["near","green","normal"],
["near","very_green","slow"]
]


RULE_STONE=[["near","stop"],
["medium","normal"],
["far","fast"]]
SPEED =[0,20,40,60,80,100]



def defuzzy_slow(slice) :
    speed_range = np.arange(DOMAIN[0],DOMAIN[1],0.01)
    speed_high_fx = fuzz.trimf(speed_range,[SPEED[0],SPEED[1],SPEED[2]])
    # print(speed_high_fx)

    speed_slice = np.fmin(slice,speed_high_fx)

    defuzzy_value  = fuzz.defuzz(speed_range, speed_slice ,'centroid')

    return defuzzy_value

def defuzzy_normal(slice) :
    speed_range = np.arange(DOMAIN[0],DOMAIN[1],0.01)
    speed_high_fx = fuzz.trimf(speed_range,[SPEED[1],SPEED[3],SPEED[4]])
    # print(speed_high_fx)

    speed_slice = np.fmin(slice,speed_high_fx)

    defuzzy_value  = fuzz.defuzz(speed_range, speed_slice ,'centroid')

    return defuzzy_value

def defuzzy_fast(slice) :
    speed_range = np.arange(DOMAIN[0],DOMAIN[1],0.01)
    speed_high_fx = fuzz.trimf(speed_range,[SPEED[3],SPEED[4],SPEED[5]])
    # print(speed_high_fx)

    speed_slice = np.fmin(slice,speed_high_fx)

    defuzzy_value  = fuzz.defuzz(speed_range, speed_slice ,'centroid')

    return defuzzy_value
def defuzzy_stop() :
    return 0



def dependency_traffic (angle,status_light,distance_traffic, times) :
    near = traffic_near(distance_traffic)
    medium = traffic_medium(distance_traffic)
    far = traffic_far(distance_traffic)
    distance_traffics_lable = []
    distance_traffics = []
    traffic_light = []
    traffic_light_label = []

    speed = []
    speed_label = []

    fire = []
    defuzzy=[]
    if( near <= 1 and near >= 0) :
        distance_traffics.append(near )
        distance_traffics_lable.append("near")
    if (medium <= 1 and medium >= 0):
        distance_traffics.append(medium)
        distance_traffics_lable.append("medium")
    if (far <= 1 and far >= 0):
        distance_traffics_lable.append("far")
        distance_traffics.append(far)


    if(status_light== "red") :
        light_red = red(times)
        light_very_red = very_red(times)
        if ( light_red >= 0 and light_red <= 1 ) :
            traffic_light.append(light_red)
            traffic_light_label.append("red")
        if (light_very_red >= 0 and light_very_red <=1 ) :
            traffic_light.append(light_very_red)
            traffic_light_label.append("very_red")

    if (status_light == "green"):
        light_green = green(times)
        light_very_green = very_green(times)
        if (light_green >= 0 and light_green <= 1):
            traffic_light.append(light_green)
            traffic_light_label.append("green")
        if (light_very_green >= 0 and light_very_green <= 1):
            traffic_light.append(light_very_green)
            traffic_light_label.append("very_green")

    # angle
    ang_small = angle_small(angle)
    ang_big  = angle_big(angle)
    angles = []
    angle_lable = []
    if (ang_small <= 1 and ang_big >= 0):
        angles.append(ang_small)
        angle_lable.append("small")
    if (ang_big <= 1 and ang_big >= 0):
        angles.append(ang_big)
        angle_lable.append("big")


    # for k in range(len(angle_lable)):
    for i in range(len(distance_traffics_lable)):
        for j in range(len(traffic_light_label)):
            min_num = min( distance_traffics[i], traffic_light[j])
            ######################################################
            fire.append(distance_traffics[i] * traffic_light[j])
            for row in range(len(RULE_TRAFFIC_LIGHT)):
                if (distance_traffics_lable[i] == RULE_TRAFFIC_LIGHT[row][0]
                        and traffic_light_label[j] == RULE_TRAFFIC_LIGHT[row][1]):
                    speed_label.append(RULE_TRAFFIC_LIGHT[row][2])
                    speed.append(min_num)

    # print(speed)
    for i in range(len(speed_label)) :
        if ( speed_label[i] == "fast") :
            defuzzy.append(defuzzy_fast(speed[i]))
        if ( speed_label[i] == "normal") :
            defuzzy.append(defuzzy_normal(speed[i]))
        if ( speed_label[i] == "slow") :
            defuzzy.append(defuzzy_slow(speed[i]))
        if ( speed_label[i] == "stop") :
            defuzzy.append(defuzzy_stop())

    # result = 0
    tuso = 0
    mauso = 0
    for i in range(len(speed_label)) :
        tuso += fire[i] * defuzzy[i]
        mauso += fire[i]

    result = tuso / mauso
    # return result
    print(int(result))

    return result

def dependency_stone (distance_stone) :
    near = stone_near(distance_stone)
    medium = stone_medium(distance_stone)
    far = stone_far(distance_stone)
    distance_stones= []
    distance_label=[]
    speed_label = []
    defuzzy = []


    if (near <= 1 and near >= 0):
        distance_stones.append(near)
        distance_label.append("near")
    if (medium <= 1 and medium >= 0):
        distance_stones.append(medium)
        distance_label.append("medium")
    if (far <= 1 and far >= 0):
        distance_stones.append(far)
        distance_label.append("far")

    print(distance_label,distance_stones)
    for i in range(len(distance_label)) :
        for j in range(len(RULE_STONE)):
            if (distance_label[i] == RULE_STONE[j][0]) :
                speed_label.append(RULE_STONE[j][1])

    print(speed_label)
    for i in range(len(speed_label)) :
        if ( speed_label[i] == "fast") :
            defuzzy.append(defuzzy_fast(distance_stones[i]))
        if ( speed_label[i] == "normal") :
            defuzzy.append(defuzzy_normal(distance_stones[i]))
        if ( speed_label[i] == "slow") :
            defuzzy.append(defuzzy_slow(distance_stones[i]))
        if ( speed_label[i] == "stop") :
            defuzzy.append(defuzzy_stop())

    # print((defuzzy))

    tuso = 0
    mauso = 0

    for i in range(len(distance_stones)) :
        tuso += distance_stones[i] * defuzzy[i]
        mauso +=distance_stones[i]

    result = int(tuso/mauso)
    print(result)

    return result

# dependency_stone(10)/
