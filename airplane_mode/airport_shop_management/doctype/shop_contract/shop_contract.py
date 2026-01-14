# Copyright (c) 2026, Alaa Badry and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import add_months, getdate, today


class ShopContract(Document):
	def before_submit(self):
		# Prevent having two active submitted contracts for the same shop
		existing = frappe.db.exists(
			"Shop Contract",
			{
				"shop": self.shop,
				"docstatus": 1,
				"name": ["!=", self.name],
			},
		)
		if existing:
			frappe.throw("This shop already has an active submitted contract.")

		# Set initial status as Pending
		self.status = "Pending"

		# Auto-set due_date if not set (first payment due 1 month after start_date)
		if not self.due_date and self.start_date:
			self.due_date = add_months(self.start_date, 1)

	def onload(self):
		# Check and update status to Overdue if past due_date and not Paid
		if self.docstatus == 1 and self.get("due_date") and self.get("status") != "Paid":
			if getdate(self.due_date) < getdate(today()):
				self.status = "Overdue"

	def on_submit(self):
		# Mark shop as Occupied + link current contract
		frappe.db.set_value(
			"Airport Shop",
			self.shop,
			{
				"current_contract": self.name,
				"status": "Occupied",
				# Optional: show tenant directly on shop (if you kept tenant_name field)
				"tenant_name": self.tenant,
				"tenant_email": self.tenant_email,
				"end_date": self.end_date,
				"rent_amount": self.monthly_rent,
			},
			update_modified=False,
		)
		frappe.msgprint(f"Shop '{self.shop}' is now marked as Occupied.")

	def on_cancel(self):
		# If this contract is the current contract, clear it and mark Vacant
		current = frappe.db.get_value("Airport Shop", self.shop, "current_contract")
		if current == self.name:
			frappe.db.set_value(
				"Airport Shop",
				self.shop,
				{
					"current_contract": None,
					"status": "Vacant",
					"tenant_name": None,
				},
				update_modified=False,
			)

	def validate(self):
		# Check if contract is overdue
		if self.docstatus == 1 and self.get("due_date") and self.get("status") != "Paid":
			if getdate(self.due_date) < getdate(today()):
				self.status = "Overdue"


def update_overdue_contracts():
	"""Scheduled task to mark contracts as overdue.

	This function is called by Frappe's scheduler daily to check all submitted contracts
	and automatically mark them as "Overdue" if their due_date has passed and payment status is not "Paid".
	It runs in the background without manual intervention.
	"""
	contracts = frappe.get_all(
		"Shop Contract",
		filters={
			"docstatus": 1,
			"status": ["in", ["Pending", ""]],
			"due_date": ["<", today()]
		},
		pluck="name"
	)

	for contract in contracts:
		frappe.db.set_value("Shop Contract", contract, "status", "Overdue", update_modified=False)

	if contracts:
		frappe.db.commit()
		frappe.logger().info(f"Marked {len(contracts)} contracts as overdue")
