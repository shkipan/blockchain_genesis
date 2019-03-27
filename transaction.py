class Transaction:
	sender = None;
	recipient = None;
	value = 0;

	def __init__(self, s, r, v):
		self.sender = s
		self.recipient = r
		self.value = v

	def send(self, key):
		print ('sending', self.value, 'with key', key)

	def display(self):
		print ('Sender:', self.sender)
		print ('Recipient', self.recipient)
		print ('Value', self.value)
