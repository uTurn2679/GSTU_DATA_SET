import sqlite3

conn = sqlite3.connect('blood_donors.db')
cursor = conn.cursor()
cursor.execute("UPDATE donors SET department = 'ACCE' WHERE department = 'ACCF'")
count = cursor.rowcount
conn.commit()
conn.close()

print(f"Successfully updated {count} donor records: Department 'ACCF' changed to 'ACCE'.")
