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

    def test_guest_restricted_access(self):
        # Guest visiting main page should see restricted hero banner
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Donor Directory Access Protected', response.data)
        # Guest should not see donor phone number
        self.assertNotIn(b'01700000001', response.data)

    def test_public_blood_request(self):
        response = self.app.post('/request-blood', data={
            'patient_name': 'Patient Salim',
            'blood_group': 'O+',
            'hospital_location': 'Patuakhali Medical',
            'contact_phone': '01899999999',
            'date_needed': '2026-10-01',
            'units_needed': '2'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Emergency Blood Request submitted', response.data)

        # Verify request exists in DB
        reqs = database.get_blood_requests()
        self.assertEqual(len(reqs), 1)
        self.assertEqual(reqs[0]['patient_name'], 'Patient Salim')

    def test_member_login_and_view_only(self):
        # Login as member
        login_resp = self.app.post('/login', data={
            'username': 'member',
            'password': 'member123'
        }, follow_redirects=True)
        self.assertEqual(login_resp.status_code, 200)
        self.assertIn(b'Donor Directory', login_resp.data)
        self.assertIn(b'Test Donor Badhon', login_resp.data)

        # Member should NOT be able to access register or edit
        reg_resp = self.app.get('/donor/register', follow_redirects=True)
        self.assertIn(b'Access denied', reg_resp.data)

    def test_admin_habib_login_and_subadmin_creation(self):
        # Login as Super Admin HABIB2679
        login_resp = self.app.post('/login', data={
            'username': 'HABIB2679',
            'password': '233134'
        }, follow_redirects=True)
        self.assertEqual(login_resp.status_code, 200)

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
        self.assertIn(b'shakil_subadmin', sub_login.data)

if __name__ == '__main__':
    unittest.main()
