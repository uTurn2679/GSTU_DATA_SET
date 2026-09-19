import unittest
import os
import database
from app import app

class BloodDonorTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
        # Use test database
        database.DB_NAME = 'test_blood_donors.db'
        if os.path.exists('test_blood_donors.db'):
            os.remove('test_blood_donors.db')
        database.init_db()

        database.add_donor(
            name="Test Donor Badhon",
            department="CSE",
            session_val="2020-21",
            blood_group="A+",
            phone="01700000001",
            last_donation_date="2026-01-01",
            total_donations=3,
            is_badhon_member=True,
            is_available=True
        )
        database.add_donor(
            name="Test Donor Regular",
            department="EEE",
            session_val="2021-22",
            blood_group="O-",
            phone="01700000002",
            last_donation_date=None,
            total_donations=0,
            is_badhon_member=False,
            is_available=False
        )

    def tearDown(self):
        if os.path.exists('test_blood_donors.db'):
            os.remove('test_blood_donors.db')

    def test_dashboard_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'GSTU Blood Donor Directory', response.data)
        self.assertIn(b'Test Donor Badhon', response.data)

    def test_filter_badhon_member(self):
        response = self.app.get('/?badhon=yes')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Donor Badhon', response.data)
        self.assertNotIn(b'Test Donor Regular', response.data)

    def test_register_donor(self):
        response = self.app.post('/donor/register', data={
            'name': 'New Student',
            'department': 'BBA',
            'session': '2022-23',
            'blood_group': 'B+',
            'phone': '01911111111',
            'last_donation_date': '2026-06-15',
            'total_donations': '2',
            'is_badhon_member': '1',
            'is_available': '1'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'New Student', response.data)

    def test_null_donation_fields(self):
        response = self.app.post('/donor/register', data={
            'name': 'Null Field Donor',
            'department': 'Physics',
            'session': '2023-24',
            'blood_group': 'AB-',
            'phone': '01500000000',
            'last_donation_date': '',
            'total_donations': '',
            'is_badhon_member': '',
            'is_available': '1'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Null Field Donor', response.data)
        self.assertIn(b'N/A', response.data)

    def test_csv_export(self):
        response = self.app.get('/export/csv')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'text/csv')
        self.assertIn(b'Test Donor Badhon', response.data)

if __name__ == '__main__':
    unittest.main()
