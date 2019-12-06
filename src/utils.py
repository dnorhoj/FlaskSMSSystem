from flask import jsonify
from random import choice
from string import digits

def fix_number(raw):
	raw = raw.replace(" ", "")
	raw = raw.replace("+45", "")
	return "+45{}".format(raw)

def generate_random_key(length):
	return "".join(choice(digits) for _ in range(length))

def error(message):
	return jsonify({"Error": message}), 400