# Copyright (c) 2026, Shyamkumar Pandey and contributors
# For license information, please see license.txt

app_name = "ipd"
app_title = "Frappe Hospital Inpatient Ipd Bed Manager"
app_publisher = "Shyamkumar Pandey"
app_description = "Frappe Hospital Inpatient Ipd Bed Manager for Frappe and ERPNext"
app_email = "shyampandey1104@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------
app_include_css = "/assets/ipd/css/ipd.bundle.css"
app_include_js = "/assets/ipd/js/ipd.bundle.js"

# Document Events
# ---------------
doc_events = {
    "DocType Event": {
        "on_submit": "ipd.engine.on_document_submit",
        "on_cancel": "ipd.engine.on_document_cancel"
    }
}

# Scheduled Tasks
# ---------------
scheduler_events = {
    "daily": [
        "ipd.engine.daily_scheduled_sync"
    ]
}
