import hashlib
from flask import json
from transaction import Transaction

max_nonce = 10000
target = 1

class Block:
	def calculate_hash(self):
		for non in range(max_nonce):
			to_hash = (
				hex(self.version).replace('0x', '') +
				hex(non).replace('0x', '') +
				hex(self.heigth).replace('0x', '') +
				self.prev_hash
			)
			for i in self.raw_transactions:
				to_hash += i
			bl_hash = hashlib.sha256(to_hash.encode('ascii')).hexdigest()
			if bl_hash[:target] == '0' * target:
				self.bl_hash = bl_hash
				return			

	def __init__(self, trans, ph, hei):
		self.version = 42
		self.nonce = 0
		self.heigth = hei
		self.prev_hash = ph
		self.raw_transactions = []
		self.transactions = []
		for i in trans:
			self.raw_transactions.append(i)
			tr = Transaction("","", 1)
			tr.deserialize(i)
			self.transactions.append(tr)
		Block.calculate_hash(self)

	def display(self):
		print ('vers', self.version)
		print ('heig', self.heigth)
		print ('nonc', self.nonce)
		print ('trans count', len(self.raw_transactions))
		for i in self.raw_transactions:
			print ('tran', i)
		print ('hash', self.bl_hash)
		print ('prev_hash', self.prev_hash)

	def to_json(self):
		return {
			'version': self.version,
			'heigth': self.heigth,
			'nonce': self.nonce,
			'hash': self.bl_hash,
			'prev_hash': self.prev_hash,
			'raw_transactions': self.raw_transactions
		}

	def from_json(self, js_data):
		self.version = js_data['version']
		self.heigth = js_data['heigth']
		self.nonce = js_data['nonce']
		self.bl_hash = js_data['hash']
		self.prev_hash = js_data['prev_hash']
		for i in js_data['raw_transactions']:
			self.raw_transactions.append(i)
			tr = Transaction("","", 1)
			tr.deserialize(i)
			self.transactions.append(tr)
	
class Blockchain:
	last_hash = '0' * 64
	curr_heigth = 0
	blocks = []

	def add_block(self, transacts):
		bl = Block(transacts, self.last_hash, self.curr_heigth)
		self.blocks.append(bl)
		self.curr_heigth += 1
		self.last_hash = bl.bl_hash

	def display(self):
		print ('total_heigth', self.curr_heigth)
		print ('last_hash', self.last_hash)
		print ('blocks')
		for x in self.blocks:
			x.display()

	def output_json(self):
		bl_js = []
		for bl in self.blocks:
			bl_js.append(bl.to_json())
		return {
			'last_hash': self.last_hash,
			'curr_heigth': self.curr_heigth,
			'blocks': bl_js
		}

	def read_from_file(self, filename):
		try:
			with open(filename, 'r') as f:
				data = json.loads(f.read())
				self.last_hash = data['last_hash']
				self.curr_heigth = data['curr_heigth']
				for i in data['blocks']:
					bl = Block([], "0", 0)
					bl.from_json(i)
					self.blocks.append(bl)
		except FileNotFoundError:
			print ('Invalid filename')
		except json.decoder.JSONDecodeError:
			print ('Invalid content of file')

if __name__ == '__main__':
	'''
	chain = Blockchain()
	chain.add_block(['2ac5e3e47d28c55ecfb4d4b54455d0259b61679627f2091bfbbb6597a8334215630000000000000000000000000000000000000000000000000000000000000001000194a1f1a475f7f8cb82421c5661c956213664019384c1d2ceb2edf7b7d80f95d0e18729bc3632ba3274631126fadb0cbcc1ef5a4e966f2f9250d351c74b905a84'])
	chain.add_block(['2ac5e3e47d28c55ecfb4d4b54455d0259b61679627f2091bfbbb6597a8334215630000000000000000000000000000000000000000000000000000000000000001000194a1f1a475f7f8cb82421c5661c956213664019384c1d2ceb2edf7b7d80f95d0e18729bc3632ba3274631126fadb0cbcc1ef5a4e966f2f9250d351c74b905a83'])
	chain.add_block(['2ac5e3e47d28c55ecfb4d4b54455d0259b61679627f2091bfbbb6597a8334215630000000000000000000000000000000000000000000000000000000000000001000194a1f1a475f7f8cb82421c5661c956213664019384c1d2ceb2edf7b7d80f95d0e18729bc3632ba3274631126fadb0cbcc1ef5a4e966f2f9250d351c74b905a82'])
	with open('file', 'w+') as f:
		json.dump(chain.output_json(), f)

	'''
	chain1 = Blockchain()
	chain1.read_from_file('file')
	chain1.display()
	



