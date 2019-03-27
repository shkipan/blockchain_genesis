#!/usr/bin/env python3

import sys
from ecdsa import SigningKey
from transaction import Transaction

class Wallet:
	priv_key = None

	def __init__(self):
		self.priv_key = 'bomba'

	def send(self, addr_from, addr_to, amount):
		trans = Transaction(addr_from, addr_to, amount)
		trans.display()
		trans.send(self.priv_key)

