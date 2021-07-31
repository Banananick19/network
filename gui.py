import matplotlib.pyplot as plt
import numpy

from GUI.widgets import *
from GUI.guimixin import *
from GUI.guimaker import GuiMakerFrameMenu
from config import MAIN_FRAME_COLOR
import math
import tkinter as tk
import tkinter.messagebox as mb
from time import sleep


class Window(GuiMakerFrameMenu):

    def __init__(self, root):
        super().__init__(root)

    def make_widgets(self):
        pass

    def start(self):
        pass
        #self.menu_bar = menu_bar

class FlatButton(tk.Label):
    def __init__(self, *args, x, y, down="#000000", up="#ffffff", command=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.down =down
        self.up = up
        self.isdown = False

        if command:
            self.bind('<1>', command)

        self.bind('<Button-1>', self.mouse_in)

    def mouse_in(self, event):
        if self.isdown:
            self.isdown = False
            self.config(bg=self.up)
        else:
            self.isdown = True
            self.config(bg=self.down)



class MainWindow(Window):

    def __init__(self, nn, root=None):
        self.nn = nn
        self.buttons = []

        super().__init__(root)


    def delete_widgets(self):
        for e in self.main_frame.pack_slaves():
            e.destroy()

    def make_widgets(self):
        if not hasattr(self, 'main_frame'):
            self.main_frame = frame(self, bg=MAIN_FRAME_COLOR)
        width = int(math.sqrt(self.nn.inputnodes))
        for i in range(width+1):
            self.main_frame.grid_columnconfigure(i)
            self.main_frame.grid_rowconfigure(i)
        for x in range(0, width):
            for y in range(0, width):
                but = FlatButton(self.main_frame, x=x, y=y, bg="#ffffff", borderwidth = 1, width=3, relief=tk.RAISED, down="#000000", up="#ffffff",
                                 command=lambda event: print('Hello!'))
                but.grid(column = y, row=x, sticky=tk.W+tk.E)
                self.buttons.append(but)
        Button(self.main_frame, command=self.make_query).grid(column = width+1, row=width+1)
        Button( self.main_frame, text="reverse ",command=self.make_query_reverse).grid(column=width - 1, row=width + 1)

    def make_query_reverse(self, event=''):
        inputs = [0.99, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01]
        print(inputs)
        image_data = self.nn.query_reverse(inputs)
        plt.imshow(image_data.reshape(28,28), cmap='Greys', interpolation='None')


    def make_query(self, event=''):
        inputs = [255 if i.isdown else 0 for i in self.buttons]
        inputs = (numpy.asfarray(inputs) / 255 * 0.99) + 0.01
        print(inputs)
        outputs = self.nn.query(inputs)
        answer = numpy.argmax(outputs)
        mb.showinfo("Title", str(answer))


