#!/usr/bin/env python3

import sys
from ecdsa import SigningKey
from transaction import Transaction

class Wallet:
	priv_key = None
	addr = None

	def __init__(self):
		try:
			f = open('key', 'r')
			self.priv_key = f.readline().replace('\n', '')
		except:
			pass

	def importing(self, key):
		self.priv_key = key
		f = open('key', 'w')
		f.write(key)

	def send(self, addr_to, amount):
		if (not self.priv_key):
			print ('Import your private key wiht <import> command!')
			return
		trans = Transaction(self.addr, addr_to, amount)
		trans.display()
		trans.send(self.priv_key)

	def balance(self, addr):
		bal = 42
		print ('Balance of', addr, 'is', bal)

