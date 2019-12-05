from flask import render_template
from src import utils
from os import getenv
from redis import Redis
import messagebird


redis = Redis().from_url(getenv("REDIS_URL"))
msg_client = messagebird.Client(getenv('MESSAGEBIRD'))

def send_sms(src: str, dst: str, text: str, key=None):
	if not key is None:
		key = key.encode()
		keys = redis.lrange("sms_keys", 0, -1)
		if key not in keys:
			return utils.error("Invalid key")

	fixed_src = utils.fix_number(src)
	if fixed_src.replace("+", "").isdecimal() and len(fixed_src) == 11:
		src = fixed_src
	dst = utils.fix_number(dst)

	if len(dst) != 11:
		return utils.error("Destination number is not 8 characters long")

	if len(src) < 3 or len(src) > 11:
		return utils.error("Source number is either too short or too long. Correct: 3 > num > 10")

	if len(text) == 0 or len(text.encode()) > 140:
		return utils.error("Invalid message length")

	if src.lower() == "nicesms" and not key is None:
		return utils.error("Reserved sender!")

	try:
		message = msg_client.message_create(src, dst, text)
		if key is not None:
			redis.lrem("sms_keys", 0, key)
	except messagebird.ErrorException:
		return utils.error("Unknown Error! Contact the admin. (Key not used)")

	if key:
		print(f"Sent sms | {src} => {dst} | Key: {key.decode()} | Text: {text}")
	else:
		print(f"Sent sms | {src} => {dst} | Text: {text}")

	return render_template("result.html", msg=message, admin=(key is None))