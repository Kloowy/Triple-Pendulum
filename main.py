import pygame as pg
import pymunk as pm
import pymunk.pygame_util

pymunk.pygame_util.positive_y_is_up = False
pg.init()

size = 700
back = (0, 0, 0)
fps = 240

rope_length = 75
tail_length = 1
tail = []
tail1 = []
tail2 = []
# a = 0

space = pm.Space()
space.gravity = 0, 1000
ball_mass, ball_radius = 1, 7

screen = pg.display.set_mode((size, size))
clock = pg.time.Clock()
draw_options = pymunk.pygame_util.DrawOptions(screen)

class String():
    def __init__(self, body1, attachment, indefier="body"):
        self.body1 = body1
        if indefier == "body":
            self.body2 = attachment
        elif indefier == "position":
            self.body2 = pm.Body(body_type=pm.Body.STATIC)
            self.body2.position = attachment
        joint = pm.PinJoint(self.body1, self.body2)
        space.add(joint)

def pm_circle(c_mass, c_rad, x, y, el, fr):
    c_moment = pm.moment_for_circle(c_mass, 0, c_rad)
    c_body = pm.Body(c_mass, c_moment)
    c_body.position = x, y
    c_shape = pm.Circle(c_body, c_rad)
    c_shape.elasticity = el
    c_shape.friction = fr
    space.add(c_body, c_shape)
    return c_body, c_rad

c_body, c_rad = pm_circle(1, 15, size/2+rope_length*2, size/2/2, 0.1, 0.5)
c_body1, c_rad1 = pm_circle(1, 15, size/2+rope_length*3, size/2/2, 0.1, 0.5)
c_body2, c_rad2 = pm_circle(1, 15, size/2+rope_length*4, size/2/2, 0.1, 0.5)

string1 = String(c_body, (size/2, size/2/2), "position")
string1 = String(c_body, c_body1)
string1 = String(c_body1, c_body2)

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            loop = False


    space.step(1 / fps)
    space.debug_draw(draw_options)
    screen.fill(back)

    if len(tail) >= tail_length*1200:
        for i in range(2):
            tail.pop(0)
        for i in range(2):
            tail1.pop(0)
        for i in range(2):
            tail2.pop(0)

    tail.append(int(c_body.position[0]))
    tail.append(int(c_body.position[1]))
    tail1.append(int(c_body1.position[0]))
    tail1.append(int(c_body1.position[1]))
    tail2.append(int(c_body2.position[0]))
    tail2.append(int(c_body2.position[1]))

    for i in range(len(tail)):
        pg.draw.circle(screen, (75, 0, 0), (int(tail[i-i%2]), int(tail[i-i%2-1])), 2)
    for i in range(len(tail1)):
        pg.draw.circle(screen, (0, 75, 0), (int(tail1[i-i%2]), int(tail1[i-i%2-1])), 2)
    for i in range(len(tail2)):
        pg.draw.circle(screen, (0, 0, 75), (int(tail2[i-i%2]), int(tail2[i-i%2-1])), 2)


    pg.draw.line(screen, (0, 255, 255), (size/2, size/2/2), (int(c_body.position[0]), int(c_body.position[1])), 3)
    pg.draw.line(screen, (0, 255, 255), (int(c_body.position[0]), int(c_body.position[1])), (int(c_body1.position[0]), int(c_body1.position[1])), 3)
    pg.draw.line(screen, (0, 255, 255), (int(c_body1.position[0]), int(c_body1.position[1])), (int(c_body2.position[0]), int(c_body2.position[1])), 3)
    pg.draw.circle(screen, (100, 100, 100), (int(c_body.position[0]), int(c_body.position[1])), c_rad)
    pg.draw.circle(screen, (100, 100, 100), (int(c_body1.position[0]), int(c_body1.position[1])), c_rad)
    pg.draw.circle(screen, (100, 100, 100), (int(c_body2.position[0]), int(c_body2.position[1])), c_rad)
    pg.draw.circle(screen, (255, 255, 0), (size/2, size/2/2), 5)

    pg.display.flip()
    clock.tick(fps)
