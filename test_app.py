import unittest
import os
import database
from app import app

class BloodDonorTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'test-secret'
        self.app = app.test_client()
        database.DB_NAME = 'test_blood_donors.db'
        if os.path.exists('test_blood_donors.db'):
            os.remove('test_blood_donors.db')
        database.init_db()

        self.donor_id = database.add_donor(
            name="Test Donor Badhon",
            department="CSE",
            session_val="2020-21",
            blood_group="A+",
            phone="01700000001",
            last_donation_date="2026-01-01",
            total_donations=1,
            is_badhon_member=True,
            is_available=True
        )

    def tearDown(self):
        if os.path.exists('test_blood_donors.db'):
            os.remove('test_blood_donors.db')

    def test_unauthenticated_user_redirect(self):
        # Unauthenticated user visiting root should be redirected to /login
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Admin System Portal', response.data)
        self.assertIn(b'Please log in as Admin or Sub-Admin', response.data)

    def test_admin_habib_login_and_subadmin_creation(self):
        # Login as Super Admin HABIB2679
        login_resp = self.app.post('/login', data={
            'username': 'HABIB2679',
            'password': '233134'
        }, follow_redirects=True)
        self.assertEqual(login_resp.status_code, 200)
        self.assertIn(b'GSTU Donor Management Dashboard', login_resp.data)
        self.assertIn(b'Super Admin', login_resp.data)

        # Create Sub-Admin
        sub_resp = self.app.post('/admin/subadmin/create', data={
            'full_name': 'Sub Admin Shakil',
            'username': 'shakil_subadmin',
            'password': 'subpassword123'
        }, follow_redirects=True)
        self.assertEqual(sub_resp.status_code, 200)
        self.assertIn(b'created successfully!', sub_resp.data)

        # Verify created sub-admin can log in
        self.app.get('/logout')
        sub_login = self.app.post('/login', data={
            'username': 'shakil_subadmin',
            'password': 'subpassword123'
        }, follow_redirects=True)
        self.assertEqual(sub_login.status_code, 200)
        self.assertIn(b'Sub-Admin', sub_login.data)
        self.assertIn(b'Test Donor Badhon', sub_login.data)

    def test_donor_10_donation_history_cap(self):
        # Login as Admin
        self.app.post('/login', data={'username': 'HABIB2679', 'password': '233134'})

        # Add 12 donation dates to donor
        for i in range(1, 13):
            date_str = f"2025-01-{i:02d}"
            database.add_donation_history(self.donor_id, date_str)

        # Check recorded history count is capped at 10
        history = database.get_donation_history(self.donor_id)
        self.assertEqual(len(history), 10)

    def test_subadmin_cannot_create_subadmin(self):
        # Create Sub-Admin via database helper
        database.create_user('sub_user', 'pass123', 'subadmin', 'Sub User')

        # Login as Sub-Admin
        self.app.post('/login', data={'username': 'sub_user', 'password': 'pass123'})

        # Attempt to create another Sub-Admin
        resp = self.app.post('/admin/subadmin/create', data={
            'full_name': 'Attempt Sub',
            'username': 'attempt_sub',
            'password': 'password'
        }, follow_redirects=True)

        self.assertIn(b'Access denied', resp.data)

if __name__ == '__main__':
    unittest.main()
