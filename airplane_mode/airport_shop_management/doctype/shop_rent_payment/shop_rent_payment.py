# Copyright (c) 2026, Alaa Badry and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc


class ShopRentPayment(Document):
	def on_submit(self):
		# Mark the contract as Paid when payment is submitted
		if self.contract:
			frappe.db.set_value("Shop Contract", self.contract, "status", "Paid", update_modified=False)
			frappe.msgprint(f"Contract {self.contract} marked as Paid")

	def on_cancel(self):
		# Mark contract back to Pending when payment is cancelled
		if self.contract:
			frappe.db.set_value("Shop Contract", self.contract, "status", "Pending", update_modified=False)


@frappe.whitelist()
def make_payment_entry(source_name, target_doc=None):
	"""Create Shop Rent Payment from Shop Contract"""

	def set_missing_values(source, target):
		target.amount = source.monthly_rent

	doclist = get_mapped_doc(
		"Shop Contract",
		source_name,
		{
			"Shop Contract": {
				"doctype": "Shop Rent Payment",
				"field_map": {
					"name": "contract",
					"tenant": "tenant"
				}
			}
		},
		target_doc,
		set_missing_values
	)

	return doclist
