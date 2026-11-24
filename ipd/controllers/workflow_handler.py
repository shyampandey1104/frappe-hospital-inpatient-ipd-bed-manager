# Copyright (c) 2026, Shyamkumar Pandey and contributors
# For license information, please see license.txt

from ipd.controllers.base_controller import EnterpriseBaseController

class WorkflowStateMachine:
    """Enterprise state-machine managing lifecycle transitions and permissions."""
    
    @classmethod
    def apply_transition(cls, doc, target_status, user="Administrator"):
        current_status = getattr(doc, "status", "Draft")
        if not EnterpriseBaseController.validate_status_transition(current_status, target_status):
            raise ValueError(f"Invalid state transition from {current_status} to {target_status}")
        
        doc.status = target_status
        EnterpriseBaseController.audit_stamp(doc, f"TRANSITION_TO_{target_status.upper()}")
        return True
