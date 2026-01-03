# Copyright (c) 2025, Alaa Badry and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator


class AirplaneFlight(WebsiteGenerator):
	def on_submit(self):
		frappe.db.set_value(self.doctype, self.name, "status", "Completed")
		frappe.db.commit()
		self.reload()
