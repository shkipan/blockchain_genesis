coded_length = 64

class Transaction:
	sender = None;
	recipient = None;
	value = 0;
	version = 42

	def __init__(self, s, r, v):
		self.sender = s
		self.recipient = r
		self.value = int(v)

	def send(self, key):
		print ('sending', self.value, 'with key', key)
		res = (
			hex(self.version).replace('0x', '') + 
			'0' * (coded_length - len(self.sender)) +
			self.sender +
			'0' * (coded_length - len(self.recipient)) +
			self.recipient +
			hex(self.value).replace('0x', '')
			)
		print (res)

	def display(self):
		print ('Sender:', self.sender)
		print ('Recipient', self.recipient)
		print ('Value', self.value)
