from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user
import calendar
from datetime import datetime, timedelta

from app import db
from models import Implant, ImplantType

# ==============================
# DECORATORI DE SECURITATE
# ==============================

def admin_required(f):
    """Decorator pentru rute accesibile doar de administratori"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin():
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

def doctor_required(f):
    """Decorator pentru rute accesibile de doctori sau administratori"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_doctor() and not current_user.is_admin():
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

# ==============================
# FUNCȚII DE STATISTICI
# ==============================

def get_implant_statistics():
    """Generează statistici generale pentru dashboard-ul administratorului"""
    
    # Totalul tuturor implanturilor
    total_implants = Implant.query.count()
    
    # Gruparea implanturilor pe tip (ex: tip A - 5 buc, tip B - 7 buc)
    implant_by_type = db.session.query(
        ImplantType.name, 
        db.func.count(Implant.id).label('count')
    ).join(Implant, ImplantType.id == Implant.type_id) \
     .group_by(ImplantType.name) \
     .all()
    
    type_labels = [t.name for t in implant_by_type]
    type_counts = [t.count for t in implant_by_type]
    
    # Gruparea pe status (Active, Removed, Replaced)
    implant_by_status = db.session.query(
        Implant.status, 
        db.func.count(Implant.id).label('count')
    ).group_by(Implant.status) \
     .all()
    
    status_labels = [s.status for s in implant_by_status]
    status_counts = [s.count for s in implant_by_status]
    
    # Implanturi adăugate în luna curentă
    today = datetime.utcnow()
    first_day = datetime(today.year, today.month, 1)
    implants_this_month = Implant.query.filter(Implant.created_at >= first_day).count()
    
    # Trendul lunar pentru ultimele 6 luni (numărul de implanturi în fiecare lună)
    monthly_trend = []
    month_labels = []
    
    for i in range(5, -1, -1):  # de la 5 luni în urmă până la luna curentă
        month_date = today - timedelta(days=30 * i)
        month_start = datetime(month_date.year, month_date.month, 1)
        
        # Pentru lunile anterioare, se setează sfârșitul lunii
        if i > 0:
            next_month = month_date + timedelta(days=30)
            month_end = datetime(next_month.year, next_month.month, 1)
        else:
            month_end = today + timedelta(days=1)  # luna curentă
        
        count = Implant.query.filter(
            Implant.created_at >= month_start,
            Implant.created_at < month_end
        ).count()
        
        month_labels.append(month_date.strftime('%b %Y'))  # ex: "Jan 2025"
        monthly_trend.append(count)
    
    # Returnează datele în format dict pentru afișare în dashboard (grafic, carduri, etc.)
    return {
        'total_implants': total_implants,
        'implants_this_month': implants_this_month,
        'type_labels': type_labels,
        'type_counts': type_counts,
        'status_labels': status_labels,
        'status_counts': status_counts,
        'month_labels': month_labels,
        'monthly_trend': monthly_trend
    }

def get_doctor_statistics(doctor_id):
    """Generează statistici pentru un anumit doctor (pentru dashboard-ul doctorului)"""
    
    # Total implanturi create de doctorul respectiv
    total_implants = Implant.query.filter_by(doctor_id=doctor_id).count()
    
    # Implanturi adăugate de doctor în luna curentă
    today = datetime.utcnow()
    first_day = datetime(today.year, today.month, 1)
    implants_this_month = Implant.query.filter(
        Implant.doctor_id == doctor_id,
        Implant.created_at >= first_day
    ).count()
    
    # Numărul de implanturi active pentru acel doctor
    active_implants = Implant.query.filter_by(
        doctor_id=doctor_id,
        status='Active'
    ).count()
    
    return {
        'total_implants': total_implants,
        'implants_this_month': implants_this_month,
        'active_implants': active_implants
    }
