from network import NeuronNetwork
from interface import (
	Interface,
	BMPParser
)

filename = "Sport18.bmp"
images = BMPParser.from_bmp_to_array(filename)
iters = 150 #количество эпох обучения

neuron_network = None

def start_teach():
	global screen, neuron_network, images, iters, error_graphic, test_error_graphic
	neuron_network = NeuronNetwork()
	neuron_network.teach(images, iters)
	screen.draw_graphic(error_graphic, "График ошибок", "№ эпохи", "Ошибка", range(0, len(neuron_network.summary_errors)), neuron_network.summary_errors)
	screen.draw_graphic(test_error_graphic, "График ошибок тестирования", "№ эпохи", "Ошибка тестирования", range(0, len(neuron_network.test_errors)), neuron_network.test_errors)
	
def start_test():
	global neuron_network, screen, images
	if not neuron_network:
		screen.show_error("Ошибка сети", "Нейронная сеть не проинициализирована")
		return
	test_screen = screen.create_test_screen(neuron_network, images)
	

screen = Interface("700x500")
# кнопка обучения
screen.add_button("Обучение", 10, 10, start_teach)
# кнопка проверки сети
screen.add_button("Тестирование сети", 10, 40, start_test)
# добавление графика ошибок
error_graphic = screen.add_graphic(3, 2, 400, 30)
# добавление графика ошибок тестирования
test_error_graphic = screen.add_graphic(3, 2, 400, 270)

screen.start()

#добавить интерфейс
#отображение образцов
#отображение графиков

