from flask import Blueprint, render_template, request, jsonify
from flask_httpauth import HTTPBasicAuth
from redis import Redis
from src import utils, msg
from os import getenv
import messagebird
import config

redis = Redis().from_url(getenv("REDIS_URL"))
msg_client = messagebird.Client(getenv('MESSAGEBIRD'))
admin_blueprint = Blueprint(__name__, 'admin')

auth = HTTPBasicAuth()
auth.verify_password(utils.verify_password)

@admin_blueprint.route('/', methods=['GET', 'POST'])
@auth.login_required
def admin_panel():
	if request.method == "POST":
		rcv = utils.fix_number(request.form.get('rcv'))
		print(rcv)

		keys = redis.lrange("keys", 0, -1)
		while True:
			key = utils.generate_random_key(4)
			if not key.encode() in keys: break

		if len(rcv) == config.phone_total_length:
			result = msg.send_sms("NiceSMS", rcv, f"Your one time key is: {key}")
			redis.lpush("keys", key)
			if type(result) == str:
				return result

			return render_template("result.html", msg=result, admin=True)

		elif len(rcv) == len(config.phone_prepend):
			print(f"Generated Anonymous Key | {key}")
			redis.lpush("keys", key)
			return jsonify({"key": key})

		return utils.error("Invalid number!")

	return render_template("admin.html")

@admin_blueprint.route('/send', methods=['GET', 'POST'])
@auth.login_required
def admin_sms():
	if request.method == "POST":
		src = request.form.get('src').strip()
		dst = request.form.get('dst')
		text = request.form.get('text')

		if request.form.get('callbox') is None:
			result =  msg.send_sms(src, dst, text)
		else:
			result = msg.make_call(src, dst, text)
		
		if type(result) == tuple:
			return result
			
		return render_template("result.html", msg=result, admin=True)

	return render_template("send.html", admin=True)