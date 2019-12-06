from flask import Blueprint, render_template, request, jsonify
from flask_httpauth import HTTPBasicAuth
from redis import Redis
from src import utils, msg
from os import getenv
import messagebird

redis = Redis().from_url(getenv("REDIS_URL"))
msg_client = messagebird.Client(getenv('MESSAGEBIRD'))
admin = Blueprint(__name__, 'admin')

auth = HTTPBasicAuth()
@auth.verify_password
def verify_password(username, password):
	return (username, password) == ("admin", getenv("ADMIN_PASS"))

@admin.route('/', methods=['GET', 'POST'])
@auth.login_required
def admin_panel():
	if request.method == "POST":
		rcv = utils.fix_number(request.form.get('rcv'))

		keys = redis.lrange("keys", 0, -1)
		key = utils.generate_random_key(4)
		while key.encode() in keys:
			key = utils.generate_random_key(4)

		if len(rcv) == 11:
			result = msg.send_sms("NiceSMS", rcv, f"Your one time key is: {key}")
			redis.lpush("keys", key)
			return result
			
		elif len(rcv) == 3:
			print(f"Generated Anonymous Key | {key}")
			redis.lpush("keys", key)
			return jsonify({"key": key})

		return utils.error("Invalid number!")

	return render_template("admin.html")

@admin.route('/send', methods=['GET', 'POST'])
@auth.login_required
def admin_sms():
	if request.method == "POST":
		src = request.form.get('src').strip()
		dst = request.form.get('dst')
		text = request.form.get('text')

		if request.form.get('callbox') is None:
			return msg.send_sms(src, dst, text)
		else:
			return msg.make_call(src, dst, text)

	return render_template("send.html", admin=True)