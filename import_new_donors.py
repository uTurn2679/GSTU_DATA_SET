import database

raw_data = """
Mohini 	1349646447	FNB	25-26	B+	YES
Tonni Khatun	1999589346	FNB	25-26	B+	YES
Kanij Fatema	1301704816	FNB	25-26	O+	YES
Mim Akter	1746840877	FNB	25-26	A+	NO
Yeasin Tanvir	1851616802	FNB	25-26	O+	YES
Shuvo	1826627248	FNB	25-26	AB+	NO
Mamun	1904463544	FNB	25-26	AB+	NO
safin	1779522001	FNB	25-26	O+	NO
sorif	1308837603	FNB	25-26	A+	NO
moin	1340789592	FNB	25-27	O+	NO
MD. HASHOR ALI	1321743428	Agriculture	25-26	O+	YES
Janif Ahmed	1953773729	Agriculture	25-26	B+	YES
Munna	1786941804	Agriculture	25-26	O+	NO
Rakim	1941907049	Agriculture	25-26	O+	NO
MD. TANVIR	1907698400	Agriculture	25-26	B+	NO
ASHIKUR	1727479396	Agriculture	25-26	B+	NO
FAHAT	1829597776	Agriculture	25-26	AB+	YES
RAJIBUL	1777170451	Agriculture	25-26	A+	NO
Prity	1886271980	Agriculture	25-26	A+	YES
Adiba	1813036240	Agriculture	25-26	B+	YES
Afsana	1400653235	Agriculture	25-26	O+	YES
Nishi	1603317679	Agriculture	25-26	B+	YES
AB Motin	1706227818	Agriculture	25-26	B+	NO
Nishat	1778500826	Agriculture	25-26	A+	NO
"""

def import_donors():
    database.init_db()
    lines = [line.strip() for line in raw_data.strip().split('\n') if line.strip()]
    count = 0
    
    for line in lines:
        parts = [p.strip() for p in line.split('\t') if p.strip()]
        if len(parts) < 6:
            # Fallback if tab split is irregular
            parts = [p.strip() for p in line.split() if p.strip()]
        
        # Parse fields from parts
        # Format: Name, Mobile, Dept, Session, BloodGroup, Badhon
        # Note: Name may contain spaces (e.g. "Tonni Khatun")
        # Let's inspect line by tab splitting first
        tab_parts = line.split('\t')
        cleaned_parts = [p.strip() for p in tab_parts if p.strip()]
        
        if len(cleaned_parts) == 6:
            name, phone, dept, sess, bg, badhon = cleaned_parts
        else:
            print(f"Skipping line due to unexpected format: {line}")
            continue

        # Format Phone number with leading '0' if missing
        if len(phone) == 10 and not phone.startswith('0'):
            phone = '0' + phone

        # Format session if needed
        if sess == '25-26':
            sess_formatted = '2025-26'
        elif sess == '25-27':
            sess_formatted = '2025-27'
        else:
            sess_formatted = sess

        is_badhon = True if badhon.upper() == 'YES' else False

        database.add_donor(
            name=name,
            department=dept,
            session_val=sess_formatted,
            blood_group=bg,
            phone=phone,
            last_donation_date=None,
            total_donations=0,
            is_badhon_member=is_badhon,
            is_available=True
        )
        count += 1
        print(f"Imported: {name} ({bg}, {dept}, {sess_formatted}, {phone})")

    print(f"\nSuccessfully imported {count} new donors into database!")

if __name__ == '__main__':
    import_donors()
