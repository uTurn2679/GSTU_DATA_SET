import sys
import database

sys.stdout.reconfigure(encoding='utf-8')

willing_donors = [
    # BGE (9)
    {"name": "ফারহান মোস্তাক", "phone": "01731511328", "department": "BGE", "session_val": "2025-26", "blood_group": "B-", "is_badhon_member": False},
    {"name": "তাসফিয়া মেহজাবীন", "phone": "01812539532", "department": "BGE", "session_val": "2025-26", "blood_group": "AB+", "is_badhon_member": True},
    {"name": "শেখ মেহিয়েল আবীর", "phone": "01572972418", "department": "BGE", "session_val": "2025-26", "blood_group": "B+", "is_badhon_member": True},
    {"name": "মেজবা উল হক (হিমেল)", "phone": "01316922629", "department": "BGE", "session_val": "2025-26", "blood_group": "B+", "is_badhon_member": True},
    {"name": "আহসান হাবীব রবিন", "phone": "01793088886", "department": "BGE", "session_val": "2025-26", "blood_group": "A+", "is_badhon_member": True},
    {"name": "সিয়াম সরকার", "phone": "01609828305", "department": "BGE", "session_val": "2025-26", "blood_group": "AB+", "is_badhon_member": True},
    {"name": "মেহেরাব হোসেন লাবন্য", "phone": "01753144640", "department": "BGE", "session_val": "2025-26", "blood_group": "O+", "is_badhon_member": False},
    {"name": "আন্দালিব কায়সার", "phone": "01916658366", "department": "BGE", "session_val": "2025-26", "blood_group": "B+", "is_badhon_member": True},
    {"name": "রাহিম আহসান", "phone": "01322139199", "department": "BGE", "session_val": "2025-26", "blood_group": "A+", "is_badhon_member": True},

    # FMB (5)
    {"name": "হাবিবা ফারজানা", "phone": "01821598671", "department": "FMB", "session_val": "2025-26", "blood_group": "AB+", "is_badhon_member": True},
    {"name": "রাবেয়া খাতুন", "phone": "01756246294", "department": "FMB", "session_val": "2025-26", "blood_group": "B-", "is_badhon_member": True},
    {"name": "রাবেয়া সুলতানা", "phone": "01749633339", "department": "FMB", "session_val": "2025-26", "blood_group": "B+", "is_badhon_member": True},
    {"name": "ফাহমিদা", "phone": "01778555141", "department": "FMB", "session_val": "2025-26", "blood_group": "O+", "is_badhon_member": False},
    {"name": "তাজবীন", "phone": "01316650520", "department": "FMB", "session_val": "2025-26", "blood_group": "B+", "is_badhon_member": False},

    # CSE (10)
    {"name": "অন্তরা", "phone": "01814603976", "department": "CSE", "session_val": "2025-26", "blood_group": "AB-", "is_badhon_member": False},
    {"name": "রূহান", "phone": "01832175049", "department": "CSE", "session_val": "2025-26", "blood_group": "B+", "is_badhon_member": False},
    {"name": "দীপ বিশ্বাস", "phone": "01340001126", "department": "CSE", "session_val": "2025-26", "blood_group": "A+", "is_badhon_member": True},
    {"name": "তন্নী", "phone": "01880296018", "department": "CSE", "session_val": "2025-26", "blood_group": "B+", "is_badhon_member": False},
    {"name": "মেজবুল রায়", "phone": "01306789706", "department": "CSE", "session_val": "2025-26", "blood_group": "O+", "is_badhon_member": False},
    {"name": "ইন্না আক্তার", "phone": "01879840343", "department": "CSE", "session_val": "2025-26", "blood_group": "O+", "is_badhon_member": False},
    {"name": "ফারজানা মেহজাবীন", "phone": "01614167202", "department": "CSE", "session_val": "2025-26", "blood_group": "O+", "is_badhon_member": False},
    {"name": "শাকির মাহমুদ", "phone": "01970012039", "department": "CSE", "session_val": "2025-26", "blood_group": "A+", "is_badhon_member": False},
    {"name": "রাকিব হাসান", "phone": "01738290328", "department": "CSE", "session_val": "2025-26", "blood_group": "O+", "is_badhon_member": False},
    {"name": "জয়", "phone": "01570209978", "department": "CSE", "session_val": "2025-26", "blood_group": "O+", "is_badhon_member": False},

    # ACCE (3)
    {"name": "মো: ইমন", "phone": "01773375236", "department": "ACCE", "session_val": "2025-26", "blood_group": "O+", "is_badhon_member": False},
    {"name": "ফয়সাল", "phone": "01315017235", "department": "ACCE", "session_val": "2025-26", "blood_group": "B+", "is_badhon_member": True},
    {"name": "ইব্রাহিম", "phone": "01860730255", "department": "ACCE", "session_val": "2025-26", "blood_group": "O+", "is_badhon_member": False},

    # Psychology (5)
    {"name": "মো: সুজন (রাশেদ)", "phone": "01992068493", "department": "Psychology", "session_val": "2025-26", "blood_group": "AB+", "is_badhon_member": False},
    {"name": "আইরিন আক্তার অনন্যা", "phone": "01577296401", "department": "Psychology", "session_val": "2025-26", "blood_group": "A+", "is_badhon_member": False},
    {"name": "অনন্যা দে সরকার", "phone": "01772987891", "department": "Psychology", "session_val": "2025-26", "blood_group": "B+", "is_badhon_member": False},
    {"name": "তানিয়া", "phone": "01710961337", "department": "Psychology", "session_val": "2025-26", "blood_group": "AB+", "is_badhon_member": False},
    {"name": "জোবাইরিয়া", "phone": "01907023443", "department": "Psychology", "session_val": "2025-26", "blood_group": "O+", "is_badhon_member": False}
]

def run_import():
    database.init_db()
    inserted_count = 0
    
    for donor in willing_donors:
        # Check if phone already exists to prevent duplicate insertion
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

    print(f"\nSuccessfully imported {inserted_count} blood donors into database!")

if __name__ == '__main__':
    run_import()
