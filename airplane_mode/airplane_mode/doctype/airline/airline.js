frappe.ui.form.on("Airline", {
  refresh(frm) {
    console.log("Airline form refreshed");
    // remove old link duplicates on refresh
    frm.page.clear_menu();

    // If website is empty, do nothing (requirement)
    if (!frm.doc.website) return;

    // Add a custom web link in the form view
    frm.add_web_link(frm.doc.website, __("Website"));
  },
});
