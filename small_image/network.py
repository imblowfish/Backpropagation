from neuron import Neuron
from random import *

#класс нейронной сети
class NeuronNetwork:
	hidden_layers = [6, 3, 4] #количество нейронов в скрытых слоях
	neurons = [] #матрица нейронов
	layers_num = len(hidden_layers) + 2 #количество нейронов в сети, учитываем входной и выходной слои
	summary_errors = None
	test_errors = None
	
	#------инициализация нейронов-----------
	def init_neurons(self, inputs, outputs):
		self.neurons = []
		#создаем нейроны ходного слоя
		slope = random()
		self.neurons.append([Neuron(slope, is_input=True) for i in range(inputs)])
		#скрытых слоев
		for num_in_layer in self.hidden_layers:
			slope = 2
			self.neurons.append([Neuron(slope) for j in range(num_in_layer)])
		#выходного слоя
		slope = 3
		self.neurons.append([Neuron(slope, is_output=True) for i in range(outputs)])
		#инициализируем веса
		self.connect_layers()
		
	#----связывание весами---
	def connect_layers(self): #
		for i in range(0, len(self.neurons) - 1):
			#проходим каждый нерон в текущем слое...
			for neuron in self.neurons[i]:
				for next_neuron in self.neurons[i+1]:
					# ...и добавляем каждому нейрону в следующем слое связь с ним
					next_neuron.add_weight()
					
	#-очистка входных сигналов-
	def clear_all_inputs(self): #
		for layer in self.neurons:
			for neuron in layer:
				neuron.inputs = None
				
	#-----поиск изображения------
	def find(self, example):
		image = []
		for row in example:
			image += row
		output, error = self.iteration(image)
		return output
		
	#-----обучение нейронной сети-------
	def teach(self, images, iterations): #С ЭТОЙ ФУНКЦИИ НАЧИНАЕТСЯ ОБУЧЕНИЕ СЕТИ
		self.summary_errors = []
		self.test_errors = []
		#инициализаруем нейроны
		self.init_neurons(len(images[0][0]) * len(images[0]), len(images))
		#проходим iterations эпох обучения
		for i in range(0, iterations):
			summary_error = 0
			test_error = 0
			for j in range(len(images)):
				#берем случайное изображение из обучающей выборки
				idx = j
				#создаем вектор проверки ошибок
				t_vector = []
				for k in range(0, len(images)):
					if k == idx:
						t_vector.append(1.0)
					else:
						t_vector.append(0.0)
				#преобразуем изображение из двумерного массива в одномерный для подачи на вход нейронам
				image = []
				for row in images[idx]:
					image += row
				#проводим одну итерацию и получаем выходные сигналы, а также квадрат ошибки выходов сети для образца
				output, quad_error = self.iteration(image, t_vector)
				summary_error += quad_error
				
			#подача искаженных образцов
			for j in range(len(images)*2):
				idx = j%len(images)
				t_vector = [0, 0, 0, 0]
				image = []
				#искажение изображения
				for row in images[idx]:
					modified_row = row.copy()
					for bit in modified_row:
						if random() >= 0.7:
							bit ^= 1
					image += modified_row
				output, quad_error = self.iteration(image, t_vector, test=True)
				test_error += sum(output)
				
			self.summary_errors.append(summary_error)
			self.test_errors.append(summary_error + test_error)
				
	#-----------одна итерация-----------------
	def iteration(self, image, t_vector=None, test=False): #одна эпоха обучения
		#очищаем все входные сигналы нейронов
		self.clear_all_inputs()
		#прямой проход, по выходу получаем вектор ошибок выходов сети и суммарную ошибку сети
		errors, quad_error = self.forward(image, t_vector, test)
		out_signals = []
		for neuron in self.neurons[-1]:
			out_signals.append(neuron.output())
		if t_vector and not test:
			self.backward(errors)
		#возвращаем выходные сигналы и суммарную ошибку сети
		return out_signals, quad_error
		
	#---------прямой проход------------	
	def forward(self, image, t_vector=None, test=False): #
		#подаем каждому нейрону входного слоя бит в изображении
		for i in range(len(self.neurons[0])):
			self.neurons[0][i].input(image[i])
		#по каждому слою
		for i in range(self.layers_num-1):
			#каждый нейрон текущего слоя...
			for neuron in self.neurons[i]:
				for next_neuron in self.neurons[i+1]:
					#...отправляет свой выход нейрону следующего слоя
					next_neuron.input(neuron.output())
		if t_vector or test:
			errors = []
			quad_error = 0
			for i in range(len(self.neurons[-1])):
				#желаемый_выходной_сигнал - реальный_выходной_сигнал
				output_error =  self.neurons[-1][i].output() - t_vector[i]
				errors.append(output_error)
				#суммарная ошибка это сумма (желаемый_выходной_сигнал - реальный_выходной_сигнал)^2
				quad_error += (output_error)**2
			return errors, quad_error
		return None, None
		
	#------обратный проход-------	
	def backward(self, errors): #
		#отправляем ошибку выхода каждому выходу
		for i in range(len(self.neurons[-1])):
			self.neurons[-1][i].input_error(errors[i])
			
		#по каждому слою начиная с предпоследнего
		for i in range(len(self.neurons)-2, -1, -1):
			#по каждому нейрону слоя i
			for j in range(len(self.neurons[i])):
				error_signal = 0
				#получаем сумму ошибоку нейронов слоя i+1
				#результат output_error это вес_связи_нейрона_ij_с_нейроном_ik * величину_ошибки_нейрона_ik
				for k in range(len(self.neurons[i+1])):
					error_signal += self.neurons[i+1][k].output_error(j)
				#отправляем результат на вход нейрону ij
				error_signal *= self.neurons[i][j].activate_func_deriv()
				self.neurons[i][j].input_error(error_signal)
				
		# обновление весов
		for i in range(1, len(self.neurons)):
			for j in range(len(self.neurons[i])):
				self.neurons[i][j].correct_weights()
				
#----NeuronNetwork----				