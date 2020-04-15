#from graphics import *
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
	FigureCanvasTkAgg, 
	NavigationToolbar2Tk
)
from matplotlib.figure import Figure
from random import *
import copy

class TestScreen:
	network = None
	datas = None
	now_data = None
	now_idx = None
	root = None
	is_distort = None
	def __init__(self, network, datas):
		self.root = tk.Tk()
		self.root.geometry("500x500")
		self.root.title("Тестирование")
		
		self.network = network
		self.datas = datas.copy()
		self.now_idx = 0
		self.now_data = copy.deepcopy(self.datas[self.now_idx])
		self.is_distort = False
		
		self.create_viewer()
		self.create_buttons()
		self.create_text_output()
		
		self.view_now_data()
		
	def view_now_data(self):
		n = len(self.now_data[0])
		m = len(self.now_data)
		width = int(self.canvas["width"])
		height = int(self.canvas["height"])
		self.canvas.delete("all")
		space_x = width/n
		space_y = height/m
		y = 0
		for i in range(len(self.now_data)):
			x = 0
			for j in range(len(self.now_data[i])):
				if self.now_data[i][j] == 1:
					self.canvas.create_rectangle(x, y, x+space_x, y+space_y, fill="black")
				else:
					self.canvas.create_rectangle(x, y, x+space_x, y+space_y, outline="black")
				x += space_x
			y += space_y
	
	def next_data(self):
		if self.now_idx + 1 >= len(self.datas):
			return
		self.now_idx += 1
		self.now_data = copy.deepcopy(self.datas[self.now_idx])
		self.is_distort = False
		self.view_now_data()
		
	def prev_data(self):
		if self.now_idx - 1 < 0:
			return
		self.now_idx -= 1
		self.now_data = copy.deepcopy(self.datas[self.now_idx])
		self.is_distort = False
		self.view_now_data()
		
	def distort(self):
		for i in range(0, len(self.now_data)):
			for j in range(0, len(self.now_data[i])):
				if random() > 0.3:
					self.is_distort = True
					self.now_data[i][j] ^= 1
		self.view_now_data()
		
	def find(self):
		output = self.network.find(self.now_data)
		text = f"Выходы сети\nВыбранное изображение {self.now_idx+1}\n"
		if self.is_distort:
			text += "Изображение было искажено\n"
		text += "["
		for out in output:
			text += f"{out:.3f} "
		text += "]"
		self.output_label["text"] = text
		
	def create_viewer(self):
		self.canvas = tk.Canvas(self.root, width=240, height=240, bg="white")
		self.canvas.place(relx=0.3, rely=0)
		
	def create_buttons(self):
		self.prev_btn = tk.Button(self.root, text="<", command=self.prev_data)
		self.prev_btn.place(relx=0, rely=0.5)
		
		self.distort_btn = tk.Button(self.root, text="Исказить", command=self.distort)
		self.distort_btn.place(relx=0.05, rely=0.5, relwidth=0.9)
		
		self.next_btn = tk.Button(self.root, text=">", command=self.next_data)
		self.next_btn.place(relx=0.96, rely=0.5)
		
		self.input_btn = tk.Button(self.root, text="Подать образец", command=self.find)
		self.input_btn.place(relx=0, rely=0.57, relwidth= 1)
	
	def create_text_output(self):
		self.output_label = tk.Label(self.root, text="Выходы сети")
		self.output_label.place(relx=0.3, rely=0.7)
		
class Interface:
	root = None
	buttons = []
	textboxes = []
	radiobuttons = []
	labels = []
	
	def __init__(self, size):
		self.root = tk.Tk()
		self.root.wm_title("Лабораторная 2")
		self.root.geometry(size)
	def start(self):
		tk.mainloop()
	def show_error(self, title, text):
		tk.messagebox.showwarning(title=title, message=text)
	#-------------------------------------------------
	def add_graphic(self,width, height, pos_x, pos_y):				#добавление графика
		fig = Figure(figsize=(width,height),dpi=100)
		ax = fig.add_subplot()
		canvas = FigureCanvasTkAgg(fig, master=self.root)
		canvas.get_tk_widget().place(x=pos_x, y=pos_y)
		canvas.draw()
		return canvas
	#-----------------------------------------------------------
	def draw_graphic(self, canvas, title, xlabel, ylabel, x, y):	#рисование значений на графике
		ax = canvas.figure.axes[0]
		ax.clear()
		ax.plot(x, y, alpha=0.7, c="#0000FF")
		ax.set_xlabel(xlabel)
		ax.set_ylabel(ylabel)
		ax.set_title(title)
		for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] + ax.get_xticklabels() + ax.get_yticklabels()):
			item.set_fontsize(6)
		canvas.draw()
	#------------------------------------------------------
	def add_button(self, text, pos_x, pos_y, command=None):
		b = tk.Button(self.root, text=text, font=("Helvetica","8"), command=command)
		b.place(x=pos_x, y=pos_y)
		self.buttons.append(b)
		return b
	def create_test_screen(self, network, images):
		return TestScreen(network, images)
#---Interface END---
			
	
		
	