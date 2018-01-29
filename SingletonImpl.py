from time import ctime
from copy import copy


"""
Module contain:
3 constants or identification type of events (normal 0, remark 1, error 2)
class Event for containing type of events and their properties (time, type, message) with method of converting to str
class Logger, which implement Logger in program
and function singleton. It is uses like decorator for implementation of singleton object
"""

normal = 0
remark = 1
error = 2


class Event:
	"""
	Class contain constructor
	and special method for converting object to str
	attributes of time, type and message of event
	"""
	def __init__(self, type, message=''):
		"""
		Make instance of event
		:param type: identify type of event
		:param message: optional param which contain message attached to event
		"""
		self.time = ctime()
		self.type = type
		self.message = message

	def __str__(self):
		"""
		special method for converting object to str
		:return: string in format
		"
		time type
		Comment:
		...
		"
		"""
		format = """{0} {1}\nComment:\n{2}\n"""
		if self.type == 0:
			type = "normal"
		elif self.type == 1:
			type = "remark"
		elif self.type == 2:
			type = "error"
		else:
			type = "unknown event %d" % self.type

		return format.format(self.time, type, self.message)


def singleton(klass):
	"""
	Function which uses for creating singleton object
	Contain nested function, which returned
	dictionary instances which contain conformity between classes and their single instances
	this object is kept because it is in the enclosing function scope
	:param klass:
	:return:
	"""
	instances = {}

	def getInstance(*args, **kwargs):
		nonlocal instances
		if klass in instances:
			return instances[klass]
		else:
			inst = klass(*args, **kwargs)
			instances[klass] = inst
			return inst

	return getInstance


@singleton
class Logger:
	"""
	Class decorated by singleton function
	Contain:
	1 construction
	method event for make note in log
	method get_log for getting last 10 records in log
	"""
	def __init__(self, file=None):
		"""
		Initialize Logger instance
		:param file: optional file for synchronisation log file with file system (if param absent -- doesn't make sync)
		"""
		if file:
			self.sync = True
			self.file = file
		else:
			self.sync = False

		self.last_events = [None for _ in range(10)]
		self.last = 0

	def event(self, type, message=None):
		"""
		Make record in log file with type, time of recording and attached message
		:param type: type of event
		:param message: attached message to event (optional)
		:return:
		"""
		event = Event(type, message)
		self.last_events[self.last] = event
		self.last = (self.last + 1) % 10
		if self.sync:
			file = open(self.file, 'w')
			file.write('\n'.join(self.get_log()))
			file.close()

	def get_log(self, format=True):
		"""
		Method for get list of 10 last records in log
		:param format: if format is True (default) return formatted log, else list of events
		:return: list of last 10 events in log
		"""
		if format:
			return map(str, filter((lambda x: x), self.last_events[self.last:] + self.last_events[:self.last]))
		else:
			return copy(self.last_events)


if __name__ == "__main__":
	inst = Logger("log.txt")
	inst.event(1)
	inst.event(2, "com1")
	inst.event(0, "com2")
	inst2 = Logger()
	inst2.event(0, "com3")
	print('\n'.join(inst.get_log()), "\n")
	print('\n'.join(inst2.get_log()))


