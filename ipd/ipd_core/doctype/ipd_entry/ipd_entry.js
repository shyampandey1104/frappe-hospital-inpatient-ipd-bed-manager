// Copyright (c) 2026, Shyamkumar Pandey and contributors
// For license information, please see license.txt

frappe.ui.form.on("Frappe Hospital Inpatient Ipd Bed Manager Entry", {
    refresh: function(frm) {
        // Custom indicator badges
        if (frm.doc.status === "Submitted") {
            frm.page.set_indicator(__("Submitted & Verified"), "green");
        } else if (frm.doc.status === "Draft") {
            frm.page.set_indicator(__("Draft Pending Review"), "orange");
        }

        // Enterprise Action Buttons
        if (frm.doc.docstatus === 1) {
            frm.add_custom_button(__("View Audit Trail"), function() {
                frappe.route_options = {
                    "reference_doctype": "Frappe Hospital Inpatient Ipd Bed Manager Entry",
                    "reference_name": frm.doc.name
                };
                frappe.set_route("List", "Frappe Hospital Inpatient Ipd Bed Manager Audit Log");
            }, __("Actions"));

            frm.add_custom_button(__("Verify Gateway Sync"), function() {
                frappe.call({
                    method: "ipd.api.get_status_overview",
                    callback: function(r) {
                        if (r.message) {
                            frappe.msgprint({
                                title: __("Gateway Status"),
                                indicator: "green",
                                message: __("Integration verified: {0}", [r.message.operational_status])
                            });
                        }
                    }
                });
            }, __("Actions"));
        }
    },

    validate: function(frm) {
        if (!frm.doc.items || frm.doc.items.length === 0) {
            frappe.msgprint(__("Please add at least one line item before saving."));
        }
    }
});

// Child Table Dynamic Recalculation Handlers
frappe.ui.form.on("Frappe Hospital Inpatient Ipd Bed Manager Item", {
    qty: function(frm, cdt, cdn) {
        calculate_row_amount(frm, cdt, cdn);
    },
    rate: function(frm, cdt, cdn) {
        calculate_row_amount(frm, cdt, cdn);
    },
    items_remove: function(frm) {
        calculate_totals(frm);
    }
});

function calculate_row_amount(frm, cdt, cdn) {
    let row = locals[cdt][cdn];
    let qty = flt(row.qty);
    let rate = flt(row.rate);
    let amount = round_based_on_currency(qty * rate, frm.doc.currency);
    frappe.model.set_value(cdt, cdn, "amount", amount);
    calculate_totals(frm);
}

function calculate_totals(frm) {
    let total_qty = 0;
    let total_amount = 0;
    (frm.doc.items || []).forEach(function(row) {
        total_qty += flt(row.qty);
        total_amount += flt(row.amount);
    });
    frm.set_value("total_qty", total_qty);
    frm.set_value("total_amount", total_amount);
    frm.set_value("grand_total", total_amount);
}
