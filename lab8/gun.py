from random import randrange as rnd, choice
import tkinter as tk
import random
import math
import time

# print (dir(math))

root = tk.Tk()
fr = tk.Frame(root)
root.geometry('800x600')
canv = tk.Canvas(root, bg='white')
canv.pack(fill=tk.BOTH, expand=1)


class ball():
    G = 1
    k = -0.02

    def __init__(self, x=40, y=450):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.collisions = 0
        self.color = choice(['blue', 'green', 'red', 'brown'])
        self.id = canv.create_oval(
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r,
            fill=self.color
        )
        self.live = 30

    def set_coords(self):
        canv.coords(
            self.id,
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r
        )

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """

        self.vx += ball.k * self.vx
        self.vy += (ball.G + ball.k * self.vy)
        if abs(self.vy) <= 0.1:
            self.vy = 0
        if abs(self.vx) <= 0.1:
            self.vx = 0
        self.x += self.vx
        self.y += self.vy

        if self.x + self.r > 800 or self.x - self.r < 0:
            self.vx *= -1
            self.x += self.vx

        if self.y + self.r > 600:
            self.vy *= -0.7
            self.y += 2*self.vy
            self.collisions += 1

        self.set_coords()



    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """

        x, y, r = obj.x, obj.y, obj.r
        x0, y0, r0 = self.x, self.y, self.r

        if (x-x0)**2 + (y-y0)**2 <= (r+r0)**2:
            return True

        return False

    def __del__(self):
        canv.delete(self.id)


class gun():

    def __init__(self, balls, bullet):
        self.balls = balls
        self.bullet = bullet
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.id = canv.create_line(20, 450, 50, 420, width=7)

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """

        self.bullet += 1
        new_ball = ball()
        new_ball.r += 5
        self.an = math.atan((event.y - new_ball.y) / (event.x - new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = self.f2_power * math.sin(self.an)
        self.balls += [new_ball]
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event=0):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan((event.y - 450) / (event.x - 20))
        if self.f2_on:
            canv.itemconfig(self.id, fill='orange')
        else:
            canv.itemconfig(self.id, fill='black')
        canv.coords(self.id, 20, 450,
                    20 + max(self.f2_power, 20) * math.cos(self.an),
                    450 + max(self.f2_power, 20) * math.sin(self.an)
                    )

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            canv.itemconfig(self.id, fill='orange')
        else:
            canv.itemconfig(self.id, fill='black')


class target:

    def __init__(self):
        self.points = 0
        self.live = 1
        self.id = canv.create_oval(0, 0, 0, 0)
        #self.id_points = canv.create_text(30, 30, text=self.points, font='28')
        x = self.x = rnd(600, 780)
        y = self.y = rnd(100, 500)
        r = self.r = rnd(5, 50)
        self.vx = 0
        self.vy = rnd(3, 7)
        self.Y0 = self.y
        self.a = rnd(50, 100)
        color = self.color = 'red'
        canv.coords(self.id, x - r, y - r, x + r, y + r)
        canv.itemconfig(self.id, fill=color)

    def hit(self, points=1):
        """Попадание шарика в цель."""
        canv.coords(self.id, -10, -10, -10, -10)
        self.points += points
        #canv.itemconfig(self.id_points, text=self.points)

    def set_coords(self):
        canv.coords(
            self.id,
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r
        )

    def move(self):
        self.x += self.vx
        self.y += self.vy
        if abs(self.Y0 - self.y) > self.a:
            self.vy *= -1
            self.y += self.vy

        self.set_coords()



screen1 = canv.create_text(400, 300, text='', font='28')


def new_game(event=''):
    targets = [target() for i in range(3)]
    bullet = 0
    balls = []
    g1 = gun(balls, bullet)
    canv.bind('<Button-1>', g1.fire2_start)
    canv.bind('<ButtonRelease-1>', g1.fire2_end)
    canv.bind('<Motion>', g1.targetting)

    z = 0.03
    lives = 0
    for i, t in enumerate(targets):
        targets[i].live = 1
        lives += 1

    while lives or balls:
        lives = 0
        for i, t in enumerate(targets):
            lives += 1
            t.move()
        for i, b in enumerate(balls):
            b.move()
            if b.collisions >= 15:
                ball.__del__(b)
                balls.remove(b)
            for j, t in enumerate(targets):
                if b.hittest(targets[j]) and targets[j].live:
                    targets[j].live = 0
                    targets[j].hit()
                    targets.remove(t)
                    ball.__del__(b)
                    balls.remove(b)
                if not targets:
                    canv.bind('<Button-1>', '')
                    canv.bind('<ButtonRelease-1>', '')
                    canv.itemconfig(screen1, text='Вы уничтожили цель за ' + str(g1.bullet) + ' выстрелов')
        canv.update()
        time.sleep(z)
        g1.targetting()
        g1.power_up()
    time.sleep(1)
    canv.itemconfig(screen1, text='')
    canv.delete(g1.id)
    root.after(1, new_game)


new_game()

tk.mainloop()
