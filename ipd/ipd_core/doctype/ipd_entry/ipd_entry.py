# Copyright (c) 2026, Shyamkumar Pandey and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class IpdEntry(Document):
    def validate(self):
        """Pre-save validations."""
        pass

    def on_submit(self):
        """Post-submit ledger and audit triggers."""
        pass

    def on_cancel(self):
        """Cancellation reversal triggers."""
        pass
