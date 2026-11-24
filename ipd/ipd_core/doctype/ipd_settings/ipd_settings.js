// Copyright (c) 2026, Shyamkumar Pandey and contributors
// For license information, please see license.txt

frappe.ui.form.on("Frappe Hospital Inpatient Ipd Bed Manager Settings", {
    refresh: function(frm) {
        frm.add_custom_button(__("Test API Connection"), function() {
            frm.call({
                doc: frm.doc,
                method: "test_connection",
                callback: function(r) {
                    if (r.message && r.message.status === "success") {
                        frappe.msgprint({
                            title: __("Connection Test Succeeded"),
                            indicator: "green",
                            message: __(r.message.message)
                        });
                    }
                }
            });
        });
    }
});
