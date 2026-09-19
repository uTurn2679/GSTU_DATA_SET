import database

sample_donors = [
    {
        "name": "Md. Rakibul Hasan",
        "department": "CSE",
        "session_val": "2020-21",
        "blood_group": "A+",
        "phone": "01711223344",
        "last_donation_date": "2026-05-12",
        "total_donations": 4,
        "is_badhon_member": True,
        "is_available": True
    },
    {
        "name": "Nusrat Jahan Tanvin",
        "department": "EEE",
        "session_val": "2021-22",
        "blood_group": "B+",
        "phone": "01822334455",
        "last_donation_date": "2026-02-18",
        "total_donations": 2,
        "is_badhon_member": True,
        "is_available": True
    },
    {
        "name": "Arifur Rahman",
        "department": "CSE",
        "session_val": "2019-20",
        "blood_group": "O+",
        "phone": "01933445566",
        "last_donation_date": "2025-11-30",
        "total_donations": 6,
        "is_badhon_member": True,
        "is_available": True
    },
    {
        "name": "Sumaiya Akter",
        "department": "BBA",
        "session_val": "2022-23",
        "blood_group": "AB+",
        "phone": "01544556677",
        "last_donation_date": "2026-08-10",
        "total_donations": 1,
        "is_badhon_member": False,
        "is_available": False
    },
    {
        "name": "Mahmudul Islam",
        "department": "Physics",
        "session_val": "2020-21",
        "blood_group": "O-",
        "phone": "01655667788",
        "last_donation_date": "2026-01-15",
        "total_donations": 5,
        "is_badhon_member": True,
        "is_available": True
    },
    {
        "name": "Tanzila Rahman",
        "department": "Chemistry",
        "session_val": "2021-22",
        "blood_group": "A-",
        "phone": "01766778899",
        "last_donation_date": None,
        "total_donations": 0,
        "is_badhon_member": False,
        "is_available": True
    },
    {
        "name": "Shakil Ahmed",
        "department": "Mathematics",
        "session_val": "2019-20",
        "blood_group": "B-",
        "phone": "01877889900",
        "last_donation_date": "2026-04-05",
        "total_donations": 3,
        "is_badhon_member": True,
        "is_available": True
    },
    {
        "name": "Faria Hossain",
        "department": "CSE",
        "session_val": "2022-23",
        "blood_group": "AB-",
        "phone": "01988990011",
        "last_donation_date": "2026-07-20",
        "total_donations": 1,
        "is_badhon_member": False,
        "is_available": False
    }
]

def seed():
    database.init_db()
    existing = database.get_donors()
    if len(existing) == 0:
        for data in sample_donors:
            database.add_donor(**data)
        print(f"Successfully seeded database with {len(sample_donors)} donors!")
    else:
        print(f"Database already contains {len(existing)} donors.")

if __name__ == '__main__':
    seed()
