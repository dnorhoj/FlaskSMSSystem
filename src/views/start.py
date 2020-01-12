from flask import Blueprint, request, render_template
from src import msg

start_blueprint = Blueprint(__name__, 'start')

@start_blueprint.route('/', methods=['GET', 'POST'])
def view():
	if request.method == "POST":
		src = request.form.get('src').strip()
		dst = request.form.get('dst')
		key = request.form.get('key')
		text = request.form.get('text')

		if request.form.get('callbox') is None:
			result = msg.send_sms(src, dst, text, key)
		else:
			result = msg.make_call(src, dst, text, key)

		if type(result) == tuple:
			return result

		return render_template("result.html", msg=result, admin=False)

	return render_template("send.html")