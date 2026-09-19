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
    conn.commit()
    conn.close()

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

    conn.close()

    return {
        'total_donors': total_donors,
        'available_donors_count': available_donors_count,
        'badhon_members_count': badhon_members_count,
        'total_donations_sum': total_donations_sum,
        'departments': departments,
        'sessions': sessions,
        'group_counts': group_counts
    }
