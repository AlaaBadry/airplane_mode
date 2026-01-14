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
refresh(frm) {
		frm.add_custom_button(
			__('Assign Seat'),
			function () {
				frm.dialog = new frappe.ui.Dialog({
					title: 'Assign Seat',
					fields: [
						{
							label: 'Seat Number',
							fieldname: 'seat_number',
							fieldtype: 'Data',
							reqd: 1
						}
					],
					primary_action_label: 'Assign',
					primary_action(values) {
						frm.set_value('seat', values.seat_number);
						frm.dialog.hide();
					}
				});

				frm.dialog.show();
			},
			__('Actions')  
		);
	},
});
	
