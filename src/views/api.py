from flask import Blueprint, request
from flask_restful import Resource, Api, reqparse, inputs
from flask_httpauth import HTTPBasicAuth
from src import utils, msg
import json

api_blueprint = Blueprint(__name__, 'api')
api = Api(api_blueprint)

auth = HTTPBasicAuth()
auth.verify_password(utils.verify_password)

def send_response(result):
	return {
		"id": result.id,
		"type": result.type,
		"from": result.originator,
		"to": "+"+str(result.recipients['items'][0].recipient),
		"message": result.body,
		"status": result.recipients['items'][0].status,
	}

@api.resource("/message/send")
class SendMessage(Resource):
	@auth.login_required
	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument("from", required=True, type=str)
		parser.add_argument("to", required=True, type=str)
		parser.add_argument("message", required=True, type=str)
		parser.add_argument("call", required=False, type=inputs.boolean)
		args = parser.parse_args()

		arg = (args["from"], args["to"], args["message"])
		if args["call"]:
			result = msg.make_call(*arg)
		else:
			result = msg.send_sms(*arg)

		return send_response(result)

@api.resource("/message/get/<string:msg_id>")
class GetMessage(Resource):
	@auth.login_required
	def get(self, msg_id):
		result = msg.get_msg(msg_id)

		if type(result) == tuple:
			return result

		return send_response(result)