from datetime import datetime
from flask_login import UserMixin
from app import db, login_manager

# Funcția care încarcă un utilizator după ID (pentru sesiuni Flask-Login)
@login_manager.user_loader
def load_user(user_id):
    # Caută utilizatorul în baza de date după ID
    return User.query.get(int(user_id))

# Modelul User – reprezintă un utilizator (doctor sau admin)
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Cheia primară
    username = db.Column(db.String(64), unique=True, nullable=False)  # Nume unic
    email = db.Column(db.String(120), unique=True, nullable=False)    # Email unic
    password_hash = db.Column(db.String(256), nullable=False)         # Parola (criptată)
    role = db.Column(db.String(20), nullable=False, default='doctor') # Rolul: doctor sau admin
    created_at = db.Column(db.DateTime, default=datetime.utcnow)      # Data creării contului
    implants = db.relationship('Implant', backref='doctor', lazy=True)  # Legătură cu implanturile

    # Metodă pentru a verifica dacă userul este admin
    def is_admin(self):
        return self.role == 'admin'

    # Metodă pentru a verifica dacă userul este doctor
    def is_doctor(self):
        return self.role == 'doctor'

# Modelul ImplantType – reprezintă un tip de implant
class ImplantType(db.Model):
    id = db.Column(db.Integer, primary_key=True)                        # Cheia primară
    name = db.Column(db.String(100), nullable=False, unique=True)      # Nume unic
    implants = db.relationship('Implant', backref='implant_type', lazy=True)  # Implanturile de acest tip

    # Reprezentare text (folosită la debug sau în shell)
    def __repr__(self):
        return f'<ImplantType {self.name}>'

# Modelul Implant – reprezintă un implant medical înregistrat
class Implant(db.Model):
    id = db.Column(db.Integer, primary_key=True)                       # Cheia primară
    implant_id = db.Column(db.String(50), unique=True, nullable=False) # ID unic, ex: IMP-1234
    type_id = db.Column(db.Integer, db.ForeignKey('implant_type.id'), nullable=False)  # Legătură cu ImplantType
    patient_name = db.Column(db.String(100), nullable=False)          # Numele pacientului
    doctor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Legătură cu doctorul
    implant_date = db.Column(db.Date, nullable=False)                 # Data implantului
    status = db.Column(db.String(20), nullable=False, default='Active')  # Statusul implantului
    notes = db.Column(db.Text, nullable=True)                         # Notițe opționale
    created_at = db.Column(db.DateTime, default=datetime.utcnow)      # Data creării
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Data ultimei modificări

    # Reprezentare text (pentru debug, shell etc.)
    def __repr__(self):
        return f'<Implant {self.implant_id}>'

    # Convertirea implantului într-un dicționar – util pentru API (JSON)
    def to_dict(self):
        """Convert implant to dictionary for API responses"""
        return {
            'id': self.id,
            'implant_id': self.implant_id,
            'implant_type': self.implant_type.name,  # Numele tipului de implant
            'patient_name': self.patient_name,
            'doctor': self.doctor.username,          # Numele doctorului
            'implant_date': self.implant_date.strftime('%Y-%m-%d'),  # Formatat ca string
            'status': self.status,
            'notes': self.notes,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }
