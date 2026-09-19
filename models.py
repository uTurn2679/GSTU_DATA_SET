from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()

class Donor(db.Model):
    __tablename__ = 'donors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    session = db.Column(db.String(50), nullable=False)
    blood_group = db.Column(db.String(5), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    last_donation_date = db.Column(db.Date, nullable=True)
    total_donations = db.Column(db.Integer, default=0, nullable=False)
    is_badhon_member = db.Column(db.Boolean, default=False, nullable=False)
    is_available = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'department': self.department,
            'session': self.session,
            'blood_group': self.blood_group,
            'phone': self.phone,
            'last_donation_date': self.last_donation_date.strftime('%Y-%m-%d') if self.last_donation_date else 'N/A',
            'total_donations': self.total_donations,
            'is_badhon_member': 'Yes' if self.is_badhon_member else 'No',
            'is_available': 'Available' if self.is_available else 'Not Available',
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

    def __repr__(self):
        return f'<Donor {self.name} ({self.blood_group})>'
