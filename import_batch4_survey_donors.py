import sys
import database

sys.stdout.reconfigure(encoding='utf-8')

batch4_donors = [
    # ESD (7)
    {"name": "আব্দুর রহমান", "phone": "01628326536", "department": "ESD", "session_val": "2025-26", "blood_group": "O+", "is_badhon_member": False},
    {"name": "তামিম ইকবাল", "phone": "01867421897", "department": "ESD", "session_val": "2025-26", "blood_group": "B+", "is_badhon_member": True},
    {"name": "শাহরিয়ার", "phone": "01896084566", "department": "ESD", "session_val": "2025-26", "blood_group": "B+", "is_badhon_member": True},
    {"name": "তানজিল সানি", "phone": "01990686764", "department": "ESD", "session_val": "2025-26", "blood_group": "O+", "is_badhon_member": True},
    {"name": "রাকিব", "phone": "01556325670", "department": "ESD", "session_val": "2025-26", "blood_group": "B+", "is_badhon_member": True},
    {"name": "মুশফিক আলভী", "phone": "01723277658", "department": "ESD", "session_val": "2025-26", "blood_group": "A+", "is_badhon_member": False},
    {"name": "অফিক চক্রবর্তী", "phone": "01742860803", "department": "ESD", "session_val": "2025-26", "blood_group": "O+", "is_badhon_member": False},

    # PS (14)
    {"name": "আহমাদ", "phone": "01704357227", "department": "PS", "session_val": "2025-26", "blood_group": "A+", "is_badhon_member": True},
    {"name": "জুবায়ের", "phone": "01634303738", "department": "PS", "session_val": "2025-26", "blood_group": "A+", "is_badhon_member": True},
    {"name": "শাদনান", "phone": "01931479411", "department": "PS", "session_val": "2025-26", "blood_group": "O+", "is_badhon_member": True},
    {"name": "অঙ্কিত", "phone": "01971613661", "department": "PS", "session_val": "2025-26", "blood_group": "O+", "is_badhon_member": False},
    {"name": "কিবরিয়া", "phone": "01878210222", "department": "PS", "session_val": "2025-26", "blood_group": "O+", "is_badhon_member": False},
    {"name": "Freitha", "phone": "01345883568", "department": "PS", "session_val": "2025-26", "blood_group": "B-", "is_badhon_member": True},
    {"name": "Akash", "phone": "01811268232", "department": "PS", "session_val": "2025-26", "blood_group": "A+", "is_badhon_member": False},
    {"name": "Mobarok", "phone": "01308515066", "department": "PS", "session_val": "2025-26", "blood_group": "B+", "is_badhon_member": True},
    {"name": "Arman", "phone": "01300937274", "department": "PS", "session_val": "2025-26", "blood_group": "O+", "is_badhon_member": True},
    {"name": "Mezba", "phone": "01301687733", "department": "PS", "session_val": "2025-26", "blood_group": "B+", "is_badhon_member": False},
    {"name": "সাজ্জাদ সরকার", "phone": "01315933863", "department": "PS", "session_val": "2025-26", "blood_group": "A+", "is_badhon_member": False},
    {"name": "সমারিতা বৈদ্য", "phone": "01814154698", "department": "PS", "session_val": "2025-26", "blood_group": "O+", "is_badhon_member": False},
    {"name": "নুসরাত জাহান", "phone": "01860522156", "department": "PS", "session_val": "2025-26", "blood_group": "A+", "is_badhon_member": False},
    {"name": "Smita Ghosh", "phone": "01828651309", "department": "PS", "session_val": "2025-26", "blood_group": "A+", "is_badhon_member": True},

    # Physics (6)
    {"name": "মো: সারাফত হোসেন", "phone": "01609148935", "department": "Physics", "session_val": "2025-26", "blood_group": "A+", "is_badhon_member": True},
    {"name": "মো: শওকত হোসেন", "phone": "01990429302", "department": "Physics", "session_val": "2025-26", "blood_group": "AB+", "is_badhon_member": True},
    {"name": "তানভীর আহমেদ সজল", "phone": "01850512107", "department": "Physics", "session_val": "2025-26", "blood_group": "O+", "is_badhon_member": True},
    {"name": "রাজিবুল সিকদার", "phone": "01959808059", "department": "Physics", "session_val": "2025-26", "blood_group": "O+", "is_badhon_member": True},
    {"name": "রিপন", "phone": "0175892219", "department": "Physics", "session_val": "2025-26", "blood_group": "O+", "is_badhon_member": True},
    {"name": "চারুক দেবাশীষ", "phone": "017289191066", "department": "Physics", "session_val": "2025-26", "blood_group": "O+", "is_badhon_member": True},

    # English (2)
    {"name": "Rebeka Sultana", "phone": "01839758897", "department": "English", "session_val": "2025-26", "blood_group": "O+", "is_badhon_member": False},
    {"name": "নুসরাত জাহান", "phone": "01326744970", "department": "English", "session_val": "2025-26", "blood_group": "B+", "is_badhon_member": True}
]

def run_import():
    database.init_db()
    inserted_count = 0
    
    for donor in batch4_donors:
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
