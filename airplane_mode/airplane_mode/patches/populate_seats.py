import frappe
from frappe.model.document import Document
from random import randint
import random

def execute():
	tickets = frappe.get_all("Airplane Ticket", filters={"seat": ""}, fields=["name"])
	letters = ["A", "B", "C", "D", "E"]
	for ticket in tickets:
		randnumber = randint(1, 200)
		randletter = random.choice(letters)
		seat = f"{randnumber}{randletter}"
		frappe.db.set_value("Airplane Ticket", ticket.name, "seat", seat)
