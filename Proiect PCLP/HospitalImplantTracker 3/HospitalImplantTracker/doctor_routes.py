# Importăm modulele necesare din Flask și aplicația noastră
from flask import Blueprint, render_template                  # Blueprint permite gruparea rutelor pe module, iar render_template redă fișiere HTML
from flask_login import login_required, current_user          # login_required asigură că doar utilizatorii autentificați pot accesa ruta
from app import db                                            # Importăm obiectul db pentru interacțiunea cu baza de date
from models import Implant, ImplantType                       # Importăm modelele Implant și ImplantType din models.py
from utils import doctor_required, get_doctor_statistics      # Importăm funcția care verifică dacă utilizatorul e doctor și funcția de obținere a statisticilor

# Definim un blueprint pentru rutele doctorului, cu prefixul /doctor
doctor_bp = Blueprint('doctor', __name__, url_prefix='/doctor')

# Ruta pentru dashboard-ul doctorului
@doctor_bp.route('/dashboard')                                # Ruta este /doctor/dashboard
@login_required                                               # Doar utilizatorii logați pot accesa
@doctor_required                                              # Doar utilizatorii cu rol de doctor pot accesa
def dashboard():
    """Doctor dashboard with their implant statistics and recent cases"""

    # Obținem statisticile implanturilor pentru doctorul curent
    stats = get_doctor_statistics(current_user.id)
    
    # Obținem cele mai recente 5 implanturi pentru doctorul curent, sortate descrescător după data creării
    recent_implants = (
        Implant.query
        .filter_by(doctor_id=current_user.id)
        .order_by(Implant.created_at.desc())
        .limit(5)
        .all()
    )
    
    # Obținem numărul de implanturi grupate după tip, doar pentru doctorul curent
    implant_types = (
        db.session.query(
            ImplantType.name,                              # Numele tipului de implant
            db.func.count(Implant.id).label('count')      # Numărăm câte implanturi sunt din fiecare tip
        )
        .join(Implant, ImplantType.id == Implant.type_id)  # Facem join între tipuri și implanturi pe baza ID-ului de tip
        .filter(Implant.doctor_id == current_user.id)      # Doar implanturile doctorului curent
        .group_by(ImplantType.name)                         # Grupăm după numele tipului
        .all()
    )
    
    # Separăm datele pentru a le folosi în grafice (etichete și numere)
    type_labels = [t.name for t in implant_types]            # Etichetele pentru graficele de tip (nume tip)
    type_counts = [t.count for t in implant_types]            # Valorile (numărul de implanturi per tip)
    
    # Obținem numărul de implanturi grupate după status (ex: activ, finalizat), doar pentru doctorul curent
    implant_statuses = (
        db.session.query(
            Implant.status,                                  # Statusul implantului
            db.func.count(Implant.id).label('count')        # Numărăm câte implanturi sunt din fiecare status
        )
        .filter(Implant.doctor_id == current_user.id)       # Doar implanturile doctorului curent
        .group_by(Implant.status)                            # Grupăm după status
        .all()
    )
    
    # Separăm datele pentru a le folosi în grafice (etichete și numere)
    status_labels = [s.status for s in implant_statuses]     # Etichetele pentru graficele de status (ex: "activ", "in curs")
    status_counts = [s.count for s in implant_statuses]       # Valorile (numărul de implanturi per status)
    
    # Returnăm template-ul HTML al dashboard-ului doctorului, împreună cu toate datele necesare
    return render_template(
        'doctor/dashboard.html',                              # Template-ul HTML folosit
        stats=stats,                                          # Statistici generale
        recent_implants=recent_implants,                      # Ultimele 5 implanturi
        type_labels=type_labels,                              # Etichetele pentru tipurile de implant
        type_counts=type_counts,                              # Numărul de implanturi per tip
        status_labels=status_labels,                          # Etichetele pentru statusurile implanturilor
        status_counts=status_counts,                          # Numărul de implanturi per status
        title='Doctor Dashboard'                              # Titlul paginii
    )
