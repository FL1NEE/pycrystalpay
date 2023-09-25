# -*- coding: utf-8 -*-
import grequests

class CrystalPay(object):
	def __init__(self, cashbox_name:str, client_key:str) -> (dict):
		self.domain = "https://api.crystalpay.io/v2"
		self.http = grequests.Session()
		self.cashbox_name = cashbox_name
		self.client_key = client_key

	def get_balance(self):
		json = \
		{
			"auth_login": self.cashbox_name,
			"auth_secret": self.client_key,
			"hide_empty": "true"
		}

		info = self.http.post(f"{self.domain}/balance/info/", json=json).json()["balances"]

		return info

	def create_payment(self, amount:int, comment:str, redirect_url:str, lifetime:int) -> (dict):
		json = \
		{
			"auth_login": self.cashbox_name,
			"auth_secret": self.client_key,
			"amount": amount,
			"type": "purchase",
			"lifetime": lifetime
		}
		if comment:
			json["description"] = comment
		if redirect_url:
			json["redirect_url"] = redirect_url

		create = self.http.post(f"{self.domain}/invoice/create/", json=json).json()

		payment_data = create["url"], create["id"]

		return payment_data

	def check_payment(self, pay_id:str) -> (dict):
		json = \
		{
			"auth_login": self.cashbox_name,
			"auth_secret": self.client_key,
			"id": pay_id
		}

		status = self.http.post(f"{self.domain}/invoice/info/", json=json).json()

		return status["state"]
