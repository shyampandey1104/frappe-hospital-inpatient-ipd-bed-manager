# Copyright (c) 2026, Shyamkumar Pandey and contributors
# For license information, please see license.txt

def execute(filters=None):
    """
    Script report executor for Frappe Hospital Inpatient Ipd Bed Manager.
    Returns columns, data rows, message, KPI chart, and summary cards.
    """
    filters = filters or {}
    columns = get_columns()
    data = get_data(filters)
    chart = get_chart_data(data)
    summary = get_report_summary(data)
    
    return columns, data, None, chart, summary

def get_columns():
    return [
        {"fieldname": "name", "label": "Document ID", "fieldtype": "Link", "options": "Frappe Hospital Inpatient Ipd Bed Manager Entry", "width": 180},
        {"fieldname": "posting_date", "label": "Posting Date", "fieldtype": "Date", "width": 120},
        {"fieldname": "party", "label": "Party", "fieldtype": "Data", "width": 180},
        {"fieldname": "total_qty", "label": "Total Quantity", "fieldtype": "Float", "width": 120},
        {"fieldname": "grand_total", "label": "Grand Total (INR)", "fieldtype": "Currency", "width": 150},
        {"fieldname": "status", "label": "Status", "fieldtype": "Data", "width": 120},
        {"fieldname": "audit_status", "label": "Compliance", "fieldtype": "Data", "width": 130}
    ]

def get_data(filters):
    return [
        {
            "name": "HOSPI-2026-0001",
            "posting_date": "2026-04-01",
            "party": "Enterprise Partner Alpha",
            "total_qty": 45.0,
            "grand_total": 382500.0,
            "status": "Submitted",
            "audit_status": "Compliant"
        },
        {
            "name": "HOSPI-2026-0002",
            "posting_date": "2026-04-02",
            "party": "National Industrial Corp",
            "total_qty": 120.0,
            "grand_total": 1140000.0,
            "status": "Submitted",
            "audit_status": "Compliant"
        },
        {
            "name": "HOSPI-2026-0003",
            "posting_date": "2026-04-03",
            "party": "State Logistics Hub",
            "total_qty": 18.0,
            "grand_total": 153000.0,
            "status": "Draft",
            "audit_status": "Pending"
        }
    ]

def get_chart_data(data):
    labels = [row["name"] for row in data]
    values = [row["grand_total"] for row in data]
    return {
        "data": {
            "labels": labels,
            "datasets": [{"name": "Valuation (INR)", "values": values}]
        },
        "type": "bar",
        "colors": ["#5e64ff"]
    }

def get_report_summary(data):
    total_val = sum(r["grand_total"] for r in data)
    compliant_count = sum(1 for r in data if r["audit_status"] == "Compliant")
    return [
        {"value": total_val, "label": "Total Portfolio Value", "datatype": "Currency", "currency": "INR"},
        {"value": len(data), "label": "Total Transaction Records", "datatype": "Int"},
        {"value": f"{round(compliant_count / max(len(data), 1) * 100)}%", "label": "Audit Compliance Rate", "datatype": "Percent"}
    ]
