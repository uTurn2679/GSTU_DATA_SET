import sqlite3
import os
from datetime import datetime, date

DB_NAME = 'blood_donors.db'

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    
    # Donors Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS donors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            session TEXT NOT NULL,
            blood_group TEXT NOT NULL,
            phone TEXT NOT NULL,
            last_donation_date TEXT,
            total_donations INTEGER DEFAULT 0,
            is_badhon_member INTEGER DEFAULT 0,
            is_available INTEGER DEFAULT 1,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
    ''')

    # Donation History Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS donation_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            donor_id INTEGER NOT NULL,
            donation_date TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(donor_id) REFERENCES donors(id) ON DELETE CASCADE
        );
    ''')

    # Users Table (Admin, Sub-Admin, Member)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            full_name TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
    ''')

    # Blood Requests Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS blood_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT NOT NULL,
            blood_group TEXT NOT NULL,
            hospital_location TEXT NOT NULL,
            contact_phone TEXT NOT NULL,
            date_needed TEXT NOT NULL,
            units_needed INTEGER DEFAULT 1,
            status TEXT DEFAULT 'Pending',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
    ''')

    conn.commit()

    # Seed Default Super Admin and Member accounts if not present
    cursor.execute("SELECT COUNT(*) as count FROM users WHERE username = ?", ('HABIB2679',))
    if cursor.fetchone()['count'] == 0:
        cursor.execute('''
            INSERT INTO users (username, password, role, full_name)
            VALUES (?, ?, ?, ?)
        ''', ('HABIB2679', '233134', 'admin', 'Super Admin Habib'))

    cursor.execute("SELECT COUNT(*) as count FROM users WHERE username = ?", ('member',))
    if cursor.fetchone()['count'] == 0:
        cursor.execute('''
            INSERT INTO users (username, password, role, full_name)
            VALUES (?, ?, ?, ?)
        ''', ('member', 'member123', 'member', 'General Member'))

    conn.commit()
    conn.close()

# User Authentication & Management Functions
def get_user_by_username(username):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user

def verify_user(username, password):
    user = get_user_by_username(username)
    if user and user['password'] == password:
        return user
    return None

def create_user(username, password, role, full_name):
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO users (username, password, role, full_name)
            VALUES (?, ?, ?, ?)
        ''', (username, password, role, full_name))
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return user_id
    except sqlite3.IntegrityError:
        conn.close()
        return None

def get_subadmins():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE role = 'subadmin' ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows

def delete_user(user_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()

# Blood Requests Functions
def add_blood_request(patient_name, blood_group, hospital_location, contact_phone, date_needed, units_needed=1):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO blood_requests (patient_name, blood_group, hospital_location, contact_phone, date_needed, units_needed, status)
        VALUES (?, ?, ?, ?, ?, ?, 'Pending')
    ''', (patient_name, blood_group, hospital_location, contact_phone, date_needed, units_needed))
    conn.commit()
    req_id = cursor.lastrowid
    conn.close()
    return req_id

def get_blood_requests(status=None):
    conn = get_db()
    cursor = conn.cursor()
    if status:
        cursor.execute("SELECT * FROM blood_requests WHERE status = ? ORDER BY id DESC", (status,))
    else:
        cursor.execute("SELECT * FROM blood_requests ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_request_status(request_id, new_status):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE blood_requests SET status = ? WHERE id = ?", (new_status, request_id))
    conn.commit()
    conn.close()

# Donor Management Functions
def get_donors(search=None, blood_group=None, department=None, session_val=None, badhon=None, availability=None):
    conn = get_db()
    cursor = conn.cursor()

    sql = "SELECT * FROM donors WHERE 1=1"
    params = []

    if search:
        sql += " AND (name LIKE ? OR department LIKE ? OR session LIKE ? OR phone LIKE ?)"
        pattern = f"%{search}%"
        params.extend([pattern, pattern, pattern, pattern])

    if blood_group:
        sql += " AND blood_group = ?"
        params.append(blood_group)

    if department:
        sql += " AND department = ?"
        params.append(department)

    if session_val:
        sql += " AND session = ?"
        params.append(session_val)

    if badhon == 'yes':
        sql += " AND is_badhon_member = 1"
    elif badhon == 'no':
        sql += " AND is_badhon_member = 0"

    if availability == 'available':
        sql += " AND is_available = 1"
    elif availability == 'unavailable':
        sql += " AND is_available = 0"

    sql += " ORDER BY name ASC"

    cursor.execute(sql, params)
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_donor(donor_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM donors WHERE id = ?", (donor_id,))
    donor = cursor.fetchone()
    conn.close()
    return donor

def add_donor(name, department, session_val, blood_group, phone, last_donation_date, total_donations, is_badhon_member, is_available):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO donors (name, department, session, blood_group, phone, last_donation_date, total_donations, is_badhon_member, is_available)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        name, department, session_val, blood_group, phone,
        last_donation_date, total_donations,
        1 if is_badhon_member else 0,
        1 if is_available else 0
    ))
    conn.commit()
    donor_id = cursor.lastrowid

    if last_donation_date:
        cursor.execute('''
            INSERT INTO donation_history (donor_id, donation_date)
            VALUES (?, ?)
        ''', (donor_id, last_donation_date))
        conn.commit()

    conn.close()
    return donor_id

def update_donor(donor_id, name, department, session_val, blood_group, phone, last_donation_date, total_donations, is_badhon_member, is_available):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE donors
        SET name = ?, department = ?, session = ?, blood_group = ?, phone = ?,
            last_donation_date = ?, total_donations = ?, is_badhon_member = ?, is_available = ?
        WHERE id = ?
    ''', (
        name, department, session_val, blood_group, phone,
        last_donation_date, total_donations,
        1 if is_badhon_member else 0,
        1 if is_available else 0,
        donor_id
    ))
    conn.commit()
    conn.close()

def get_donation_history(donor_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM donation_history
        WHERE donor_id = ?
        ORDER BY donation_date DESC, id DESC
        LIMIT 10
    ''', (donor_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def add_donation_history(donor_id, donation_date):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO donation_history (donor_id, donation_date)
        VALUES (?, ?)
    ''', (donor_id, donation_date))
    conn.commit()

    # Enforce max 10 dates per donor (delete older entries)
    cursor.execute('''
        DELETE FROM donation_history
        WHERE id NOT IN (
            SELECT id FROM donation_history
            WHERE donor_id = ?
            ORDER BY donation_date DESC, id DESC
            LIMIT 10
        ) AND donor_id = ?
    ''', (donor_id, donor_id))
    conn.commit()

    _sync_donor_donation_stats(cursor, donor_id)
    conn.commit()
    conn.close()

def delete_donation_history(history_id, donor_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM donation_history WHERE id = ? AND donor_id = ?", (history_id, donor_id))
    conn.commit()

    _sync_donor_donation_stats(cursor, donor_id)
    conn.commit()
    conn.close()

def _sync_donor_donation_stats(cursor, donor_id):
    cursor.execute('''
        SELECT MAX(donation_date) as max_date, COUNT(*) as history_count
        FROM donation_history
        WHERE donor_id = ?
    ''', (donor_id,))
    res = cursor.fetchone()
    if res and res['history_count'] > 0:
        max_date = res['max_date']
        count = res['history_count']
        cursor.execute('''
            UPDATE donors
            SET last_donation_date = ?,
                total_donations = CASE WHEN total_donations < ? THEN ? ELSE total_donations END
            WHERE id = ?
        ''', (max_date, count, count, donor_id))

def toggle_availability(donor_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE donors SET is_available = CASE WHEN is_available = 1 THEN 0 ELSE 1 END WHERE id = ?", (donor_id,))
    conn.commit()
    cursor.execute("SELECT is_available, name FROM donors WHERE id = ?", (donor_id,))
    row = cursor.fetchone()
    conn.close()
    return row

def delete_donor(donor_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM donors WHERE id = ?", (donor_id,))
    row = cursor.fetchone()
    name = row['name'] if row else "Donor"
    cursor.execute("DELETE FROM donation_history WHERE donor_id = ?", (donor_id,))
    cursor.execute("DELETE FROM donors WHERE id = ?", (donor_id,))
    conn.commit()
    conn.close()
    return name

def get_stats():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) as total FROM donors")
    total_donors = cursor.fetchone()['total']

    cursor.execute("SELECT COUNT(*) as avail FROM donors WHERE is_available = 1")
    available_donors_count = cursor.fetchone()['avail']

    cursor.execute("SELECT COUNT(*) as badhon FROM donors WHERE is_badhon_member = 1")
    badhon_members_count = cursor.fetchone()['badhon']

    cursor.execute("SELECT SUM(total_donations) as sum_donations FROM donors")
    row_sum = cursor.fetchone()
    total_donations_sum = row_sum['sum_donations'] if row_sum['sum_donations'] else 0

    cursor.execute("SELECT DISTINCT department FROM donors WHERE department IS NOT NULL AND department != '' ORDER BY department ASC")
    departments = [r['department'] for r in cursor.fetchall()]

    cursor.execute("SELECT DISTINCT session FROM donors WHERE session IS NOT NULL AND session != '' ORDER BY session ASC")
    sessions = [r['session'] for r in cursor.fetchall()]

    cursor.execute("SELECT blood_group, COUNT(*) as count FROM donors GROUP BY blood_group")
    group_counts = {r['blood_group']: r['count'] for r in cursor.fetchall()}

    cursor.execute("SELECT COUNT(*) as pending FROM blood_requests WHERE status = 'Pending'")
    pending_requests_count = cursor.fetchone()['pending']

    conn.close()

    return {
        'total_donors': total_donors,
        'available_donors_count': available_donors_count,
        'badhon_members_count': badhon_members_count,
        'total_donations_sum': total_donations_sum,
        'departments': departments,
        'sessions': sessions,
        'group_counts': group_counts,
        'pending_requests_count': pending_requests_count
    }
