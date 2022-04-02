# import config
# import json
# from flask import Flask
# from flask import render_template, request
# from ks_api_client import ks_api
#
# app = Flask(__name__)
#
#
# client = ks_api.KSTradeApi(access_token="2042d3ae-3eca-3a6e-823a-0cc63fa8574d", userid="TS01061986",
#                            consumer_key="oblkMRyEpbSam9fxb2j5XEYGmE8a", ip="127.0.0.1", app_id="1")
#
# client.login(password="ya@Mi786")
#
# client.session_2fa(access_code="7354")
#
# @app.route('/')
# def dashboard():
#     orders = client.order_report();
#     return render_template('dashboard.html', kotak_orders=orders)
#
#
# @app.route('/webhook', methods=['POST'])
# def webhook():
#     webhook_message = json.loads(request.data)
#
#     print(webhook_message)
#
#     if webhook_message['passphrase'] != "aj$Ta786":
#         return {
#             'code': 'error',
#             'message': 'nice try buddy'
#         }
#
#     price = webhook_message['strategy']['order_price']
#     # quantity = webhook_message['strategy']['order_contracts']
#
#     quantity = 1
#     symbol = webhook_message['ticker']
#     side = webhook_message['strategy']['order_action']
#
#     if side == "BUY":
#         try:
#             # Place a Fixed Symbol Order
#             # If side Is Buy then Place Buy Order
#             client.place_order(order_type="N", instrument_token=symbol, transaction_type="BUY", quantity=quantity,
#                                price=0,
#                                disclosed_quantity=0, trigger_price=0,
#                                validity="GFD", variety="REGULAR", tag="string")
#
#             print("Order Placed ! ", symbol, quantity, side)
#         except Exception as e:
#             print("Exception when calling OrderApi->place_order: %s\n" % e)
#         return webhook_message
#     else:
#
#         try:
#             # Place a Fixed Symbol Order
#             # If side Is Buy then Place Buy Order
#             client.place_order(order_type="N", instrument_token=symbol, transaction_type="SELL", quantity=quantity,
#                                price=0,
#                                disclosed_quantity=0, trigger_price=0,
#                                validity="GFD", variety="REGULAR", tag="string")
#
#             print("Order Placed ! ", symbol, quantity, side)
#         except Exception as e:
#             print("Exception when calling OrderApi->place_order: %s\n" % e)
#         return webhook_message
#
#
# if _name_ == "_main_":
#     app.run(host='0.0.0.0')







import config
import json
from ks_api_client import ks_api
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


URL = ""
class Kotak:
	global URL
	def __init__(self, access_token, userid, consumer_key, app_id, password):
		self.access_token = access_token
		self.userid = userid
		self.consumer_key = consumer_key
		self.app_id = app_id
		self.password = password
		self.client = None

	def configure(self):
		self.client = ks_api.KSTradeApi(access_token=self.access_token, userid=self.userid,
										consumer_key=self.consumer_key, ip="127.0.0.1", app_id="APP")
		self.client.login(password=self.password)

	def session_login(self,acess_code):
		self.client.session_2fa(access_code=acess_code)

	def set_webhookurl(self,url):
		self.url = url
		URL = url
		print(self.url)


@csrf_exempt
@require_POST
def webhook_call(request,URL):
	print("URL: ",URL)
	jsondata = request.body
	data = json.loads(jsondata)
	print("Data: ",data)
	return HttpResponse(status=200)


