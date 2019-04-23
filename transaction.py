import ecdsa, binascii

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
		if (self.value <= 0):
			raise ValueError('Invalid transaction value')

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
		sk = ecdsa.SigningKey.from_string(
			binascii.unhexlify(key), 
			curve=ecdsa.SECP256k1)
		vk = binascii.hexlify(sk.get_verifying_key().to_string()).decode()
		sig = binascii.hexlify(sk.sign(bytes.fromhex(res))).decode()
		res += vk + sig
		return res

	def deserialize(self, raw):
		print (raw)
		self.version = raw[0:2]
		self.sender = raw[2:66]
		self.recipient = raw[66:130]
		self.value = int(raw[130:134], 16)
		self.verif_key = raw[134:262]
		self.signature = raw[262:]

	def display(self):
		print ('Sender:', self.sender)
		print ('Recipient', self.recipient)
		print ('Value', self.value)
