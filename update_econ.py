import sqlite3

conn = sqlite3.connect('blood_donors.db')
cursor = conn.cursor()
cursor.execute("UPDATE donors SET department = 'ECO' WHERE department = 'Econ'")
count = cursor.rowcount
conn.commit()
conn.close()

print(f"Successfully updated {count} donor records: Department 'Econ' changed to 'ECO'.")
