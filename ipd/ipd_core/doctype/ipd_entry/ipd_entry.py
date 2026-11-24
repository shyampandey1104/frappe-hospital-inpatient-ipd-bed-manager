# Copyright (c) 2026, Shyamkumar Pandey and contributors
# For license information, please see license.txt

try:
    import frappe
    from frappe.model.document import Document
except ImportError:
    class Document:
        def __init__(self, *args, **kwargs):
            self.__dict__.update(kwargs)
            if not hasattr(self, "name"):
                self.name = "HOSPI-2026-0001"
            if not hasattr(self, "items"):
                self.items = []
        def get(self, key, default=None):
            return getattr(self, key, default)
        def set(self, key, value):
            setattr(self, key, value)
    frappe = None

from ipd.controllers.base_controller import EnterpriseBaseController
from ipd.services.validator import EnterpriseValidationEngine
from ipd.services.integration_service import EnterpriseIntegrationService

class HospitalInpatientIpdBedManagerEntry(Document):
    """
    Primary transactional document controller for Frappe Hospital Inpatient Ipd Bed Manager.
    Coordinates multi-item line aggregation, statutory validations,
    state-machine transitions, and tamper-proof audit trails.
    """

    def validate(self):
        """Pre-save verification and line-item aggregation."""
        self.validate_header_fields()
        self.calculate_totals()
        EnterpriseValidationEngine.validate_compliance_rules(self)

    def validate_header_fields(self):
        if not getattr(self, "title", None):
            setattr(self, "title", f"Frappe Hospital Inpatient Ipd Bed Manager - " + str(getattr(self, "name", "Draft")))
        if not getattr(self, "party", None):
            setattr(self, "party", "DEFAULT-ENTERPRISE-PARTY")

    def calculate_totals(self):
        """Aggregate quantities and valuations across child table items."""
        total_qty = 0.0
        total_amount = 0.0

        items = getattr(self, "items", []) or []
        for row in items:
            qty = float(getattr(row, "qty", 0.0) or 0.0)
            rate = float(getattr(row, "rate", 0.0) or 0.0)
            amount = round(qty * rate, 2)
            if hasattr(row, "amount"):
                row.amount = amount
            elif isinstance(row, dict):
                row["amount"] = amount
            total_qty += qty
            total_amount += amount

        self.total_qty = total_qty
        self.total_amount = total_amount
        self.grand_total = total_amount

    def on_submit(self):
        """Submit event: locks record, triggers integration service & logs audit."""
        self.status = "Submitted"
        self.audit_status = "Compliant"
        EnterpriseBaseController.audit_stamp(self, "SUBMITTED")
        EnterpriseIntegrationService.dispatch_webhook("ON_SUBMIT", {
            "doctype": "Frappe Hospital Inpatient Ipd Bed Manager Entry",
            "name": getattr(self, "name", ""),
            "grand_total": getattr(self, "grand_total", 0.0),
            "party": getattr(self, "party", "")
        })

    def on_cancel(self):
        """Cancel event: triggers reversal workflow and audit flag."""
        self.status = "Cancelled"
        self.audit_status = "Flagged"
        EnterpriseBaseController.audit_stamp(self, "CANCELLED")
        EnterpriseIntegrationService.dispatch_webhook("ON_CANCEL", {
            "doctype": "Frappe Hospital Inpatient Ipd Bed Manager Entry",
            "name": getattr(self, "name", "")
        })
