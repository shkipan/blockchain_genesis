#!/usr/bin/env python3

import flask, requests, sys
from flask import jsonify, request
from block import Blockchain, Block
from transaction import Transaction

PORT = 1400

blockchain = Blockchain()

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.errorhandler(404)
def not_found(error):
	return jsonify({'error': 'Not found'}), 404

@app.route('/', methods=['GET'])
def homepage():
	return 'Hello, blockchain genesis', 201

@app.route('/balance', methods=['GET'])
def balance():
	a = request.args.get('address')
	if not a:
		return jsonify({'error': 'Adress wasn\'t passed'}), 404
	bal = 0
	for bl in blockchain.blocks:
		for tr in bl.transactions:
			if tr.sender == a:
				bal -= tr.value
			if tr.recipient == a:
				bal += tr.value
	return jsonify({'balance': bal}), 201

@app.route('/history', methods=['GET'])
def history():
	a = request.args.get('address')
	if not a:
		return jsonify({'error': 'Adress wasn\'t passed'}), 404
	trans = []
	for bl in blockchain.blocks:
		for tr in bl.transactions:
			if tr.sender == a or tr.recipient == a:
				to_app = {
					'Sender': tr.sender,
					'Recipient': tr.recipient,
					'Amount': tr.value}
				trans.append(to_app)
	return jsonify({'Address history': trans}), 201

@app.route('/broadcast', methods=['POST'])
def broadcast():
	if not request.is_json:
		return jsonify({'error': 'Invalid object passed'}), 404
	trans = request.get_json()['transaction']
	blockchain.add_block([trans])
	return jsonify({'success': 1}), 201

@app.route('/heigth/get', methods=['GET'])
def get_heigth():
	return jsonify({'current_heigth': blockchain.curr_heigth}), 201

@app.route('/block/get/heigth', methods=['GET'])
def get_block_by_heigth():
	hei = request.args.get('heigth')
	print (hei)
	if not hei:
		return jsonify({'error': 'No parameter passed'}), 404
	hei = int(hei)
	if hei < 0:
		return jsonify({'error': 'Block heigth must be positive number'}), 404
	if hei >= blockchain.curr_heigth:
		return jsonify({'error': 'Heigth exceeds number of blocks'}), 404
	for i in blockchain.blocks:
		if i.heigth == hei:
			return jsonify({'block': i.to_json()}), 201

@app.route('/block/get/hash', methods=['GET'])
def get_block_by_hash():
	has = request.args.get('hash')
	if not has:
		return jsonify({'error': 'No parameter passed'}), 404
	for i in blockchain.blocks:
		if i.bl_hash == has:
			return jsonify({'block': i.to_json()}), 201
	return jsonify({'error': 'No such hash in blocks'}), 201

#@app.route('')
	#	return jsonify({'error': 'Invalid address'}), 404

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=PORT, threaded=True)
