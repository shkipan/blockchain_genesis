import ecdsa

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

	def serialize(self, key):
		val = hex(self.value).replace('0x', '')
		res = (
			hex(self.version).replace('0x', '') + 
			'0' * (coded_length - len(self.sender)) +
			self.sender +
			'0' * (coded_length - len(self.recipient)) +
			self.recipient +
			'0' * (4 - len(val)) +
			val
			)
		return res

	def deserialize(self, raw):
		self.version = raw[0:2]
		self.sender = raw[2:66]
		self.recipient = raw[66:130]
		self.value = int(raw[130:134], 16)

	def display(self):
		print ('Sender:', self.sender)
		print ('Recipient', self.recipient)
		print ('Value', self.value)
