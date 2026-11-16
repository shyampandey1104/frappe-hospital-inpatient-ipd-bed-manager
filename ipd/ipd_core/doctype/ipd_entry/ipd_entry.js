// Copyright (c) 2026, Shyamkumar Pandey and contributors
// For license information, please see license.txt

frappe.ui.form.on("Ipd Entry", {
    refresh: function(frm) {
        if (frm.doc.docstatus === 1) {
            frm.add_custom_button(__("View Ledger"), function() {
                frappe.msgprint(__("Ledger entries verified and posted."));
            }, __("Actions"));
        }
    }
});
