# Copyright (c) 2025, Alaa Badry and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class FlightPassenger(Document):
	def before_save(self):
		parts = [self.first_name, self.last_name]
		parts = [p for p in parts if p]
		self.full_name = " ".join(parts)
