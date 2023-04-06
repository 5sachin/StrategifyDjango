

from ks_api_client import ks_api

URL = ""
class Kotak():
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


	def place_order(self,order_type,instrument_token,transaction_type,quantity,price,disclosed_quantity,trigger_price,validity,variety,tag):
		print("Client Info: ",self.client)
		self.client.place_order(order_type=order_type,instrument_token=instrument_token,transaction_type=transaction_type,
				quantity=quantity,price=price,disclosed_quantity=disclosed_quantity,
				trigger_price=trigger_price,validity=validity,variety=variety,tag=tag)
		print("BUY Order Placed ! ", instrument_token, quantity, transaction_type)

	def trade_report(self):
		print("Order Report: ")
		report = self.client.order_report()
		print(report)

	def trade_report_order(self,orderid):
		print("Order Report Id: ",orderid)
		report = self.client.order_report(order_id = orderid)
		print(report)

	def get_quote(self,token):
		try:
			print(self.client.quote(instrument_token = token))
		except Exception as e:
			print("Get Quote Exception: ",str(e))




