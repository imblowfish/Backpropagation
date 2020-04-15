from math import *
from random import *

#класс нейрона
class Neuron: 
	alpha = 0.1 #скорость обучения
	slope = None #угол наклона сигмоды
	
	inputs = None #входные сигналы нейрона
	weights = None #веса связи нейрона с нейронами предыдущего слоя
	error = None #величина ошибки нейрона
	out = None
	deltas = None
	is_input = None
	is_output = None
	
	#------------инициализация нейрона------------------
	def __init__(self, slope, is_input=False, is_output=False):
		#указываем входной он или выходной
		#либо ни тот не тот, а значит скрытый
		self.is_input, self.is_output = is_input, is_output
		#генерируем случайный коэффициент наклона сигмоиды
		self.slope = slope
		
	#--добавление веса---
	def add_weight(self):
		if not self.weights:
			self.weights = []
			self.deltas = []
		#добавляем вес равный случайному малому числу
		self.weights.append(random()-0.5) # от 0 до 1в
		self.deltas.append(0)
		
	#-получение входного сигнала-
	def input(self, signal):
		if not self.inputs:
			self.inputs = []
		#добавляем нейрону поступивший входной сигнал
		self.inputs.append(signal)
		
	#-выход нейрона--
	def output(self):
		#если нейрон из входного слоя, то выход = входу
		if self.is_input:
			self.out = self.inputs[0]
			return self.out
		#иначе рассчитываем сумму sj по формуле из методички на стр.64
		sj = 0
		for i in range(len(self.inputs)):
			sj += self.inputs[i] * self.weights[i]
		#применяем к сумме активационную функцию
		self.out = self.activate_func(sj)
		#и возвращаем выход нейрона
		return self.out
		
	#---получениесигнала ошибки---
	def input_error(self, signal):
		#домножение на производную ф-ии активации, формула 5.1 в методичке на стр.63
		self.error = signal
		
	#---выход ошибки нейрона----
	def output_error(self, idx):
		#вычисляем дельту для индекса
		self.deltas[idx] = self.alpha * self.inputs[idx] * self.error
		#если выходной слой, то выход_ошибка = входу_ошибка
		if self.is_output:
			return self.error * self.weights[idx]
		#иначе умножаем на вес связи с нейроном idx
		return self.error * self.weights[idx]
		
	#-----коррекция весов-----
	def correct_weights(self):
		#если входной нейрон, значит нет входных весов, а значит не требуется коррекции
		if self.is_input:
			return
		#рассчитываем дельту изменения весов для коррекции весов
		#для каждого входного веса нейрона
		for i in range(len(self.weights)):
			# прибавляем дельту
			self.weights[i] -= self.deltas[i]
			self.deltas[i] = 0
			
	#-----------f(x)-----------
	def activate_func(self, x):
		return 1/(1+exp(-self.slope * x))
		
	#-------------f'(x)-----------
	def activate_func_deriv(self):
		return self.slope * self.out * (1 - self.out)
		
#----Neuron----