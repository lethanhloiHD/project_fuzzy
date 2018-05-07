import pygame as pg
import sys
from os import path
from settings import *
from sprites import *
from tilemap import *
from dijkstra import *

# HUD functions
def draw_player_speed(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 30
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    if pct > 0.6:
        col = GREEN
    elif pct > 0.3:
        col = YELLOW
    else:
        col = RED
    pg.draw.rect(surf, col, fill_rect)
    pg.draw.rect(surf, col, outline_rect, 2)


def draw_traffic_light(surf, x, y, col1, col2, col3):
    BAR_LENGTH = 150
    BAR_HEIGHT = 40
    fill_red = pg.Rect(x, y,50, BAR_HEIGHT)
    fill_amber = pg.Rect(x+50, y, 50, BAR_HEIGHT)
    fill_green = pg.Rect(x+100, y, 50, BAR_HEIGHT)

    pg.draw.ellipse(surf, col1,fill_red)
    pg.draw.ellipse(surf, col2, fill_amber)
    pg.draw.ellipse(surf, col3, fill_green)

    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    # fill_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    pg.draw.rect(surf, GREEN, outline_rect, 4)


def draw_times(surf, text, size, x,y) :
    font= pg.font.Font(pg.font.match_font('arial'),size)
    text_surface = font.render(text, True, RED)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)
def draw_speed(surf, text, size, x,y) :
    font= pg.font.Font(pg.font.match_font('arial'),size)
    text_surface = font.render(text, True, RED)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)



class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.load_data()

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        map_folder = path.join(game_folder, 'maps')
        self.map = TiledMap(path.join(map_folder, 'title_4.tmx'))

        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()
        self.stone_img = pg.image.load(path.join(img_folder, STONE_IMG)).convert_alpha()
        self.maker_img = pg.image.load(path.join(img_folder, MAKER_IMG)).convert_alpha()

    def new(self):
        self.players = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.stones = pg.sprite.Group()
        self.color_light = BLACK
        self.times=0
        self.g = Graph()

        # self.stone=(Obstacle(self,800,125,35,35))
        # self.car = Car(self, 100, 125)
        # self.start = Maker(self, self.car.pos.x, self.car.pos.y)
        # self.end = Maker(self,800,125)
        # self.traffic = Maker(self, 510, 125)

        self.maker = [Maker(self, 510, 125),Maker(self, 510, 385),Maker(self, 510, 650),
                      Maker(self, 910, 650),Maker(self, 910, 385),Maker(self, 910, 125)]
        self.path = []

        for tile_object in self.map.tmxdata.objects:

            if tile_object.name == 'car':
                self.car = Car( self, tile_object.x, tile_object.y )
                self.start = Maker(self, self.car.pos.x, self.car.pos.y)
            if tile_object.name == 'end':
                self.end = Maker(self, tile_object.x, tile_object.y)
            if tile_object.name == 'pos_traffic':
                self.pos_traffic = Maker(self, tile_object.x, tile_object.y)
            if tile_object.name == 'wall':
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)


        #find path shortest
        self.find_path()
        print(shortest_path(self.g, str(self.index_start), str(self.index_end)))
        pos_path = shortest_path(self.g, str(self.index_start), str(self.index_end))
        for i in range(len(pos_path)) :
            self.path.append(self.maker[int(pos_path[i])])
        self.path.append(self.end)

        #Camera
        self.camera = Camera(self.map.width, self.map.height)
        self.draw_debug = False



    def cal_dist(self):
        self.index_start = 0
        dstart = math.sqrt((self.maker[self.index_start].pos.x - self.start.pos.x) ** 2 +
                  (self.maker[self.index_start].pos.y - self.start.pos.y) ** 2)

        self.index_end = 0
        dend = math.sqrt((self.maker[self.index_end].pos.x - self.end.pos.x) ** 2 +
                           (self.maker[self.index_end].pos.y - self.end.pos.y) ** 2)

        for i in range(len(self.maker)) :
            distance_start = math.sqrt((self.maker[i].pos.x - self.start.pos.x) ** 2 +
                                        (self.maker[i].pos.y - self.start.pos.y) ** 2)
            if distance_start < dstart :
                self.index_start = i
                dstart = distance_start

            distance_end = math.sqrt((self.maker[i].pos.x - self.end.pos.x) ** 2 +
                                       (self.maker[i].pos.y - self.end.pos.y) ** 2)
            if distance_end < dend :
                self.index_end = i
                dend = distance_end

        # if( self.dend < 285 ) :
        #     self.dend = 1
        # else : self.dend = 2
        # if (self.dstart < 285):
        #     self.dstart = 1
        # else:
        #     self.dstart = 2
        # print(self.dend,self.dstart)
        # print(dend)
        print(self.index_start,self.index_end)
        # return min(self.dis_start),min(self.dis_end)

    def find_path(self):
        self.g.add_vertex('0')
        self.g.add_vertex('1')
        self.g.add_vertex('2')
        self.g.add_vertex('3')
        self.g.add_vertex('4')
        self.g.add_vertex('5')

        self.g.add_edge('0', '1', 1 )
        self.g.add_edge('0', '5', 2)
        self.g.add_edge('1', '2', 1)
        self.g.add_edge('1', '0', 1)
        self.g.add_edge('1', '4', 2)
        self.g.add_edge('2', '1', 1)
        self.g.add_edge('2', '3', 2)
        self.g.add_edge('3', '4', 1)
        self.g.add_edge('3', '2', 2)
        self.g.add_edge('4', '5', 1)
        self.g.add_edge('4', '1', 2)
        self.g.add_edge('4', '3', 1)
        self.g.add_edge('5', '0', 2)
        self.g.add_edge('5', '4', 1)

        # self.g.add_edge('start', str(self.index_start), self.dstart)
        # self.g.add_edge('5', '4', 1)


        # print(self.g)
        self.cal_dist()
        # print(dijkstra(self.g, 'a'))



    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS)/1000
            self.events()
            self.draw_traffic()
            self.update()
            self.draw()


    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):

        self.players.update()

        self.camera.update(self.car)

    def draw_traffic(self):
        self.time = pg.time.get_ticks() / 1000 % 20
        self.times = self.time + 1
        self.color_light1 = BLACK
        self.color_light2 = BLACK
        self.color_light3 = BLACK
        if (self.time) < 8:
            self.color_light1 = RED
            self.color_light = RED
            self.color_light2 = BLACK
            self.color_light3 = BLACK
        elif (self.time) < 10:
            self.times = self.time - 7
            self.color_light1 = BLACK
            self.color_light2 = YELLOW
            self.color_light3 = BLACK
            self.color_light = YELLOW
        elif (self.time) < 18:
            self.times = self.time - 9
            self.color_light1 = BLACK
            self.color_light2 = BLACK
            self.color_light3 = GREEN
            self.color_light = GREEN
        elif (self.time) < 20:
            self.times = self.time - 17
            self.color_light1 = BLACK
            self.color_light2 = YELLOW
            self.color_light3 = BLACK
            self.color_light = YELLOW
        # print(self.color_light)


    def draw(self):

        pg.display.set_caption("{:.1f}".format(self.clock.get_fps()))
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        # for i in range(len(self.maker)) :
        #     self.screen.blit(self.maker[i].image, self.maker[i].pos)
        self.screen.blit(self.start.image, self.start.pos)
        self.screen.blit(self.end.image, self.end.pos)
        # for sprite in self.all_sprites:
            # if isinstance(sprite, Mob):
            #     sprite.draw_health()
        self.screen.blit(self.car.image, self.camera.apply(self.car))
        if self.draw_debug:
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(self.car.hit_rect), 1)
        if self.draw_debug:
            for wall in self.walls:
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(wall.rect), 1)
        draw_player_speed(self.screen, 100, 10, (self.car.car_speed) / PLAYER_SPEED)
        draw_traffic_light(self.screen, 300, 10, self.color_light1, self.color_light2, self.color_light3)
        draw_times(self.screen, str(self.times.__int__()), 40, 480, 10)
        draw_speed(self.screen, str("{:.0f}".format(self.car.car_speed)), 40, 250, 5)
        # self.map_img.blit(self.stone_img,( self.stone.rect.x,self.stone.rect.y))
        pg.display.flip()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_h:
                    self.end.kill()
                    self.draw_debug = not self.draw_debug
            # if event.type == pg.MOUSEBUTTONUP and event.button == 1 :
            #     self.pos_maker = pg.mouse.get_pos()
            #     self.pos_makerx, self.pos_makery = pg.mouse.get_pos()
            #     self.maker = Maker(self, self.pos_makerx, self.pos_makery)
            #     self.map_img.blit(self.maker_img, self.pos_maker)
            #     print(self.pos_maker)
            if event.type == pg.MOUSEBUTTONUP and event.button == 1 :
                self.pos_maker = pg.mouse.get_pos()
                self.pos_makerx, self.pos_makery = pg.mouse.get_pos()
                self.maker_click = Maker(self, self.pos_makerx, self.pos_makery)

                self.map_img.blit(self.maker_img, self.pos_maker)
                print(self.pos_maker)

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_k:
                    self.maker_click.kill()
            if event.type == pg.MOUSEBUTTONUP and event.button == 3 :
                self.pos_stone = pg.mouse.get_pos()
                self.pos_stonex, self.pos_stoney = pg.mouse.get_pos()
                self.stone = Obstacle(self, self.pos_stonex, self.pos_stoney,35,35)
                self.map_img.blit(self.stone_img, self.pos_stone)

                self.distance_stone = math.sqrt((self.car.pos.x - self.pos_stonex) ** 2 +
                                                  (self.car.pos.y - self.pos_stoney) ** 2)

                # if (self.distance_stone < 500):
                #     self.car.vt = 100
                #     self.car.car_speed -= self.car.vt * self.dt

                # if (self.distance_stone < 200):
                #     # self.car.vt = 150
                #     # self.car.car_speed -= self.car.vt * self.dt

                if (self.distance_stone < 100):
                    # self.car.vt = 200
                    # self.car.car_speed -= self.car.vt * self.dt
                    self.car.car_speed = 0

                if (self.car.car_speed < 0):
                    self.car.car_speed = 0
                print(self.distance_stone)

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()