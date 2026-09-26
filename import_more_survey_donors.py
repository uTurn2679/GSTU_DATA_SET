import sys
import database

sys.stdout.reconfigure(encoding='utf-8')

new_survey_donors = [
    # ACCF (1)
    {"name": "নুসরাত জাহান উমি", "phone": "01829769453", "department": "ACCF", "session_val": "2025-26", "blood_group": "B+", "is_badhon_member": False},

    # Econ (14)
    {"name": "হৃদয় সরকার", "phone": "01871828716", "department": "Econ", "session_val": "2025-26", "blood_group": "B+", "is_badhon_member": False},
    {"name": "মো: শাহরিয়ার", "phone": "01836473606", "department": "Econ", "session_val": "2025-26", "blood_group": "B+", "is_badhon_member": True},
    {"name": "মো: ইমন হাসান", "phone": "01301361767", "department": "Econ", "session_val": "2025-26", "blood_group": "O+", "is_badhon_member": True},
    {"name": "রিয়াজ রহমান সজল", "phone": "01822786014", "department": "Econ", "session_val": "2025-26", "blood_group": "B+", "is_badhon_member": True},
    {"name": "হেজবুল্লাহ আল মামুন", "phone": "01788097475", "department": "Econ", "session_val": "2025-26", "blood_group": "B+", "is_badhon_member": True},
    {"name": "নিলয় হোসেন", "phone": "01612935618", "department": "Econ", "session_val": "2025-26", "blood_group": "AB+", "is_badhon_member": True},
    {"name": "প্রদীপ স্বর্ণকার", "phone": "01930980852", "department": "Econ", "session_val": "2025-26", "blood_group": "AB+", "is_badhon_member": False},
    {"name": "মো: আবিদ হোসেন", "phone": "01949636448", "department": "Econ", "session_val": "2025-26", "blood_group": "B+", "is_badhon_member": True},
    {"name": "তামসুবা খানম", "phone": "01707168250", "department": "Econ", "session_val": "2025-26", "blood_group": "B+", "is_badhon_member": True},
    {"name": "তমা রায়", "phone": "01330315019", "department": "Econ", "session_val": "2025-26", "blood_group": "B+", "is_badhon_member": True},
    {"name": "জান্নাত", "phone": "01786284703", "department": "Econ", "session_val": "2025-26", "blood_group": "O+", "is_badhon_member": True},
    {"name": "নীপা", "phone": "01560031076", "department": "Econ", "session_val": "2025-26", "blood_group": "O+", "is_badhon_member": True},
    {"name": "অপর্ণা", "phone": "01782913388", "department": "Econ", "session_val": "2025-26", "blood_group": "O+", "is_badhon_member": False},
    {"name": "মাহেক মাহমুদ অনিক", "phone": "01613140222", "department": "Econ", "session_val": "2025-26", "blood_group": "O+", "is_badhon_member": False}
]

def run_import():
    database.init_db()
    inserted_count = 0
    
    for donor in new_survey_donors:
        existing = database.get_donors(search=donor["phone"])
        if len(existing) == 0:
            database.add_donor(
                name=donor["name"],
                department=donor["department"],
                session_val=donor["session_val"],
                blood_group=donor["blood_group"],
                phone=donor["phone"],
                last_donation_date=None,
                total_donations=0,
                is_badhon_member=donor["is_badhon_member"],
                is_available=True
            )
            inserted_count += 1
            print(f"[{inserted_count}] Imported Willing Donor: {donor['name']} ({donor['blood_group']}, {donor['department']}, {donor['phone']})")

    print(f"\nSuccessfully imported {inserted_count} new blood donors into database!")

if __name__ == '__main__':
    run_import()
