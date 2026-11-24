# Copyright (c) 2026, Shyamkumar Pandey and contributors
# For license information, please see license.txt

class EnterpriseValidationEngine:
    """Multi-tiered compliance and integrity rule validator."""
    
    @staticmethod
    def validate_compliance_rules(doc):
        items = getattr(doc, "items", []) or []
        for idx, row in enumerate(items, start=1):
            qty = float(getattr(row, "qty", 0.0) or 0.0)
            rate = float(getattr(row, "rate", 0.0) or 0.0)
            if qty < 0:
                raise ValueError(f"Row {idx}: Quantity cannot be negative")
            if rate < 0:
                raise ValueError(f"Row {idx}: Rate cannot be negative")
        return True
