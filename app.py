import io
import csv
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, Response
import database

app = Flask(__name__)
app.config['SECRET_KEY'] = 'gstu-blood-donor-secret-key-2026'

database.init_db()

BLOOD_GROUPS = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']

@app.route('/')
def index():
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

    stats = database.get_stats()

    group_stats = {bg: stats['group_counts'].get(bg, 0) for bg in BLOOD_GROUPS}

    return render_template(
        'index.html',
        donors=donors,
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

@app.route('/donor/register', methods=['GET', 'POST'])
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
        return redirect(url_for('index'))

    return render_template('edit.html', donor=donor, blood_groups=BLOOD_GROUPS)

@app.route('/donor/<int:id>/toggle-status', methods=['POST'])
def toggle_status(id):
    res = database.toggle_availability(id)
    if res:
        status_str = "Available" if res['is_available'] == 1 else "Unavailable"
        flash(f"Status for {res['name']} changed to {status_str}.", 'info')
    return redirect(url_for('index'))

@app.route('/donor/<int:id>/delete', methods=['POST'])
def delete_donor(id):
    name = database.delete_donor(id)
    flash(f'Donor "{name}" was removed from the database.', 'warning')
    return redirect(url_for('index'))

@app.route('/export/csv')
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
