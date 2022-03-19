import config
import json
from flask import Flask
from flask import render_template, request
from ks_api_client import ks_api

app = Flask(_name_)

class Kotak:
	def __init__(self,access_token):
		client = ks_api.KSTradeApi(access_token="2042d3ae-3eca-3a6e-823a-0cc63fa8574d", userid="TS01061986",
                           consumer_key="oblkMRyEpbSam9fxb2j5XEYGmE8a", ip="127.0.0.1", app_id="1")
		client.login(password="ya@Mi786")
		client.session_2fa(access_code="7354")
