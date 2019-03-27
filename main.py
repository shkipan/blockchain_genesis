#!/usr/bin/env python3

import sys
from ecdsa import SigningKey

from wallet import Wallet

def usage():
	print ('usage:')
	print ('Send coins from one acc to another')
	print ('\t./wallet.py send <sender_key> <recipient_key> <amount>')

def select_action(wall, arguments):
	if len(arguments) == 0:
		usage()
		return
	if ((arguments[0] == 'import' and len(arguments) != 2) or (arguments[0] == 'send' and len(arguments) != 3)):
		usage()
		return
	if (arguments[0] == 'import' and len(arguments) == 2):
		wall.importing(arguments[1])
	if (arguments[0] == 'send' and len(arguments) == 3):
		wall.send(arguments[1], arguments[2])
	
if __name__ == "__main__":
	wall = Wallet()
	select_action(wall, sys.argv[1:])

