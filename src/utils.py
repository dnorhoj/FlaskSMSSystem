from flask import jsonify
from random import choice
from string import digits
import config

def fix_number(raw):
	remove = [" ","(",")"]
	for i in remove:
		raw = raw.replace(i, "")
	raw.replace(config.phone_prepend, "", 1)
	return config.phone_prepend+raw

def generate_random_key(length):
	return "".join(choice(digits) for _ in range(length))

def error(message):
	return jsonify({"Error": message}), 400