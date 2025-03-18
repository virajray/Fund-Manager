import sqlite3

DATABASE = 'university_fund.db'

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row  # Access columns by name
    return db

def init_db():
    db = get_db()
    with open('schema.sql', 'r') as f:
        db.executescript(f.read())
    db.commit()
    db.close()

# --- Student Functions ---
def get_student_by_index(index_number):
    db = get_db()
    cur = db.execute('SELECT * FROM Students WHERE index_number = ?', (index_number,))
    student = cur.fetchone()
    db.close()
    return student

def get_student_payments(student_id):
    db = get_db()
    cur = db.execute('SELECT * FROM Payments WHERE student_id = ? ORDER BY month', (student_id,))
    payments = cur.fetchall()
    db.close()
    return payments

def get_all_students():
    db = get_db()
    cur = db.execute('SELECT * FROM Students')
    students = cur.fetchall()
    db.close()
    return students
# --- Payment Functions ---
def add_payment(student_id, month, amount_paid, payment_date):
    db = get_db()
    db.execute('INSERT INTO Payments (student_id, month, amount_paid, payment_date) VALUES (?, ?, ?, ?)',
               (student_id, month, amount_paid, payment_date))
    db.commit()
    db.close()

def get_admin(username):
    db = get_db()
    cur = db.execute('SELECT * FROM Admins WHERE username = ?', (username,))
    admin = cur.fetchone()
    db.close()
    return admin
# Example usage (you'd call init_db() once to create the tables)
# init_db()