# Copyright (c) 2026, Shyamkumar Pandey and contributors
# For license information, please see license.txt

app_name = "ipd"
app_title = "Frappe Hospital Inpatient Ipd Bed Manager"
app_publisher = "Shyamkumar Pandey"
app_description = "Frappe Hospital Inpatient Ipd Bed Manager - Enterprise Multi-DocType Solution for Frappe & ERPNext"
app_email = "shyampandey1104@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------
app_include_css = "/assets/ipd/css/ipd.bundle.css"
app_include_js = "/assets/ipd/js/ipd.bundle.js"

# Document Events
# ---------------
doc_events = {
    "Frappe Hospital Inpatient Ipd Bed Manager Entry": {
        "validate": "ipd.services.validator.EnterpriseValidationEngine.validate_compliance_rules",
        "on_submit": "ipd.services.integration_service.EnterpriseIntegrationService.verify_remote_status"
    }
}

# Scheduled Background Tasks
# --------------------------
scheduler_events = {
    "hourly": [
        "ipd.tasks.hourly_sync"
    ],
    "daily": [
        "ipd.tasks.daily_reconciliation"
    ],
    "weekly": [
        "ipd.tasks.weekly_digest"
    ]
}
