#!/usr/bin/env python3

import flask, requests, sys
from flask import jsonify, request

PORT = 1400

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
	print (a)
	if a == '2':
		return jsonify({'error': 'Invalid address'}), 404
	return jsonify({'balance': 42}), 201

@app.route('')

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=PORT, threaded=True)
