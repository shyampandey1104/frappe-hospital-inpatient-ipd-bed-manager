import unittest
from ipd.engine import IPDBedManagerEngine, BedMaster

class TestIPDBedManager(unittest.TestCase):
    def test_ipd_bed_allocation_and_discharge(self):
        engine = IPDBedManagerEngine()
        bed_icu = BedMaster(bed_id="ICU-101", ward_type="ICU", daily_tariff=8500.0, has_ventilator_support=True)
        engine.register_bed(bed_icu)

        admission = engine.admit_patient(
            admission_id="IPD-2026-554",
            patient_name="Rajesh Verma",
            bed_id="ICU-101",
            admission_date_str="2026-05-01",
            tpa_insurer="Star Health",
            pre_auth_limit=50000.0
        )

        self.assertTrue(engine.beds["ICU-101"].is_occupied)

        summary = engine.process_discharge_and_settlement(
            admission=admission,
            discharge_date_str="2026-05-05",
            pharmacy_lab_total=18000.0
        )

        self.assertEqual(summary.stay_duration_days, 4)
        self.assertEqual(summary.room_charges, 34000.0)
        self.assertEqual(summary.nursing_charges, 10000.0)
        self.assertEqual(summary.gross_hospital_bill, 62000.0)
        self.assertEqual(summary.tpa_approved_claim, 50000.0)
        self.assertEqual(summary.patient_co_pay_payable, 12000.0)
        self.assertFalse(engine.beds["ICU-101"].is_occupied)

if __name__ == "__main__":
    unittest.main()
