#!/usr/bin/env python3

import sys

from wallet import Wallet

def usage():
	print ('usage:')
	print ('Send coins from one acc to another')
	print ('\t./wallet_cli.py send <recipient_address> <amount>')
	print ('\nGenerate new private key')
	print ('\t./wallet_cli.py generate')
	print ('\nImport existing private key')
	print ('\t./wallet_cli.py import <private_key>')
	print ('\nGet balance of the address')
	print ('\t./wallet_cli.py balance <address>')

def select_action(wall, arguments):
	if len(arguments) == 0:
		usage()
		return
	if ((arguments[0] == 'import' and len(arguments) != 2) or
		(arguments[0] == 'balance' and len(arguments) != 2) or
		(arguments[0] == 'broadcast' and len(arguments) != 2) or
		(arguments[0] == 'send' and len(arguments) != 3)):
		usage()
		return
	if (arguments[0] == 'import' and len(arguments) == 2):
		wall.importing(arguments[1])
	if (arguments[0] == 'balance' and len(arguments) == 2):
		wall.balance(arguments[1])
	if (arguments[0] == 'broadcast' and len(arguments) == 2):
		wall.broadcast(arguments[1])
	if (arguments[0] == 'send' and len(arguments) == 3):
		wall.send(arguments[1], arguments[2])
	if (arguments[0] == 'generate' and len(arguments) == 1):
		wall.generate()
	
if __name__ == "__main__":
	wall = Wallet()
	select_action(wall, sys.argv[1:])

