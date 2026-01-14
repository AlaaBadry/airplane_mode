import frappe


def execute():
	"""Migrate payment_status field to status field in Shop Contract"""

	# Check if both columns exist in the database
	has_payment_status = frappe.db.has_column("Shop Contract", "payment_status")
	has_status = frappe.db.has_column("Shop Contract", "status")

	if has_payment_status and has_status:
		# Copy payment_status to status for all contracts
		frappe.db.sql("""
			UPDATE `tabShop Contract`
			SET status = payment_status
			WHERE payment_status IS NOT NULL AND payment_status != ''
		""")

		frappe.db.commit()
		print("Migrated payment_status to status for Shop Contract")
	elif has_status and not has_payment_status:
		# Status field exists, payment_status is already removed, nothing to migrate
		print("Status field exists, no migration needed")
	else:
		# Status field doesn't exist yet, will be created by model sync
		print("Status field not created yet, skipping migration")
