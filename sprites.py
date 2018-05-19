import pygame as pg
import math
from random import uniform
from settings import *
from tilemap import collide_hit_rect
from dijkstra import *
from defuzzy import  *
vec = pg.math.Vector2

def collide_with_walls(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        # print(hits)
        if hits:
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width /2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width /2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y

class Car(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.players
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_img
        self.rect = self.image.get_rect()
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.car_speed = PLAYER_SPEED
        self.vt = 0
        self.index = 0
        self.index_next = 1

        self.rot_speed = 0
        self.status_light = ""

        # self.target_dis = 10

    # def get_keys(self):
    #     self.rot_speed = 0
    #     self.vel = vec(0, 0)
    #     keys = pg.key.get_pressed()
    #     if keys[pg.K_LEFT] or keys[pg.K_a]:
    #         self.rot_speed = PLAYER_ROT_SPEED
    #     if keys[pg.K_RIGHT] or keys[pg.K_d]:
    #         self.rot_speed = -PLAYER_ROT_SPEED
    #     if keys[pg.K_UP] or keys[pg.K_w]:
    #         self.vel = vec(PLAYER_SPEED, 0).rotate(-self.rot)
    #     if keys[pg.K_DOWN] or keys[pg.K_s]:
    #         self.vel = vec(-PLAYER_SPEED / 2, 0).rotate(-self.rot)

    def move(self):

        # print(self.rot)
        self.image = pg.transform.rotate(self.game.player_img, self.rot )
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.acc = vec(self.car_speed, 0).rotate(-self.rot)
        self.acc += self.vel * -1
        self.vel += self.acc * self.game.dt
        self.pos += self.vel * self.game.dt + self.acc * self.game.dt
        # print(self.acc)
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')


        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center

    def get_distance(self,index):
        self.distance = math.sqrt((self.game.path[index].pos.x - self.pos.x) ** 2 +
                                  (self.game.path[index].pos.y - self.pos.y) ** 2)
        # print(self.distance)

    def update(self):

        if (self.game.color_light == RED):
            self.status_light = "red"
        if (self.game.color_light == YELLOW):
            self.status_light = "red"
        if (self.game.color_light == GREEN):
            self.status_light = "green"

        self.angle = (self.game.path[self.index].pos - self.pos).angle_to(vec(1,0))
        self.angle_next  = (self.game.path[self.index_next].pos - self.pos).angle_to(vec(1,0))
        self.abs = math.fabs(self.angle_next) % 90

        # print(self.abs)
        # print(self.index_next)

        self.get_distance(self.index)

        self.rot = (self.rot + self.rot_speed * self.game.dt) % 360
        self.rot = self.angle
        self.move()
        # if (self.abs > 65):
        #     self.rot_speed = self.angle_next/2
        # if(self.abs > 75  ) :
        #     self.rot_speed = self.angle_next
        # if (self.abs > 80):
        #     self.rot_speed = 0
        if self.distance < 30 :
            self.index += 1
            # self.index_next += 1
            if (self.index > (len(self.game.path) - 1)):
                self.index = len(self.game.path) - 1
            # if (self.index_next > (len(self.game.path) - 1)):
            #     self.index_next = len(self.game.path) - 1

        self.change_speed_traffic()

    def change_speed_traffic(self):
        if (self.game.stone_bool):
            for i in range(len(self.game.list_stones)):
                self.angle_stone = (self.game.list_stones[i].pos - self.pos).angle_to(vec(1, 0))
                self.abs_angle_stone = math.fabs(math.fabs(self.angle_stone) - math.fabs(self.angle))
                # print(self.abs_angle_stone)
                if(self.abs_angle_stone < 30) :
                    self.distance_stone = math.sqrt((self.game.list_stones[i].rect.x - self.pos.x) ** 2 +
                                                    (self.game.list_stones[i].rect.y - self.pos.y) ** 2)
                    self.car_speed = dependency_stone(self.distance_stone)

        else:
            self.target_dis = math.sqrt((self.game.path[len(self.game.path) - 1].pos.x - self.pos.x) ** 2 +
                                        (self.game.path[len(self.game.path) - 1].pos.y - self.pos.y) ** 2)

            self.car_speed = dependency_stone(self.target_dis)

            for i in range(len(self.game.pos_traffics)):
                self.angle_light = (self.game.pos_traffics[i].pos - self.pos).angle_to(vec(1, 0))
                print("angle : ",self.angle )
                print("angle_traffic :",self.angle_light)
                self.abs_angle_traffic = math.fabs(math.fabs(self.angle_light) - math.fabs(self.angle))

                print("do lech khoang goc :", self.abs_angle_traffic)

                if ( self.abs_angle_traffic < 60 ) :
                    self.distance_traffic = math.sqrt((self.game.pos_traffics[i].pos.x - self.pos.x) ** 2 +
                                                  (self.game.pos_traffics[i].pos.y - self.pos.y) ** 2)
                    # print(self.distance_traffic)
                    self.car_speed = dependency_traffic(60,self.status_light,self.distance_traffic,self.game.times)





class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.stone_img = self.game.stone_img
        self.pos = vec(x, y)
    # def update(self):


class Stone(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.stones
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.stone_img = self.game.stone_img
        self.rect = pg.Rect(x, y, w, h)
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.pos = vec(x, y)

class Maker(pg.sprite.Sprite) :
    def __init__(self,game,x,y):
        self.groups = game.makers
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image_start = game.maker_img_start
        self.image_end = game.maker_img_end
        self.rect = self.image_start.get_rect()
        self.pos = vec(x, y)
        self.traffic_img = game.traffic_img




