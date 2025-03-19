from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import database
import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this in a real application!

# --- Student Routes ---

@app.route('/', methods=['GET', 'POST'])
def student_login():
    if request.method == 'POST':
        index_number = request.form['index_number']
        password = request.form['password']  # Get password from the form
        student = database.get_student_by_index(index_number)
        if student and student['password'] == password: #Basic password check
            session['student_id'] = student['student_id'] #Store student_id in the session
            return redirect(url_for('student_dashboard'))
        else:
            return render_template('index.html', error='Invalid credentials')
    return render_template('index.html')

@app.route('/student/dashboard')
def student_dashboard():
    if 'student_id' not in session:
        return redirect(url_for('student_login'))

    student_id = session['student_id']
    student = database.get_db().execute('SELECT * FROM Students WHERE student_id = ?', (student_id,)).fetchone()
    payments = database.get_student_payments(student_id)

    # Calculate total due and paid
    total_due = calculate_total_due(student_id)  # Implement this function
    total_paid = sum([p['amount_paid'] for p in payments])

    return render_template('student_dashboard.html', student=student, payments=payments, total_due=total_due, total_paid=total_paid)

def calculate_total_due(student_id):
    # Assuming a fixed monthly fee of 1000 (you can customize this)
    monthly_fee = 100
    current_year = datetime.datetime.now().year
    current_month = datetime.datetime.now().month
    # You might want to store the start date of the batch to be more accurate
    start_year = 2025  # Example start year
    start_month = 1   # Example start month

    total_months = (current_year - start_year) * 12 + (current_month - start_month) + 1
    total_due = total_months * monthly_fee
    return total_due


# --- Admin Routes ---
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        admin = database.get_admin(username)

        if admin and admin['password'] == password:  # Very basic password check
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
             return render_template('admin_login.html', error='Invalid credentials')

    return render_template('admin_login.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

    students = database.get_all_students()
    return render_template('admin.html', students=students)


@app.route('/admin/add_payment', methods=['POST'])
def add_payment_route():
    if not session.get('admin_logged_in'):
        return jsonify({'message': 'Unauthorized'}), 401

    data = request.get_json()
    student_id = data['student_id']
    month = data['month']
    amount_paid = data['amount_paid']
    payment_date = datetime.date.today().isoformat()  # Current date

    try:
        database.add_payment(student_id, month, amount_paid, payment_date)
        return jsonify({'message': 'Payment added successfully'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@app.route('/logout')
def logout():
    session.clear()  # Clear all session data
    return redirect(url_for('student_login')) # Redirect to the student login page


if __name__ == '__main__':
    app.run(debug=True)