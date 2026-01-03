# Copyright (c) 2025, Alaa Badry and contributors
# For license information, please see license.txt

# import frappe
import random
from random import randint

from frappe import frappe
from frappe.model.document import Document


class AirplaneTicket(Document):
	def validate(self):
		frappe.errprint(self.flight_price)

		# Remove duplicate add-ons
		seen_items = []
		items_to_remove = []
		for item in self.add_ons:
			if item.item in seen_items:
				items_to_remove.append(item)
			else:
				seen_items.append(item.item)

		for item in items_to_remove:
			self.remove(item)

		if items_to_remove:
			frappe.msgprint(
				f"Removed {len(items_to_remove)} duplicate item(s). Reloading form...",
				indicator="orange",
				alert=True,
			)

		# Calculate total amount
		itemamount = 0
		for item in self.add_ons:
			itemamount += item.amount
		self.total_amount = self.flight_price + itemamount

	def after_save(self):
		# Trigger client-side reload after save
		frappe.flags.after_save_reload = True

	def on_submit(self):
		if self.status != "Boarded":
			frappe.throw("Cannot submit ticket unless status is 'Boarded'")

	def before_insert(self):
		randnumber = randint(1, 200)
		letter = ("A", "B", "C", "D", "E")
		randletter = random.choice(letter)
		self.seat = f"{randnumber}{randletter}"
