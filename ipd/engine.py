"""Hospital In-Patient Department (IPD), Ward Bed Allocation & TPA Cashless Billing Engine."""

from datetime import datetime, date
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field


@dataclass
class BedMaster:
    bed_id: str
    ward_type: str  # ICU, DELUXE, SEMI_PRIVATE, GENERAL
    daily_tariff: float
    has_ventilator_support: bool = False
    is_occupied: bool = False
    current_patient_id: Optional[str] = None


@dataclass
class IPDAdmission:
    admission_id: str
    patient_name: str
    assigned_bed_id: str
    ward_type: str
    daily_tariff: float
    admission_date: str
    tpa_insurer: Optional[str] = None
    pre_auth_approved_limit: float = 0.0


@dataclass
class IPDDischargeSummary:
    admission_id: str
    stay_duration_days: int
    room_charges: float
    nursing_charges: float
    investigations_and_pharmacy: float
    gross_hospital_bill: float
    tpa_approved_claim: float
    patient_co_pay_payable: float


class IPDBedManagerEngine:
    """Enterprise Hospital In-Patient Department (IPD) Bed and Tariff Billing Controller."""

    NURSING_DAILY_RATES = {
        "ICU": 2500.0,
        "DELUXE": 1200.0,
        "SEMI_PRIVATE": 800.0,
        "GENERAL": 400.0
    }

    def __init__(self):
        self.beds: Dict[str, BedMaster] = {}

    def register_bed(self, bed: BedMaster):
        self.beds[bed.bed_id] = bed

    def admit_patient(
        self,
        admission_id: str,
        patient_name: str,
        bed_id: str,
        admission_date_str: str,
        tpa_insurer: Optional[str] = None,
        pre_auth_limit: float = 0.0
    ) -> IPDAdmission:
        if bed_id not in self.beds:
            raise ValueError(f"Bed {bed_id} does not exist in ward registry.")
        bed = self.beds[bed_id]
        if bed.is_occupied:
            raise ValueError(f"Bed {bed_id} is currently occupied by patient {bed.current_patient_id}.")

        bed.is_occupied = True
        bed.current_patient_id = admission_id

        return IPDAdmission(
            admission_id=admission_id,
            patient_name=patient_name,
            assigned_bed_id=bed_id,
            ward_type=bed.ward_type,
            daily_tariff=bed.daily_tariff,
            admission_date=admission_date_str,
            tpa_insurer=tpa_insurer,
            pre_auth_approved_limit=pre_auth_limit
        )

    def process_discharge_and_settlement(
        self,
        admission: IPDAdmission,
        discharge_date_str: str,
        pharmacy_lab_total: float
    ) -> IPDDischargeSummary:
        d_in = datetime.strptime(admission.admission_date, "%Y-%m-%d").date()
        d_out = datetime.strptime(discharge_date_str, "%Y-%m-%d").date()
        stay_days = max(1, (d_out - d_in).days)

        room_charges = round(stay_days * admission.daily_tariff, 2)
        nursing_rate = self.NURSING_DAILY_RATES.get(admission.ward_type, 600.0)
        nursing_charges = round(stay_days * nursing_rate, 2)
        gross_bill = round(room_charges + nursing_charges + pharmacy_lab_total, 2)

        approved_claim = min(gross_bill, admission.pre_auth_approved_limit)
        patient_due = max(0.0, round(gross_bill - approved_claim, 2))

        # Release Bed
        if admission.assigned_bed_id in self.beds:
            self.beds[admission.assigned_bed_id].is_occupied = False
            self.beds[admission.assigned_bed_id].current_patient_id = None

        return IPDDischargeSummary(
            admission_id=admission.admission_id,
            stay_duration_days=stay_days,
            room_charges=room_charges,
            nursing_charges=nursing_charges,
            investigations_and_pharmacy=pharmacy_lab_total,
            gross_hospital_bill=gross_bill,
            tpa_approved_claim=approved_claim,
            patient_co_pay_payable=patient_due
        )
