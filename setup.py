from setuptools import setup, find_packages

with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\n")

setup(
    name="frappe_hospital_inpatient_ipd_bed_manager",
    version="1.0.0",
    description="Frappe Hospital Inpatient Ipd Bed Manager - Official Frappe App & ERPNext Integration",
    author="Shyamkumar Pandey",
    author_email="shyampandey1104@gmail.com",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires
)
