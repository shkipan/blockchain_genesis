#!/usr/bin/env python3

import sys, ecdsa, requests, json
from flask import json
from ecdsa import SigningKey, VerifyingKey
from transaction import Transaction

class Wallet:
	priv_key = None
	addr = None

	def __init__(self):
		try:
			f = open('key', 'r')
			self.priv_key = f.readline().replace('\n', '')
			print(self.priv_key)
			vk = SigningKey.from_string(bytes.fromhex(self.priv_key), curve=ecdsa.SECP256k1).get_verifying_key()
			a = vk.to_string().hex()
			self.addr = ('03' if int(a[127], 16) & 1 else '02') + a[:64]
		except FileNotFoundError:
			print ('File with private key not found')

	def importing(self, key):
		if len(key) != 64:
			print ('Invalid key')
			return
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

	def generate(self):
		sk = SigningKey.generate(curve=ecdsa.SECP256k1)
		self.priv_key = sk
		print (sk.to_string().hex())

	def balance(self, addr):
			r = requests.get('http://127.0.0.1:1400/balance?address=' + addr)
			bal = json.loads(r.text)
			if r.status_code == 201:
				print ('Balance of', addr, 'is', bal['balance'])
			else:
				print ('Error:', bal['error'])

