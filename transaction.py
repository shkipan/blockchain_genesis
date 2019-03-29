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

	def send(self, key):
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
		sk = ecdsa.SigningKey.from_string(bytes.fromhex(key), curve=ecdsa.SECP256k1)
		res_bytes = bytes.fromhex(res)
		signature = sk.sign(res.encode('ascii'))
		res += signature.hex()
#		print ('signature', signature)
		print ('raw transaction\n' + res)
#		print ('ver', res[0:2])
#		print ('sen', res[2:66])
#		print ('rec', res[66:130])
#		print ('val', int(res[130:134], 16))
#		print ('sig', res[134:])
#		print ('signature', bytes.fromhex(res[134:]))
		vk = sk.get_verifying_key()
		assert vk.verify(bytes.fromhex(res[134:]), res[:134].encode('ascii'))

	def display(self):
		print ('Sender:', self.sender)
		print ('Recipient', self.recipient)
		print ('Value', self.value)
