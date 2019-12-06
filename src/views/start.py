from flask import Blueprint, request, render_template
from src import utils, msg

start = Blueprint(__name__, 'start')

@start.route('/', methods=['GET', 'POST'])
def view():
	if request.method == "POST":
		src = request.form.get('src').strip()
		dst = request.form.get('dst')
		key = request.form.get('key')
		text = request.form.get('text')

		if request.form.get('callbox') is None:
			return msg.send_sms(src, dst, text, key)
		else:
			return msg.make_call(src, dst, text, key)

	return render_template("send.html")