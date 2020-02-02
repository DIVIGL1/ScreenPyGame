#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import random
import math

SCREEN_DIM = (800, 600)

class Vec2d(object):
    def __init__(self, x_coordinate, y_coordinate):
        # Initiates vector with (x,y) coordinates.
        self.x, self.y = x_coordinate, y_coordinate

    def __add__(self, add_vector):
        # Creates new vector using this and new one.
        return (Vec2d(self.x + add_vector.x, self.y + add_vector.y))

    def __sub__(self, add_vector):
        # Creates new vector using this and new one.
        return (Vec2d(self.x - add_vector.x, self.y - add_vector.y))

    def __mul__(self, k):
        # Creates new vector using this multyplayed with n.
        return (Vec2d(self.x * k, self.y * k))

    def len(self):
        # Returns it's own length.
        return (math.sqrt(self.x**2 + self.y**2))

    def int_pair(self):
        # Returns tuple of it's own coordinates.
        return (self.x, self.y)

class Polyline(object):
    def __init__(self, gameDisplay, steps=35, screen_dim=(800, 600)):
        Polyline.points = []
        Polyline.speeds = []
        Polyline.steps = steps
        Polyline.screen_dim = screen_dim
        Polyline.polyline_points = []

    def add_point(self, point, speed):
        # Adds points to the list.
        Polyline.points.append(point)
        Polyline.speeds.append(speed)

    def set_points(self):
        # Recalculates coordinates of points.
        for p in range(len(Polyline.points)):
            Polyline.points[p] = Polyline.points[p] + Polyline.speeds[p]
            if Polyline.points[p].x > Polyline.screen_dim[0] or Polyline.points[p].x < 0:
                Polyline.speeds[p] = Vec2d(- Polyline.speeds[p].x, Polyline.speeds[p].y)
            if Polyline.points[p].y > Polyline.screen_dim[1] or Polyline.points[p].y < 0:
                Polyline.speeds[p] = Vec2d(Polyline.speeds[p].x, -Polyline.speeds[p].y)

    def draw_points(self, width=3, color=(255, 255, 255)):
        # Draws points on a screen.
        for point in Polyline.points:
            pygame.draw.circle(gameDisplay, color, (int(point.x), int(point.y)), width)

    def draw_lines(self, width=3, color=(200, 200, 200)):
        # Draws lines on a screen using polyline_points.
        for point_num in range(-1, len(Polyline.polyline_points) - 1):
            start_point = Polyline.polyline_points[point_num].int_pair()
            end_point = Polyline.polyline_points[point_num + 1].int_pair()
            pygame.draw.line(gameDisplay, color, start_point, end_point, width)

class Knot(Polyline):
    def __init__(self):
#        super().__init__()
        pass

    def get_point(self, list_of_base_points, koeff, deg=None):
        if deg is None:
            deg = len(list_of_base_points) - 1
        if deg == 0:
            return (list_of_base_points[0])
        ret_value = \
            list_of_base_points[deg] * koeff + \
            self.get_point(list_of_base_points, koeff, deg - 1) * (1 - koeff)
        return (ret_value)

    def get_points(self, list_of_base_points, points_ko_bo):
        alpha = 1 / points_ko_bo
        res = []
        for i in range(points_ko_bo):
            res.append(self.get_point(list_of_base_points, i * alpha))
        return (res)

    def get_knot(self):
        if len(Polyline.points) < 3:
            return []
        res = []
        for i in range(-2, len(Polyline.points) - 2):
            ptn = []
            ptn.append((Polyline.points[i] + Polyline.points[i + 1]) * 0.5)
            ptn.append(Polyline.points[i + 1])
            ptn.append((Polyline.points[i + 1] + Polyline.points[i + 2]) * 0.5)
            res.extend(self.get_points(ptn, Polyline.steps))
        return (res)
    
    def add_point(self, point, speed):
        # Adds point to the list.
        Polyline.add_point(self, point, speed)
        # Calculate other points
        self.set_knots()

    def set_knots(self):
        Polyline.polyline_points = self.get_knot()

def draw_help():
    """функция отрисовки экрана справки программы"""
    gameDisplay.fill((50, 50, 50))
    font1 = pygame.font.SysFont("courier", 24)
    font2 = pygame.font.SysFont("serif", 24)
    data = []
    data.append(["F1", "Show Help"])
    data.append(["R", "Restart"])
    data.append(["P", "Pause/Play"])
    data.append(["Num+", "More points"])
    data.append(["Num-", "Less points"])
    data.append(["", ""])
    data.append([str(steps), "Current points"])

    pygame.draw.lines(gameDisplay, (255, 50, 50, 255), True, [
        (0, 0), (800, 0), (800, 600), (0, 600)], 5)
    for i, text in enumerate(data):
        gameDisplay.blit(font1.render(
            text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
        gameDisplay.blit(font2.render(
            text[1], True, (128, 128, 255)), (200, 100 + 30 * i))

if __name__ == "__main__":
    screen_dim = SCREEN_DIM
    pygame.init()
    gameDisplay = pygame.display.set_mode(screen_dim)
    pygame.display.set_caption("MyScreenSaver")

    steps = 35
    working = True
    polyline = Polyline(screen_dim=screen_dim, gameDisplay=gameDisplay, steps=steps)
    knot = Knot()
    show_help = False
    pause = True

    hue = 0
    color = pygame.Color(0)

    while working:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    working = False
                if event.key == pygame.K_r:
                    polyline = Polyline(screen_dim=screen_dim)
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_KP_PLUS:
                    steps += 1
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_KP_MINUS:
                    steps -= 1 if steps > 1 else 0

            if event.type == pygame.MOUSEBUTTONDOWN:
                point = Vec2d(event.pos[0], event.pos[1])
                speed = Vec2d(random.random() * 2, random.random() * 2)
                knot.add_point(point, speed)

        gameDisplay.fill((0, 0, 0))
        hue = (hue + 1) % 360
        color.hsla = (hue, 100, 50, 100)
        polyline.draw_points()
        knot.set_knots()
        polyline.draw_lines(color=color)

        if not pause:
            polyline.set_points()
        if show_help:
            draw_help()

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)

