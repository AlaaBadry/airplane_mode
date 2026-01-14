// Copyright (c) 2026, Alaa Badry and contributors
// For license information, please see license.txt

frappe.ui.form.on("Shop Contract", {
	refresh(frm) {
		if (frm.doc.docstatus === 1) {
			frm.add_custom_button(__('Create Payment'), function() {
				frappe.model.open_mapped_doc({
					method: "airplane_mode.airport_shop_management.doctype.shop_rent_payment.shop_rent_payment.make_payment_entry",
					frm: frm
				});
			}, __('Actions'));
		}
	},
});
