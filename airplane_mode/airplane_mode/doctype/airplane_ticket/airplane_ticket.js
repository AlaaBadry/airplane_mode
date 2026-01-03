// Copyright (c) 2025, Alaa Badry and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airplane Ticket", {
	validate(frm) {
		console.log("After Save Triggered");
		if (frappe.flags.after_save_reload) {
			// Auto-reload form after save to show removed duplicates
			frm.reload_doc();
			frappe.flags.after_save_reload = false;
		}
	},
});
