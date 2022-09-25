import pygame
import pymunk
import math
import pymunk.pygame_util
import random


pygame.init()
WIDTH, HIGHT = 1400, 800  #1350
window = pygame.display.set_mode([WIDTH, HIGHT])

#pygame clock
clock = pygame.time.Clock()
fps = 61
pressed_pos = pygame.mouse.get_pos()

#colors
gelb = (255,255,0)
gruen = (0,255,0)
blau = (0,0,255)
rot = (255,0,0)
orange = (255,165,0)
weiss = (255,255,255)
schwarz = (0,0,0)

space = pymunk.Space()
space.gravity = (0, 700)

class Draw:
    def __init__(self):
        self.block_hight = 40
    def draw(self, draw_options, line):
        window.fill(gruen)
        space.debug_draw(draw_options)
        pygame.draw.line(window, "black", shape.body.position, pygame.mouse.get_pos(), 3)
        pygame.display.update()
    def create_ball(self, space, radius, mass):
        global shape
        body = pymunk.Body()
        body.position = (WIDTH/2, HIGHT/2)
        shape = pymunk.Poly.create_box(body, (self.block_hight, self.block_hight))
        shape.mass = mass
        shape.elasticity = 0.9
        shape.friction = 0.5
        #shape.color = pygame.Color('black')
        space.add(body, shape)
        return shape
    def create_boundaries(self, space):
        rects = [
            [(WIDTH/2, HIGHT-10), (WIDTH, 20)],
            [(WIDTH/2, 10), (WIDTH, 20)],
            [(10, HIGHT/2), (20, HIGHT)],
            [(WIDTH-10, HIGHT/2), (20, HIGHT)]
        ]
        for pos, size in rects:
            body = pymunk.Body(body_type=pymunk.Body.STATIC)
            body.position = pos
            shape = pymunk.Poly.create_box(body, size)
            shape.elasticity = 0.4
            shape.friction = 0.4
            space.add(body, shape)
    def create_blocks(self, count, size):
        for i in range(count):
            body = pymunk.Body(body_type=pymunk.Body.STATIC)
            body.position = (random.randint(0, WIDTH), random.randint(self.block_hight+50, HIGHT))
            shape = pymunk.Poly.create_box(body, size)
            shape.elasticity = 0.4
            shape.friction = 0.4
            space.add(body, shape)
    def calculate_distance(self, p1, p2):
        return math.sqrt((p2[1] - p1[1]) ** 2 + (p2[0] - p1[0]) ** 2)
    def calculate_angle(self, p1, p2):
        return math.atan2(p2[1] - p1[1], p2[0] - p1[0])
    def calculate_direction(self, line):
        angle = self.calculate_angle(*line)
        force = self.calculate_distance(*line) * 50
        fx = math.cos(angle) * force
        fy = math.sin(angle) * force
        return (fx, fy)


Draw = Draw()
def main():
    global space
    run = True
    dt = 1 / fps

    space = pymunk.Space()
    space.gravity = (0, 700)

    ball = Draw.create_ball(space, 30, 20)
    Draw.create_boundaries(space)
    Draw.create_blocks(10, (180, 20))

    draw_options = pymunk.pygame_util.DrawOptions(window)
    line = shape.body.position, pygame.mouse.get_pos()
    while run:
        if not line:
            line = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                line = shape.body.position, pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONUP:
                ball.body.angle = 0
                ball.body.apply_impulse_at_local_point((Draw.calculate_direction(line)), (0, 0))

        Draw.draw(draw_options, line)
        space.step(dt)
        clock.tick(fps)


if __name__ == '__main__':
    main()
