from pygame import display, draw, time, event, KEYDOWN, K_KP_ENTER, K_RETURN, FULLSCREEN
from random import randint

x_width = 800
y_width = 600

screen = display.set_mode([x_width, y_width], FULLSCREEN)
#screen = display.set_mode([x_width, y_width])

screen.fill([0, 0, 0])
base_radius = 20
max_radius = 50
num_circles = 1
circles = []

class Circle:
    def __init__(self):
        self.rad = randint(base_radius, max_radius)
        self.pos = [randint(max_radius,x_width - max_radius), randint(max_radius, y_width - max_radius)]
        self.col = [randint(100, 255), randint(100, 255), randint(100, 255)]
        self.width = 2

display.flip()

clock = time.Clock()
while True:
    ev = event.poll()
    if ev.type == KEYDOWN:
        if ev.key in [K_KP_ENTER, K_RETURN]:
            break
    screen.fill([0, 0, 0])
    circles.append(Circle())

    for circle in circles[:]:
        circle.rad += 1
        if circle.rad > 60:
            circles.remove(circle)

        draw.circle(screen, circle.col, circle.pos, circle.rad, circle.width)

    display.flip()
    clock.tick(60)


