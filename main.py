import pygame as pg
import pymunk as pm
import pymunk.pygame_util
# from random import randint
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
# segment_thickness = 6

screen = pg.display.set_mode((size, size))
clock = pg.time.Clock()
draw_options = pymunk.pygame_util.DrawOptions(screen)

# pm.Segment(STATIC, 6, space, 'darkolivegreen')
# pm.Segment((0, size), (size, size), 20, space, 'darkslategray')

# ====================================================== CIRCLE ======================================================

# circle_mass = 1
# circle_radius = 50
#
# circle_moment = pm.moment_for_circle(circle_mass, 0, circle_radius)
# circle_body = pm.Body(circle_mass, circle_moment)
# circle_body.position = size/2+rope_length, 50
# circle_shape = pm.Circle(circle_body, circle_radius)
# circle_shape.elasticity = 0.1
# circle_shape.friction = 0.5
# space.add(circle_body, circle_shape)

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
    # def draw(self):
    #     pos1 = convert_coordinates(self.body1.position)
    #     pos2 = convert_coordinates(self.body2.position)
    #     pg.draw.line(screen, (255, 255, 255), pos1, pos2, 5)

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
# pm.constraints.PinJoint(c_body, c_body1, (0, 0), (0, 0))

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


    # for i in tail1:
    #     pg.draw.circle(screen, (50, 50, 50), tail1[i], 3)
    # a += 1
    # if a == 10:
    #     space.gravity = randint(-1000, 1000), randint(-1000, 1000)
    #     a = 0

    pg.display.flip()
    clock.tick(fps)
