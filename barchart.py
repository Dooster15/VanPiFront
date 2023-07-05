import tkinter as tk   
import time
from tkinter import ttk

# parent = tk.Tk()
# parent.configure(background='blue')
# parent.geometry('600x480')
# can = tk.Canvas(parent,bg='white',width=600, height=480)

# can.create_rectangle(10,20,30,40,fill='green',outline="")

# can.place(x=20,y=20)

class tk_bar_graph:
    def __init__(self,x_coord,y_coord,height,width,num_col,padding,parent):
        self.height = height
        self.width = width
        self.num_col = num_col
        self.padding = padding
        self.parent = parent

        graph_width = ((self.width + self.padding) * num_col) + self.padding
        # print(graph_width)
        self.canvas = tk.Canvas(self.parent,bg='white',width=graph_width,height=self.height+(self.padding*2), borderwidth=0,highlightthickness=0)

        x = 0
        y = 0
        self.bars = []
        for i in range(num_col):
            x0 = (self.padding + x)
            y0 = (self.height - 20 + self.padding)
            x1 = (self.padding + x + self.width)
            y1 = self.height + self.padding
            # print(f"{x0},{y0},{x1},{y1}")
            bar = self.canvas.create_rectangle(x0,y0,x1,y1,fill='green',outline='')
            self.bars.append(bar)
            x += (self.padding + self.width)
        # print(x)
        self.canvas.place(x= x_coord, y = y_coord)

    def bar_val(self,bar_num,value): # value expressed between 0 and height
        if value > self.height:
            print('Error height value to large')
        bar = self.bars[bar_num]
        if value < 0:
            self.canvas.itemconfig(bar,fill='red')
            value = abs(value)
        x0,y0,x1,y1 = self.canvas.coords(bar)
        y0 = y1 - value
        self.canvas.coords(bar,x0,y0,x1,y1)

# graph = tk_bar_graph(10,10,100,5,60,1,parent)

# z = 0
# while True:
#     if z >= 100:
#         z = 0
#     else:
#         z+=1
#     parent.update()
#     graph.bar_val(0,z)
#     time.sleep(.01)