from tkinter import *
import random
import time
class Ball:
    def __init__(self, canvas, diameter, color, x0, y0, balls=None):
        self.canvas = canvas
        self.diameter = diameter
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        center = (self.canvas_height / 2, self.canvas_width / 2)
        self.x = random.randint(1, 3)
        self.y = random.randint(1, 3)
        self.id = canvas.create_oval(0, 0, self.diameter, self.diameter, fill=color)
        self.canvas.move(self.id, x0, y0)
        #self.hit_bottom = False
        self.balls = balls

    def draw2(self, b):
        self.canvas.move(self.id, self.x, self.y)
        b.canvas.move(b.id, b.x, b.y)
        pos = self.canvas.coords(self.id)
        pos2 = self.canvas.coords(b.id)
        if pos[3] > self.canvas_height:
            self.y = -self.y
        elif pos[2] > self.canvas_width:
            self.x = -self.x
        elif pos[1] < 0:
            self.y = -self.y
        elif pos[0] < 0:
            self.x = - self.x
        if pos2[3] > self.canvas_height:
            self.y = -self.y
        elif pos2[2] > self.canvas_width:
            self.x = -self.x
        elif pos2[1] < 0:
            self.y = -self.y
        elif pos2[0] < 0:
            self.x = - self.x
        d = self.diameter
        if pos[2] > pos2[0] and pos[0]<pos2[2] and pos[3]-pos2[3]<=d and pos[3]-pos2[3]>=-d:
            a = self.x
            self.x = b.x
            b.x = a
        if pos2[2] > pos[0] and pos2[0]<pos2[2] and pos[3]-pos2[3]<=d and pos[3]-pos2[3]>=-d:
            a = self.x
            self.x = b.x
            b.x = a
        if pos[1] > pos2[3] and pos[3]<pos2[1] and pos[2]-pos2[2]<=d and pos[2]-pos2[2]>=-d:
            a = self.y
            self.y = b.y
            b.y = a
        if pos2[1] < pos[3] and pos2[3]>pos[1] and pos[2]-pos2[2]<=d and pos[2]-pos2[2]>=-d:
            a = self.y
            self.y = b.y
            b.y = a

        '''elif pos[3] > pos2[1] and pos[1]<pos2[3]:
            self.y = -self.y
            b.y = - b.y
        elif pos[1] < pos2[3] and pos[3] > pos2[1]:
            self.y = -self.y
            b.y = - b.y
        elif pos[0] < pos2[2] and pos[2] > pos2[0]:
            self.x = -self.x
            b.x = - b.x'''
        #else:
        #self.x = random.randint(-30, 30)
        #self.y = random.randint(-30, 30)
    def draw(self):
        self.canvas.move(self.id, self.x, self.y)
        pos = self.canvas.coords(self.id)
        if pos[3] > self.canvas_height:
            self.y = -self.y
        elif pos[2] > self.canvas_width:
            self.x = -self.x
        elif pos[1] < 0:
            self.y = -self.y
        elif pos[0] < 0:
            self.x = - self.x
        #else:
        #self.x = random.randint(-30, 30)
        #self.y = random.randint(-30, 30)
if __name__ == '__main__':
    tk = Tk()
    tk.title('Gas')
    tk.resizable(0, 0) #
    tk.wm_attributes('-topmost', 1) #
    canvas = Canvas(tk, width=800, height=600, bd=0, highlightthickness=0) # bd, highlightthickness
    canvas.pack()
    tk.update() #
    balls = []
    #for i in range(2):
    ball = Ball(canvas, 80, 'red', 100, 100)
    balls.append(ball)
    ball = Ball(canvas, 80, 'blue', 200, 200)
    balls.append(ball)
    ball = Ball(canvas, 80, 'green', 300, 300)
    balls.append(ball)
    while True:
        #for ball in balls:
        balls[0].draw2(balls[1])
        #balls[1].draw2(balls[0])
        balls[1].draw2(balls[2])
        #balls[2].draw2(balls[1])
        balls[2].draw2(balls[0])
        #balls[0].draw2(balls[2])
        #ball.draw()
        tk.update_idletasks() #
        tk.update() #
        time.sleep(0.02)