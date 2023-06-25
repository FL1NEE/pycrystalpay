# -*- coding: utf-8 -*-
from requests import *

class CrystalPay(object):
	def __init__(self, cashbox_name=None, client_key1=None):
		self.http = Session()
		self.cashbox_name = cashbox_name
		self.client_key1 = client_key1
		self.domain = "https://api.crystalpay.io/v2"

	def get_balance(self):
		json = \
		{
			"auth_login": self.cashbox_name,
			"auth_secret": self.client_key1,
			"hide_empty": "true"
		}

		info = self.http.post(f"{self.domain}/balance/info/", json=json).json()["balances"]

		return info

	def create_payment(self, amount=None, comment=None, redirect_url=None, lifetime=None):
		json = \
		{
			"auth_login": self.cashbox_name,
			"auth_secret": self.client_key1,
			"amount": amount,
			"description": comment,
			"type": "purchase",
			"lifetime": lifetime
		}

		create = self.http.post(f"{self.domain}/invoice/create/", json=json).json()

		payment_data = create["url"], create["id"]

		return payment_data

	def check_payment(self, id=None):
		json = \
		{
			"auth_login": self.cashbox_name,
			"auth_secret": self.client_key1,
			"id": id
		}

		status = self.http.post(f"{self.domain}/invoice/info/", json=json).json()

		return status["state"]
