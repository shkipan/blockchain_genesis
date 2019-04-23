import sys, ecdsa, requests, json, hashlib
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
			if len(self.priv_key) != 64:
				print ('Invalid key in file')
				return
			vk = SigningKey.from_string(bytes.fromhex(self.priv_key), curve=ecdsa.SECP256k1).get_verifying_key()
			a = vk.to_string().hex()
			self.addr = ('03' if int(a[127], 16) & 1 else '02') + a[:64]
			self.addr = hashlib.sha256(bytes.fromhex(self.addr)).hexdigest()
		except FileNotFoundError:
			print ('File with private key not found')

	def importing(self, key):
		if len(key) != 64:
			print ('Invalid key imported')
			return
		self.priv_key = key
		vk = SigningKey.from_string(bytes.fromhex(self.priv_key), curve=ecdsa.SECP256k1).get_verifying_key()
		a = vk.to_string().hex()
		self.addr = ('03' if int(a[127], 16) & 1 else '02') + a[:64]
		self.addr = hashlib.sha256(bytes.fromhex(self.addr)).hexdigest()
		print (self.addr, 'imported')

		f = open('key', 'w')
		f.write(key)

	def send(self, addr_to, amount):
		if (not self.priv_key):
			print ('Import your private key wiht <import> command!')
			return
		if len(addr_to) != 64:
			print ('Invalid address to send!')
			return
		try:
			if int(amount) <= 0:
				print ('Amount must be a positive number')
				return
		except:
			print ('Amount must be a number')
			return
		trans = Transaction(self.addr, addr_to, amount).serialize(self.priv_key)
		print (trans)

	def broadcast(self, raw_trans):
		if len(raw_trans) < 136:
			print ('Invalid raw transaction')
			return
		try:
			r = requests.post(
				url = 'http://127.0.0.1:1400/broadcast', 
				json={'transaction': raw_trans})
		except requests.exceptions.ConnectionError:
			print ('Unable to connect')
			return
		if r.status_code == 201:
			print ('Broadcasted successfully')
		else:
			print ('Error', r.status_code, ':', json.loads(r.text)['error'])

	def generate(self):
		sk = SigningKey.generate(curve=ecdsa.SECP256k1)
		vk = sk.get_verifying_key()
		a = vk.to_string().hex()
		addr = ('03' if int(a[127], 16) & 1 else '02') + a[:64]
		addr = hashlib.sha256(bytes.fromhex(addr)).hexdigest()
		print ('Private key:', sk.to_string().hex())
		print ('Address:', addr)

	def balance(self, addr):
			r = requests.get('http://127.0.0.1:1400/balance?address=' + addr)
			bal = json.loads(r.text)
			if r.status_code == 201:
				print ('Balance of', addr, 'is', bal['balance'])
			else:
				print ('Error:', bal['error'])

