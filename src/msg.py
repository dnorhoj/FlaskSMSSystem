from src import utils
from os import getenv
from redis import Redis
import config
import messagebird


redis = Redis().from_url(getenv("REDIS_URL"))
msg_client = messagebird.Client(getenv("MESSAGEBIRD"))

def send_sms(src, dst, text, key=None):
	if key is not None:
		key = key.encode()
		keys = redis.lrange("keys", 0, -1)
		if key not in keys:
			return utils.error("Invalid key")

	fixed_src = utils.fix_number(src)
	if fixed_src.replace(config.phone_prepend, "").isdecimal() and len(fixed_src) == config.phone_total_length:
		src = fixed_src
	dst = utils.fix_number(dst)

	if len(dst) != config.phone_total_length:
		return utils.error("Destination number is not 8 characters long")

	if len(text) == 0 or (len(text.encode()) > 150 and key is not None):
		return utils.error("Invalid message length")

	if src.lower() == "nicesms" and key is not None:
		return utils.error("Reserved sender!")

	try:
		message = msg_client.message_create(src, dst, text)
		if key is not None:
			redis.lrem("keys", 0, key)
	except messagebird.ErrorException as e:
		print(e)
		return utils.error("Unknown Error! Contact the admin. (Key not used)")

	if key:
		print(f"Sent sms | {src} => {dst} | Key: {key.decode()} | Text: {text}")
	else:
		print(f"Sent sms | {src} => {dst} | Text: {text}")

	return message

def make_call(src, dst, text, key=None):
	if key is not None:
		key = key.encode()
		keys = redis.lrange("keys", 0, -1)
		if key not in keys:
			return utils.error("Invalid key")

	src = utils.fix_number(src)
	dst = utils.fix_number(dst)

	if len(dst) != 11 or len(src) != 11:
		return utils.error("Destination and Source numbers are not 8 characters long")

	if len(text) == 0 or len(text.encode()) > 140:
		return utils.error("Invalid tts message length")

	try:
		result = msg_client.voice_message_create(dst, text, params={"originator": src, "language": "da-DK"})
		if key is not None:
			redis.lrem("keys", 0, key)
	except messagebird.ErrorException:
		return utils.error("Unknown Error! Contact the admin. (Key not used)")

	if key:
		print(f"Made call | {src} => {dst} | Key: {key.decode()} | Text: {text}")
	else:
		print(f"Made call | {src} => {dst} | Text: {text}")

	return result

def get_msg(msg_id):
	try:
		return msg_client.message(msg_id)
	except messagebird.ErrorException:
		try:
			return msg_client.voice_message(msg_id)
		except messagebird.ErrorException:
			return utils.error("Message not found!")