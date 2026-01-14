# Copyright (c) 2025, Alaa Badry and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator


class AirplaneFlight(WebsiteGenerator):
	def on_submit(self):
		frappe.db.set_value(self.doctype, self.name, "status", "Completed")
		frappe.db.commit()
		self.reload()

	def on_update_after_submit(self):
		before = self.get_doc_before_save()
		if not before:
			return

		old_gate = before.gate_number
		new_gate = self.gate_number

		if old_gate == new_gate:
			return
		frappe.msgprint(f"Gate changed from {old_gate} to {new_gate}")
		# Enqueue background job
		frappe.enqueue(
			"airplane_mode.airplane_mode.doctype.airplane_flight.airplane_flight.update_tickets_gate",
			flight_name=self.name,
			new_gate=new_gate,
		)


@frappe.whitelist()
def update_tickets_gate(flight_name, new_gate):
	frappe.db.set_value(
		"Airplane Ticket",
		{"flight": flight_name, "docstatus": ["<", 2]},
		"gate_number",
		new_gate,
		update_modified=False,
	)
	frappe.db.commit()
