from SingletonImpl import Logger, error, normal, remark
from random import randint
from threading import Thread, Semaphore
from time import sleep, clock
import os
import signal

stop = False  # To stop threads
sem = Semaphore(1)  # Semaphore for sync access to Logger
semstop = Semaphore(1)  # Semaphore for sync access to stop


def show_log():
	"""
	Function showing log in console (last 10 records in log)
	:return: None
	"""
	if os.name == 'nt':
		os.system('cls')
	elif os.name == 'posix':
		os.system('clear')
	sem.acquire()
	loglist = Logger().get_log()
	sem.release()
	print('\n'.join(loglist))


def stopper(signum, frame):
	"""
	Handler for keyboard interruption to stop threads
	:param signum:
	:param frame:
	:return:
	"""
	global stop
	semstop.acquire()
	stop = True
	semstop.release()


def error_maker():
	"""
	Function which making error events
	:return:
	"""
	global stop
	log = Logger('log.txt')
	x = [i for i in range(10)]  # list with maximum index 9!
	semstop.acquire()
	while not stop:
		semstop.release()
		sleep(0.5)
		try:
			error_type = randint(0, 2)  # choice of error
			if error_type == 0:
				x[randint(0, 10)] = randint(0, 10)  # index out of range if 10

			elif error_type ==1:
				if randint(0, 10) == 0:
					"123"/3  # unsupported operation for this types

			elif error_type==2:
				if randint(0, 10) == 0:
					print(unknown_var)  # unknown var

		except IndexError as err:  # three exceptions for make records in lof
			sem.acquire()
			log.event(error, err)
			sem.release()

		except TypeError as err:
			sem.acquire()
			log.event(error, err)
			sem.release()

		except NameError as err:
			sem.acquire()
			log.event(error, err)
			sem.release()

		semstop.acquire()
	semstop.release()


def normal_maker():
	"""
	Function which making normal events
	:return:
	"""
	global stop
	log = Logger("log.txt")
	semstop.acquire()
	while not stop:
		semstop.release()
		sleep(0.5)
		if randint(0, 10) == 0:
			sem.acquire()
			log.event(normal, "Oh my god\nIt's so awesome program")
			sem.release()

		semstop.acquire()
	semstop.release()


def remark_maker():
	"""
	Function which making remark events
	:return:
	"""
	global stop
	log = Logger("log.txt")
	semstop.acquire()
	while not stop:
		semstop.release()
		sleep(0.5)
		if randint(0, 10) == 0:
			sem.acquire()
			log.event(remark, "If anyone wanted ter find out some stuff,\nall they’d have ter do would be ter follow the spiders.\nThat’d lead ’em right!\nThat’s all I’m sayin")
			sem.release()

		semstop.acquire()
	semstop.release()


if __name__ == "__main__":
	signal.signal(signal.SIGINT, stopper)  # Set handler for keyboard interrupt

	err_thread = Thread(target=error_maker)
	norm_thread = Thread(target=normal_maker)
	rem_thread = Thread(target=remark_maker)
	err_thread.start()
	norm_thread.start()
	rem_thread.start()

	show_log()
	last_log_show = clock()
	semstop.acquire()
	while not stop:  # Refresh screen with last logs, until stop == True
		semstop.release()
		sleep(0.1)
		if clock() - last_log_show > 1:
			show_log()
			last_log_show = clock()
		semstop.acquire()
	semstop.release()

	err_thread.join()
	norm_thread.join()
	rem_thread.join()
	Logger().event(3, "Ho-ho-ho")  # Make last unknown event

	show_log()  # show last log
