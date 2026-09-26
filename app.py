import io
import csv
from datetime import datetime
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, flash, Response, session
import database

app = Flask(__name__)
app.config['SECRET_KEY'] = 'gstu-blood-donor-secret-key-2026'

database.init_db()

BLOOD_GROUPS = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']

# Session User Context Processor
@app.context_processor
def inject_user():
    return dict(current_user=session.get('user'))

# Role-based access decorators
def role_required(allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = session.get('user')
            if not user:
                flash('Please log in as Admin or Sub-Admin to access the portal.', 'warning')
                return redirect(url_for('login'))
            if user.get('role') not in allowed_roles:
                flash('Access denied. You do not have permission for this action.', 'error')
                return redirect(url_for('index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@app.route('/')
@role_required(['admin', 'subadmin'])
def index():
    user = session.get('user')
    
    search_query = request.args.get('search', '').strip()
    blood_group = request.args.get('blood_group', '').strip()
    department = request.args.get('department', '').strip()
    session_filter = request.args.get('session', '').strip()
    badhon_filter = request.args.get('badhon', '').strip()
    availability_filter = request.args.get('availability', '').strip()

    donors = database.get_donors(
        search=search_query,
        blood_group=blood_group,
        department=department,
        session_val=session_filter,
        badhon=badhon_filter,
        availability=availability_filter
    )
    donor_histories = {d['id']: database.get_donation_history(d['id']) for d in donors}

    stats = database.get_stats()
    group_stats = {bg: stats['group_counts'].get(bg, 0) for bg in BLOOD_GROUPS}
    subadmins = database.get_subadmins() if user and user.get('role') == 'admin' else []

    return render_template(
        'index.html',
        donors=donors,
        donor_histories=donor_histories,
        subadmins=subadmins,
        total_donors=stats['total_donors'],
        available_donors_count=stats['available_donors_count'],
        badhon_members_count=stats['badhon_members_count'],
        total_donations_sum=stats['total_donations_sum'],
        blood_groups=BLOOD_GROUPS,
        departments=stats['departments'],
        sessions=stats['sessions'],
        group_stats=group_stats,
        search_query=search_query,
        selected_blood_group=blood_group,
        selected_department=department,
        selected_session=session_filter,
        selected_badhon=badhon_filter,
        selected_availability=availability_filter
    )

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        user = database.verify_user(username, password)
        if user and user['role'] in ['admin', 'subadmin']:
            session['user'] = {
                'id': user['id'],
                'username': user['username'],
                'role': user['role'],
                'full_name': user['full_name']
            }
            flash(f"Welcome back, {user['full_name']}!", 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password for Admin / Sub-Admin portal.', 'error')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Logged out successfully.', 'info')
    return redirect(url_for('login'))

@app.route('/admin/dashboard')
@role_required(['admin', 'subadmin'])
def admin_dashboard():
    return redirect(url_for('index'))

@app.route('/admin/subadmin/create', methods=['POST'])
@role_required(['admin'])  # Only Super Admin HABIB2679 can create Sub-Admins
def create_subadmin():
    full_name = request.form.get('full_name', '').strip()
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '').strip()

    if not full_name or not username or not password:
        flash('Please fill in all Sub-Admin fields.', 'error')
        return redirect(url_for('index'))

    res = database.create_user(username=username, password=password, role='subadmin', full_name=full_name)
    if res:
        flash(f'Sub-Admin account "{username}" created successfully!', 'success')
    else:
        flash(f'Username "{username}" is already taken.', 'error')

    return redirect(url_for('index'))

@app.route('/admin/user/<int:id>/delete', methods=['POST'])
@role_required(['admin'])  # Only Super Admin HABIB2679 can delete users
def delete_user_route(id):
    database.delete_user(id)
    flash('Sub-Admin account removed.', 'warning')
    return redirect(url_for('index'))

@app.route('/donor/register', methods=['GET', 'POST'])
@role_required(['admin', 'subadmin'])
def register():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        department = request.form.get('department', '').strip()
        session_val = request.form.get('session', '').strip()
        blood_group = request.form.get('blood_group', '').strip()
        phone = request.form.get('phone', '').strip()
        last_donation_date = request.form.get('last_donation_date', '').strip()
        total_donations_str = request.form.get('total_donations', '0').strip()
        is_badhon_member = True if request.form.get('is_badhon_member') else False
        is_available = True if request.form.get('is_available') else False

        if not name or not department or not session_val or not blood_group or not phone:
            flash('Please fill in all required fields (Name, Department, Session, Blood Group, Phone).', 'error')
            return redirect(url_for('register'))

        if total_donations_str != '' and total_donations_str.isdigit():
            total_donations = int(total_donations_str)
        else:
            total_donations = None

        database.add_donor(
            name=name,
            department=department,
            session_val=session_val,
            blood_group=blood_group,
            phone=phone,
            last_donation_date=last_donation_date if last_donation_date else None,
            total_donations=total_donations,
            is_badhon_member=is_badhon_member,
            is_available=is_available
        )

        flash(f'Donor "{name}" successfully registered!', 'success')
        return redirect(url_for('index'))

    return render_template('register.html', blood_groups=BLOOD_GROUPS)

@app.route('/donor/<int:id>/edit', methods=['GET', 'POST'])
@role_required(['admin', 'subadmin'])
def edit_donor(id):
    donor = database.get_donor(id)
    if not donor:
        flash('Donor not found.', 'error')
        return redirect(url_for('index'))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        department = request.form.get('department', '').strip()
        session_val = request.form.get('session', '').strip()
        blood_group = request.form.get('blood_group', '').strip()
        phone = request.form.get('phone', '').strip()
        last_donation_date = request.form.get('last_donation_date', '').strip()
        total_donations_str = request.form.get('total_donations', '0').strip()
        is_badhon_member = True if request.form.get('is_badhon_member') else False
        is_available = True if request.form.get('is_available') else False

        if total_donations_str != '' and total_donations_str.isdigit():
            total_donations = int(total_donations_str)
        else:
            total_donations = None

        database.update_donor(
            donor_id=id,
            name=name,
            department=department,
            session_val=session_val,
            blood_group=blood_group,
            phone=phone,
            last_donation_date=last_donation_date if last_donation_date else None,
            total_donations=total_donations,
            is_badhon_member=is_badhon_member,
            is_available=is_available
        )

        flash(f'Donor "{name}" updated successfully!', 'success')
        return redirect(url_for('edit_donor', id=id))

    history = database.get_donation_history(id)
    return render_template('edit.html', donor=donor, history=history, blood_groups=BLOOD_GROUPS)

@app.route('/donor/<int:id>/history/add', methods=['POST'])
@role_required(['admin', 'subadmin'])
def add_history(id):
    donor = database.get_donor(id)
    if not donor:
        flash('Donor not found.', 'error')
        return redirect(url_for('index'))

    donation_date = request.form.get('donation_date', '').strip()
    if not donation_date:
        flash('Please select a valid donation date.', 'error')
        return redirect(url_for('edit_donor', id=id))

    database.add_donation_history(id, donation_date)
    flash(f'Donation date ({donation_date}) added to donor history!', 'success')
    return redirect(url_for('edit_donor', id=id))

@app.route('/donor/<int:id>/history/<int:history_id>/delete', methods=['POST'])
@role_required(['admin', 'subadmin'])
def delete_history(id, history_id):
    donor = database.get_donor(id)
    if not donor:
        flash('Donor not found.', 'error')
        return redirect(url_for('index'))

    database.delete_donation_history(history_id, id)
    flash('Donation date removed from history.', 'info')
    return redirect(url_for('edit_donor', id=id))

@app.route('/donor/<int:id>/toggle-status', methods=['POST'])
@role_required(['admin', 'subadmin'])
def toggle_status(id):
    res = database.toggle_availability(id)
    if res:
        status_str = "Available" if res['is_available'] == 1 else "Unavailable"
        flash(f"Status for {res['name']} changed to {status_str}.", 'info')
    return redirect(url_for('index'))

@app.route('/donor/<int:id>/delete', methods=['POST'])
@role_required(['admin', 'subadmin'])
def delete_donor(id):
    name = database.delete_donor(id)
    flash(f'Donor "{name}" was removed from the database.', 'warning')
    return redirect(url_for('index'))

@app.route('/export/csv')
@role_required(['admin', 'subadmin'])
def export_csv():
    donors = database.get_donors()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        'ID', 'Name', 'Department', 'Session', 'Blood Group',
        'Phone', 'Last Donation Date', 'Total Donations',
        'Member of Badhon', 'Availability Status', 'Created At'
    ])

    for d in donors:
        writer.writerow([
            d['id'],
            d['name'],
            d['department'],
            d['session'],
            d['blood_group'],
            d['phone'],
            d['last_donation_date'] if d['last_donation_date'] else 'N/A',
            d['total_donations'] if d['total_donations'] is not None else 'N/A',
            'Yes' if d['is_badhon_member'] == 1 else 'No',
            'Available' if d['is_available'] == 1 else 'Not Available',
            d['created_at']
        ])

    response = Response(output.getvalue(), mimetype='text/csv')
    response.headers['Content-Disposition'] = 'attachment; filename=gstu_blood_donors.csv'
    return response

if __name__ == '__main__':
    app.run(debug=True, port=5000)
