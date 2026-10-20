import sqlite3

def clear_donors():
    conn = sqlite3.connect('blood_donors.db')
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM donation_history")
    cursor.execute("DELETE FROM donors")
    try:
        cursor.execute("DELETE FROM sqlite_sequence WHERE name IN ('donors', 'donation_history')")
    except sqlite3.OperationalError:
        pass
        
    conn.commit()
    
    cursor.execute("SELECT COUNT(*) FROM donors")
    donor_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM donation_history")
    history_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]
    
    conn.close()
    print(f"Cleared all donor info successfully.")
    print(f"Donors count: {donor_count}")
    print(f"Donation history count: {history_count}")
    print(f"Admin / Sub-admin users retained: {user_count}")

if __name__ == '__main__':
    clear_donors()
