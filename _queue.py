class Queue(object):
	"""docstring for Queue array based of FIFO"""
	def __init__(self):
		self.items = []

	def __str__(self):
		return str(self.items)

	def show(self):
		return self.items

	def isEmpty(self):
		return self.items == []

	def push(self, item):
		self.items.insert(0,item)

	def pop(self):
		return self.items.pop()

	def length(self):
		return len(self.items)
