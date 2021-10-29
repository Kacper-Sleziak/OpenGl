import sys
from datetime import datetime, time

from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random


def startup():
    update_viewport(None, 400, 400)
    glClearColor(1.0, 1.0, 1.0, 1.0)


def shutdown():
    pass


def render_exercise_1():
    glClear(GL_COLOR_BUFFER_BIT)

    glBegin(GL_TRIANGLES)
    glVertex2f(50.0, 0.0)
    glColor3f(1.0, 0.0, 0.0)

    glVertex2f(0.0, 100.0)
    glColor3f(0, 1.0, 0)

    glVertex2f(-50.0, 0.0)
    glColor3f(0, 0, 1.0)

    glEnd()
    glFlush()


def render_exercise_3(x, y, a, b, d=0, color_pack1=(1.0, 0, 0), color_pack2=(0, 0, 1.0)):
    # x, y are cordinates of left bottom vertex
    r1, g1, b1 = color_pack1
    r2, g2, b2 = color_pack2

    glClear(GL_COLOR_BUFFER_BIT)
    if a == 0:
        a = 1

    if b == 0:
        b = 1

    if d != 0:
        a = a * d
        b = b * d

        if a > 100 - x:
            while a > 100 - x:
                a = a / 10

        if b > 100 - x:
            while b > 100 - x:
                b = b / 10

    glBegin(GL_TRIANGLES)

    glColor3f(r1, g1, b1)
    glVertex2f(x, y)
    glVertex2f(x + a, y)
    glVertex2f(x + a, y + b)
    glEnd()

    glBegin(GL_TRIANGLES)
    glColor3f(r2, g2, b2)
    glVertex2f(x, y)
    glVertex2f(x, y + b)
    glVertex2f(x + a, y + b)
    glEnd()


def render_rec(x, y, a, b):
    glBegin(GL_TRIANGLES)
    glColor3f(1.0, 0, 0)
    glVertex2f(x, y)
    glVertex2f(x + a, y)
    glVertex2f(x + a, y + b)
    glEnd()

    glBegin(GL_TRIANGLES)
    glColor3f(1.0, 0, 0)
    glVertex2f(x, y)
    glVertex2f(x, y + b)
    glVertex2f(x + a, y + b)
    glEnd()
    glFlush()


def draw_carpet_part(x, y, a, b):
    render_rec(x, y, a / 3, b / 3)
    render_rec(x + a / 3, y, a / 3, b / 3)
    render_rec(x + (2 * a / 3), y, a / 3, b / 3)

    render_rec(x, y + b / 3, a / 3, b / 3)
    render_rec(x, y + (2 * b) / 3, a / 3, b / 3)

    render_rec(x + a / 3, y + (2 * b) / 3, a / 3, b / 3)
    render_rec(x + 2 * a / 3, y + (2 * b) / 3, a / 3, b / 3)

    render_rec(x + 2 * a / 3, y + b / 3, a / 3, b / 3)

    glFlush()


def render_exercise_4():
    glClear(GL_COLOR_BUFFER_BIT)
    x = -100
    y = -100
    a = 60
    b = 45

    draw_carpet_part(x, y, a, b)
    draw_carpet_part(x + a, y, a, b)
    draw_carpet_part(x + 2 * a, y, a, b)

    draw_carpet_part(x, y, a, b)
    draw_carpet_part(x, y + b, a, b)
    draw_carpet_part(x, y + 2 * b, a, b)

    draw_carpet_part(x + a, y + 2 * b, a, b)
    draw_carpet_part(x + 2 * a, y + 2 * b, a, b)

    draw_carpet_part(x + 2 * a, y + b, a, b)


def update_viewport(window, width, height):
    if height == 0:
        height = 1
    if width == 0:
        width = 1

    aspectRatio = width / height
    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()

    if width <= height:
        glOrtho(-100.0, 100.0, -100.0 / aspectRatio, 100.0 / aspectRatio, 1.0, -1.0)
    else:
        glOrtho(-100.0 * aspectRatio, 100.0 * aspectRatio, -100.0, 100.0, 1.0, -1.0)

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
    random.seed(random.randint(1, 100000))

    r1 = random.uniform(0, 1)
    g1 = random.uniform(0, 1)
    b1 = random.uniform(0, 1)

    r2 = random.uniform(0, 1)
    g2 = random.uniform(0, 1)
    b2 = random.uniform(0, 1)

    color_pack1 = (r1, g1, b1)
    color_pack2 = (r2, g2, b2)

    while not glfwWindowShouldClose(window):
        # render_exercise_3(x=0, y=0, a=50, b=30, d=3, color_pack1=color_pack1, color_pack2=color_pack2)
        render_exercise_4()
        glfwSwapBuffers(window)
        glfwWaitEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()
