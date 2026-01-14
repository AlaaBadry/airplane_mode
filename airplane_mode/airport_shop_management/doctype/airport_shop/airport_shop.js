// Copyright (c) 2026, Alaa Badry and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airport Shop", {
  setup(frm) {
    frm.set_query("shop_type", function () {
      return {
        filters: { enabled: 1 }
      };
    });
  }
});

