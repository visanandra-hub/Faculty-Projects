# Importăm modulele necesare din Flask și extensii
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from datetime import datetime
import uuid

# Importăm instanța bazei de date, modelele și formularul necesar
from app import db
from models import Implant, ImplantType, User
from forms import ImplantForm
from utils import admin_required

# Definim un blueprint pentru rutele legate de implanturi, cu prefixul /implants
implant_bp = Blueprint('implant', __name__, url_prefix='/implants')

# ======================
# LISTARE IMPLANTURI
# ======================
@implant_bp.route('/')
@login_required
def list_implants():
    """List all implants (filtered by doctor for non-admin users)"""

    # Form simplu pentru protecție CSRF în șablon (chiar dacă nu are câmpuri)
    form = FlaskForm()
    
    # Preluăm parametrii de filtrare din URL
    implant_type = request.args.get('type')
    status = request.args.get('status')
    doctor_id = request.args.get('doctor')
    
    # Pornim de la o interogare de bază
    query = Implant.query
    
    # Aplicăm filtre în funcție de rolul utilizatorului și parametrii de filtrare
    if not current_user.is_admin():
        # Doctorii văd doar propriile implanturi
        query = query.filter_by(doctor_id=current_user.id)
    else:
        # Adminii pot filtra și după doctor
        if doctor_id and doctor_id.isdigit():
            query = query.filter_by(doctor_id=int(doctor_id))
    
    # Filtrare după tip de implant
    if implant_type and implant_type.isdigit():
        query = query.filter_by(type_id=int(implant_type))
    
    # Filtrare după status
    if status:
        query = query.filter_by(status=status)
    
    # Executăm interogarea și obținem lista de implanturi, ordonate descrescător după data creării
    implants = query.order_by(Implant.created_at.desc()).all()
    
    # Date adiționale pentru filtre în interfață
    implant_types = ImplantType.query.all()
    doctors = User.query.filter_by(role='doctor').all() if current_user.is_admin() else []
    
    # Rendem șablonul HTML pentru listarea implanturilor
    return render_template(
        'implants/list.html',
        implants=implants,
        implant_types=implant_types,
        doctors=doctors,
        statuses=['Active', 'Removed', 'Replaced'],
        form=form,
        title='Implant Records'
    )

# ======================
# ADĂUGARE IMPLANT
# ======================
@implant_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_implant():
    """Add a new implant record"""
    form = ImplantForm()
    
    # Populăm opțiunile pentru câmpurile de selectare
    form.type_id.choices = [(t.id, t.name) for t in ImplantType.query.all()]
    
    if current_user.is_admin():
        # Adminul poate alege oricare doctor
        form.doctor_id.choices = [(d.id, d.username) for d in User.query.filter_by(role='doctor').all()]
    else:
        # Doctorul poate selecta doar pe el însuși
        form.doctor_id.choices = [(current_user.id, current_user.username)]
        form.doctor_id.data = current_user.id  # Preselectăm doctorul curent
    
    if form.validate_on_submit():
        # Generăm un ID unic pentru implant
        implant_id = f"IMP-{str(uuid.uuid4())[:8].upper()}"
        
        # Cream obiectul nou de tip Implant
        new_implant = Implant()
        new_implant.implant_id = implant_id
        new_implant.type_id = form.type_id.data
        new_implant.patient_name = form.patient_name.data
        new_implant.doctor_id = form.doctor_id.data
        new_implant.implant_date = form.implant_date.data
        new_implant.status = form.status.data
        new_implant.notes = form.notes.data
        
        # Salvăm în baza de date
        db.session.add(new_implant)
        db.session.commit()
        
        # Afișăm un mesaj de succes
        flash('Implant record has been added successfully!', 'success')
        return redirect(url_for('implant.list_implants'))
    
    return render_template(
        'implants/add.html',
        form=form,
        title='Add Implant Record'
    )

# ======================
# VIZUALIZARE IMPLANT
# ======================
@implant_bp.route('/<int:implant_id>', methods=['GET'])
@login_required
def view_implant(implant_id):
    """View a single implant record"""

    # Căutăm implantul după ID sau returnăm 404 dacă nu există
    implant = Implant.query.get_or_404(implant_id)
    
    # Form pentru CSRF
    form = FlaskForm()
    
    # Verificăm dacă utilizatorul are dreptul să vadă implantul
    if not current_user.is_admin() and implant.doctor_id != current_user.id:
        flash('You do not have permission to view this implant record.', 'danger')
        return redirect(url_for('implant.list_implants'))
    
    return render_template(
        'implants/view.html',
        implant=implant,
        form=form,
        title=f'Implant {implant.implant_id}'
    )

# ======================
# EDITARE IMPLANT
# ======================
@implant_bp.route('/<int:implant_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_implant(implant_id):
    """Edit an existing implant record"""

    # Căutăm implantul sau returnăm 404
    implant = Implant.query.get_or_404(implant_id)
    
    # Verificăm permisiunea de editare
    if not current_user.is_admin() and implant.doctor_id != current_user.id:
        flash('You do not have permission to edit this implant record.', 'danger')
        return redirect(url_for('implant.list_implants'))
    
    # Formular pre-populat cu valorile existente
    form = ImplantForm(obj=implant)
    
    # Populăm opțiunile pentru câmpurile selectabile
    form.type_id.choices = [(t.id, t.name) for t in ImplantType.query.all()]
    
    if current_user.is_admin():
        form.doctor_id.choices = [(d.id, d.username) for d in User.query.filter_by(role='doctor').all()]
    else:
        form.doctor_id.choices = [(current_user.id, current_user.username)]
        form.doctor_id.data = current_user.id
    
    if form.validate_on_submit():
        # Actualizăm câmpurile implantului
        implant.type_id = form.type_id.data
        implant.patient_name = form.patient_name.data
        implant.doctor_id = form.doctor_id.data
        implant.implant_date = form.implant_date.data
        implant.status = form.status.data
        implant.notes = form.notes.data
        implant.updated_at = datetime.utcnow()
        
        # Salvăm modificările
        db.session.commit()
        
        flash('Implant record has been updated successfully!', 'success')
        return redirect(url_for('implant.view_implant', implant_id=implant.id))
    
    return render_template(
        'implants/edit.html',
        form=form,
        implant=implant,
        title=f'Edit Implant {implant.implant_id}'
    )

# ======================
# ȘTERGERE IMPLANT
# ======================
@implant_bp.route('/<int:implant_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_implant(implant_id):
    """Delete an implant record (admin only)"""

    # Căutăm implantul sau 404
    implant = Implant.query.get_or_404(implant_id)
    
    # Ștergem din baza de date
    db.session.delete(implant)
    db.session.commit()
    
    flash('Implant record has been deleted successfully!', 'success')
    return redirect(url_for('implant.list_implants'))

# ======================
# API - DATE PENTRU DATATABLES
# ======================
@implant_bp.route('/api/data')
@login_required
def api_data():
    """API endpoint for implant data (used by DataTables)"""

    # Adminul vede toate implanturile, doctorul doar ale lui
    if current_user.is_admin():
        implants = Implant.query.all()
    else:
        implants = Implant.query.filter_by(doctor_id=current_user.id).all()
    
    # Returnăm datele în format JSON, folosind metoda to_dict() definită în model
    return jsonify({
        'data': [implant.to_dict() for implant in implants]
    })
