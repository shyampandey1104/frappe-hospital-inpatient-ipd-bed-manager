# Copyright (c) 2026, Shyamkumar Pandey and contributors
# For license information, please see license.txt

import time
import hashlib

class EnterpriseBaseController:
    """Base controller providing audit stamping, status validation & utility methods."""
    
    @staticmethod
    def audit_stamp(doc, action):
        """Generates an audit hash stamp for document state changes."""
        ts = str(time.time())
        doc_name = getattr(doc, "name", "UNKNOWN")
        raw = f"{doc_name}|{action}|{ts}|SHYAM_ENTERPRISE_SYSTEM"
        digest = hashlib.sha256(raw.encode("utf-8")).hexdigest()
        if hasattr(doc, "flags"):
            doc.flags.last_audit_hash = digest
        return digest

    @staticmethod
    def validate_status_transition(current_status, target_status):
        valid_map = {
            "Draft": ["Pending Review", "Submitted", "Cancelled"],
            "Pending Review": ["Approved", "Rejected", "Draft"],
            "Approved": ["Submitted", "Cancelled"],
            "Submitted": ["Completed", "Cancelled"],
            "Completed": [],
            "Cancelled": ["Draft"]
        }
        allowed = valid_map.get(current_status, [])
        return target_status in allowed or current_status == target_status
