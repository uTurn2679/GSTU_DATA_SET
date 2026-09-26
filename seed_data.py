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
        "is_available": True,
        "history_dates": ["2026-05-12", "2025-12-10", "2025-07-04", "2024-11-20"]
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
        "is_available": True,
        "history_dates": ["2026-02-18", "2025-08-15"]
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
        "is_available": True,
        "history_dates": ["2025-11-30", "2025-06-12", "2024-12-01", "2024-05-15", "2023-10-10", "2023-03-25"]
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
        "is_available": False,
        "history_dates": ["2026-08-10"]
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
        "is_available": True,
        "history_dates": ["2026-01-15", "2025-08-01", "2025-02-14", "2024-09-10", "2024-03-01"]
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
        "is_available": True,
        "history_dates": []
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
        "is_available": True,
        "history_dates": ["2026-04-05", "2025-10-12", "2025-04-01"]
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
        "is_available": False,
        "history_dates": ["2026-07-20"]
    }
]

def seed():
    database.init_db()
    existing = database.get_donors()
    if len(existing) == 0:
        for data in sample_donors:
            history_dates = data.pop("history_dates", [])
            donor_id = database.add_donor(**data)
            for d in history_dates:
                # Add each date to donation_history
                database.add_donation_history(donor_id, d)
        print(f"Successfully seeded database with {len(sample_donors)} donors and their donation histories!")
    else:
        print(f"Database already contains {len(existing)} donors.")

if __name__ == '__main__':
    seed()
