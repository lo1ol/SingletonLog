from time import ctime
from copy import copy

normal = 0
remark = 1
error = 2

class Event:
	def __init__(self, type, message):
		self.time = ctime()
		self.type = type
		self.message = message

	def __str__(self):
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
	def __init__(self, file=None):
		if file:
			self.sync = True
			self.file = file
		else:
			self.sync = False

		self.last_events = [None for _ in range(10)]
		self.last = 0

	def event(self, type, message = None):
		if type not in {0, 1, 2}:
			raise RuntimeWarning("Unknown event")
		event = Event(type, message)
		self.last_events[self.last] = event
		self.last = (self.last + 1) % 10
		if self.sync:
			file = open(self.file, 'w')
			file.write('\n'.join(self.get_log()))
			file.close()

	def get_log(self, format = True):
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


