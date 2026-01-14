import frappe
from frappe.query_builder import DocType
from frappe.query_builder.functions import Sum


def execute(filters=None):
	Airline = DocType("Airline")
	Airplane = DocType("Airplane")
	Flight = DocType("Airplane Flight")
	Ticket = DocType("Airplane Ticket")

	rows = (
		frappe.qb.from_(Airline)
		.left_join(Airplane)
		.on(Airplane.airline == Airline.name)
		.left_join(Flight)
		.on(Flight.airplane == Airplane.name)
		.left_join(Ticket)
		.on((Ticket.flight == Flight.name) & (Ticket.docstatus == 1))
		.groupby(Airline.name)
		.select(
			Airline.name.as_("airline"),
			Sum(Ticket.total_amount).as_("revenue"),
		)
	).run(as_dict=True)

	data = []
	total_revenue = 0.0

	for r in rows:
		revenue = float(r.get("revenue") or 0)  # ✅ ensures 0 for no revenue airlines
		data.append({"airline": r["airline"], "revenue": revenue})
		total_revenue += revenue

	columns = [
		{"label": "Airline", "fieldname": "airline", "fieldtype": "Link", "options": "Airline", "width": 200},
		{"label": "Revenue", "fieldname": "revenue", "fieldtype": "Currency", "width": 140},
	]

	chart = {
		"data": {
			"labels": [d["airline"] for d in data],
			"datasets": [{"values": [d["revenue"] for d in data]}],
		},
		"type": "donut",
	}

	report_summary = [{"label": "Total Revenue", "value": total_revenue, "indicator": "Green"}]

	return columns, data, None, chart, report_summary
