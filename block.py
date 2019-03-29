import hashlib

class Block:
	heigth = 0
	transactions = []
	nonce = 0
	version = 42
	bl_hash = ''
	prev_hash = ''

	def calculate_hash(self):
		to_hash = (
			hex(self.version).replace('0x', '') +
			hex(self.nonce).replace('0x', '') +
			hex(self.heigth).replace('0x', '') +
			self.prev_hash
		)
		for i in self.transactions:
			to_hash += i
		self.bl_hash = hashlib.sha256(to_hash.encode('ascii')).hexdigest()

	def __init__(self, trans, ph, hei):
		self.heigth = hei
		self.prev_hash = ph
		for i in trans:
			self.transactions.append(i)
		Block.calculate_hash(self)

	def display(self):
		print ('vers', self.version)
		print ('heig', self.heigth)
		print ('nonc', self.nonce)
		for i in self.transactions:
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
			'transactions': self.transactions
		}

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

if __name__ == '__main__':
	chain = Blockchain()
	chain.add_block(['1', '2', '3'])
	chain.add_block(['7', '6', '5'])
	chain.display()


