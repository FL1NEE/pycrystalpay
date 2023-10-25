"""
:authors: FL1NEE
:license: Apache License, Version 2.0, see LICENSE file
:copyright: (c) 2023 FL1NEE
"""

# -*- coding: utf-8 -*-
import aiohttp
import asyncio

class CrystalPay(object):
	"""
	:param cashbox_name: - CrystalPay API Cashbox login
	:param client_key: - CrystalPay API Cashbox secret key
	:return:
	"""
	def __init__(self, cashbox_name:str, client_key:str) -> (dict):
		self.domain:str = "https://api.crystalpay.io/v2"
		self.http:str = aiohttp.ClientSession()
		self.cashbox_name:str = cashbox_name
		self.client_key:str = client_key

	async def get_balance(self):
		""" Return cashbox balance """
		json = \
		{
			"auth_login": self.cashbox_name,
			"auth_secret": self.client_key,
			"hide_empty": "true"
		}

		data = await self.http.post(f"{self.domain}/balance/info/", json=json)

		info = await data.json()["balances"]

		return info

	async def create_payment(self, amount:int, comment:str, redirect_url:str, lifetime:int) -> (dict):
		""" Create payment link """
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

		data = await self.http.post(f"{self.domain}/invoice/create/", json=json)

		create = await data.json()

		payment_data = create["url"], create["id"]

		return payment_data

	async def check_payment(self, pay_id:str) -> (dict):
		json = \
		{
			"auth_login": self.cashbox_name,
			"auth_secret": self.client_key,
			"id": pay_id
		}

		data = await self.http.post(f"{self.domain}/invoice/info/", json=json)

		status = await data.json()["state"]

		return status
