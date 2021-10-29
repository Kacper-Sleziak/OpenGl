#!/usr/bin/env python3
import math
import sys
import numpy as np

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


def get_points(n):
    array_of_points = [[[(0, 0, 0) for col in range(3)] for row in range(n)] for element in range(n)]
    step = 1 / n

    for i in range(n):
        for k in range(n):
            for j in range(3):
                u = 0 + i * step
                v = 0 + k * step

                x = (-90 * u ** 5 + 225 * u ** 4 - 270 * u ** 3 + 180 * u ** 2 - 45 * u) * math.cos(math.pi * v)
                y = 160 * u ** 4 - 320 * u ** 3 + 160 * u ** 2
                z = (-90 * u ** 5 + 225 * u ** 4 - 270 * u ** 3 + 180 * u ** 2 - 45 * u) * math.sin(math.pi * v)

                point = (x, y, z)
                array_of_points[i][k][j] = point

    return array_of_points


def render(time, points, n, angle):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    angle = time * 180 / math.pi
    spin(angle)

    glBegin(GL_POINTS)
    glColor3f(1.0, 0.0, 0.0)

    for cols in points:
        for row in cols:
            for point in row:
                x, y, z = point
                glVertex3f(x, y, z)
    glEnd()

    for i in range(n):
        for j in range(n):
            if i + 1 < n and j + 1 < n:
                for k in range(3):
                    x1, y1, z1 = points[i][j][k]
                    x2, y2, z2 = points[i + 1][j][k]
                    x3, y3, z3 = points[i][j + 1][k]

                    glBegin(GL_LINES)
                    glColor3f(0.0, 1.0, 0.0)

                    glVertex3f(x1, y1, z1)
                    glVertex3f(x2, y2, z2)
                    glEnd()

                    glBegin(GL_LINES)
                    glColor3f(0.0, 1.0, 0.0)
                    glVertex3f(x1, y1, z1)
                    glVertex3f(x3, y3, z3)
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
    n = 20
    points = get_points(n)
    while not glfwWindowShouldClose(window):
        render(glfwGetTime(), points, n, 90)
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()
