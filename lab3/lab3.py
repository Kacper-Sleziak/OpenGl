#!/usr/bin/env python3
import math
import sys
import random

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)


def shutdown():
    pass


def axes():
    glBegin(GL_LINES)

    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-5.0, 0.0, 0.0)
    glVertex3f(5.0, 0.0, 0.0)

    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, -5.0, 0.0)
    glVertex3f(0.0, 5.0, 0.0)

    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, -5.0)
    glVertex3f(0.0, 0.0, 5.0)

    glEnd()


def spin(angle):
    glRotate(angle, 1.0, 0.0, 0.0)
    glRotate(angle, 0.0, 1.0, 0.0)
    glRotate(angle, 0.0, 0.0, 1.0)


def get_color_array(n):
    colors = [[(0, 0, 0) for col in range(n + 1)] for row in range(n + 1)]

    random.seed(random.randint(1, 100))

    for i in range(n + 1):
        for k in range(n + 1):
            r = random.uniform(0, 1)
            g = random.uniform(0, 1)
            b = random.uniform(0, 1)
            colors[i][k] = (r, g, b)

    return colors


def get_points(n):
    array_of_points = [[(0, 0, 0) for col in range(n + 1)] for row in range(n + 1)]
    step = 1 / n

    for i in range(n + 1):
        for k in range(n + 1):
            u = 0 + i * step
            v = 0 + k * step

            x = (-90 * u ** 5 + 225 * u ** 4 - 270 * u ** 3 + 180 * u ** 2 - 45 * u) * math.cos(math.pi * v)
            y = 160 * u ** 4 - 320 * u ** 3 + 160 * u ** 2
            z = (-90 * u ** 5 + 225 * u ** 4 - 270 * u ** 3 + 180 * u ** 2 - 45 * u) * math.sin(math.pi * v)

            point = (x, y, z)
            array_of_points[i][k] = point

    return array_of_points


def render(time, points, colors, n):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    angle = time * 180 / math.pi
    spin(angle)

    for i in range(n + 1):
        for j in range(n + 1):
            if i + 1 < n + 1 and j + 1 < n + 1:

                x1, y1, z1 = points[i][j]
                x2, y2, z2 = points[i + 1][j]
                x3, y3, z3 = points[i][j + 1]
                x4, y4, z4 = points[i + 1][j + 1]

                glBegin(GL_TRIANGLES)

                r, g, b = colors[i][j]
                glColor3f(r, g, b)
                glVertex3f(x1, y1, z1)

                r, g, b = colors[i + 1][j]
                glColor3f(r, g, b)
                glVertex3f(x2, y2, z2)

                r, g, b = colors[i][j + 1]
                glColor3f(r, g, b)
                glVertex3f(x3, y3, z3)
                glEnd()

                glBegin(GL_TRIANGLES)

                r, g, b = colors[i + 1][j]
                glColor3f(r, g, b)
                glVertex3f(x2, y2, z2)

                r, g, b = colors[i][j + 1]
                glColor3f(r, g, b)
                glVertex3f(x3, y3, z3)

                glVertex3f(x4, y4, z4)
                r, g, b = colors[i + 1][j + 1]
                glColor3f(r, g, b)
                glEnd()
    axes()
    glFlush()


def update_viewport(window, width, height):
    if width == 0:
        width = 1
    if height == 0:
        height = 1
    aspect_ratio = width / height

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()

    if width <= height:
        glOrtho(-7.5, 7.5, -7.5 / aspect_ratio, 7.5 / aspect_ratio, 7.5, -7.5)
    else:
        glOrtho(-7.5 * aspect_ratio, 7.5 * aspect_ratio, -7.5, 7.5, 7.5, -7.5)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSwapInterval(1)

    startup()
    n = 50
    points = get_points(n)
    colors = get_color_array(n)
    while not glfwWindowShouldClose(window):
        render(glfwGetTime(), points, colors, n)
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()
