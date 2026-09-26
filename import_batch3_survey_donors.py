import sys
import database

sys.stdout.reconfigure(encoding='utf-8')

batch3_donors = [
    # FNE (6)
    {"name": "আব্দুর রহমান", "phone": "01628326536", "department": "FNE", "session_val": "2025-26", "blood_group": "B+", "is_badhon_member": True},
    {"name": "তৌসিফ হাসান", "phone": "01867421897", "department": "FNE", "session_val": "2025-26", "blood_group": "B+", "is_badhon_member": True},
    {"name": "শাহরিয়ার", "phone": "01896084566", "department": "FNE", "session_val": "2025-26", "blood_group": "O+", "is_badhon_member": True},
    {"name": "সামছুল হুদা রাফি", "phone": "01990686764", "department": "FNE", "session_val": "2025-26", "blood_group": "B+", "is_badhon_member": True},
    {"name": "মুশফিক আলভী", "phone": "01723277658", "department": "FNE", "session_val": "2025-26", "blood_group": "O+", "is_badhon_member": False},
    {"name": "অফিক চক্রবর্তী", "phone": "01742860803", "department": "FNE", "session_val": "2025-26", "blood_group": "A+", "is_badhon_member": False},

    # THM (11)
    {"name": "আদনান", "phone": "01704357227", "department": "THM", "session_val": "2025-26", "blood_group": "A+", "is_badhon_member": True},
    {"name": "জোবায়ের", "phone": "01634303738", "department": "THM", "session_val": "2025-26", "blood_group": "A+", "is_badhon_member": True},
    {"name": "শাবনুর", "phone": "01931479411", "department": "THM", "session_val": "2025-26", "blood_group": "O+", "is_badhon_member": True},
    {"name": "অংকিত", "phone": "01971613661", "department": "THM", "session_val": "2025-26", "blood_group": "O+", "is_badhon_member": False},
    {"name": "কিবরিয়া", "phone": "01878210222", "department": "THM", "session_val": "2025-26", "blood_group": "O+", "is_badhon_member": False},
    {"name": "Freitha", "phone": "01345883568", "department": "THM", "session_val": "2025-26", "blood_group": "B+", "is_badhon_member": True},
    {"name": "Akash", "phone": "01811268232", "department": "THM", "session_val": "2025-26", "blood_group": "A+", "is_badhon_member": False},
    {"name": "Mobarok", "phone": "01308515066", "department": "THM", "session_val": "2025-26", "blood_group": "B+", "is_badhon_member": True},
    {"name": "Arman", "phone": "01300937274", "department": "THM", "session_val": "2025-26", "blood_group": "O+", "is_badhon_member": True},
    {"name": "Mezba", "phone": "01301687733", "department": "THM", "session_val": "2025-26", "blood_group": "B+", "is_badhon_member": False},
    {"name": "সাজ্জাদ সরকার", "phone": "01315933863", "department": "THM", "session_val": "2025-26", "blood_group": "A+", "is_badhon_member": False},

    # ASVM (6)
    {"name": "Anolina Hasda", "phone": "01333511992", "department": "ASVM", "session_val": "2025-26", "blood_group": "AB+", "is_badhon_member": False},
    {"name": "Shoriat Hossain", "phone": "01958625340", "department": "ASVM", "session_val": "2025-26", "blood_group": "B+", "is_badhon_member": True},
    {"name": "Shihab Uddin", "phone": "01830888862", "department": "ASVM", "session_val": "2025-26", "blood_group": "O+", "is_badhon_member": False},
    {"name": "Siam Ahmed", "phone": "01892463218", "department": "ASVM", "session_val": "2025-26", "blood_group": "O+", "is_badhon_member": False},
    {"name": "MD. Al Mamun", "phone": "01828548271", "department": "ASVM", "session_val": "2025-26", "blood_group": "B+", "is_badhon_member": False},
    {"name": "Mithun Mandal", "phone": "01717197213", "department": "ASVM", "session_val": "2025-26", "blood_group": "A+", "is_badhon_member": True},

    # Sociology (10)
    {"name": "Adnan", "phone": "01783509906", "department": "Sociology", "session_val": "2025-26", "blood_group": "B+", "is_badhon_member": False},
    {"name": "Sajib Hossain", "phone": "01990429302", "department": "Sociology", "session_val": "2025-26", "blood_group": "AB+", "is_badhon_member": True},
    {"name": "Mostakim", "phone": "01850512107", "department": "Sociology", "session_val": "2025-26", "blood_group": "B+", "is_badhon_member": True},
    {"name": "Mubin Mahfuz", "phone": "01516576431", "department": "Sociology", "session_val": "2025-26", "blood_group": "A+", "is_badhon_member": True},
    {"name": "Ahmad", "phone": "01870315860", "department": "Sociology", "session_val": "2025-26", "blood_group": "B+", "is_badhon_member": True},
    {"name": "Tanzim", "phone": "01916997036", "department": "Sociology", "session_val": "2025-26", "blood_group": "B+", "is_badhon_member": True},
    {"name": "Naoknoy", "phone": "01611536628", "department": "Sociology", "session_val": "2025-26", "blood_group": "A+", "is_badhon_member": True},
    {"name": "Tastia", "phone": "01798473359", "department": "Sociology", "session_val": "2025-26", "blood_group": "O+", "is_badhon_member": True},
    {"name": "Nur-Jahan", "phone": "01758924862", "department": "Sociology", "session_val": "2025-26", "blood_group": "B-", "is_badhon_member": True},
    {"name": "Halima", "phone": "01916940204", "department": "Sociology", "session_val": "2025-26", "blood_group": "AB+", "is_badhon_member": True}
]

def run_import():
    database.init_db()
    inserted_count = 0
    
    for donor in batch3_donors:
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
