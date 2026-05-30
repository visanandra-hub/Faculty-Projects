# =======================
# admin_routes.py
# Rute pentru administratori (gestionare utilizatori, dashboard, statistici)
# =======================

# Importuri din Flask pentru rutare, template-uri, redirecționare, mesaje etc.
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify

# Pentru a verifica dacă utilizatorul este logat și pentru a accesa utilizatorul curent
from flask_login import login_required, current_user

# Pentru criptarea parolelor
from werkzeug.security import generate_password_hash

# Pentru manipularea datelor tabelare (statistici etc.)
import pandas as pd

# Importă instanța bazei de date
from app import db

# Importă modelele ORM definite pentru User, Implant, ImplantType
from models import User, Implant, ImplantType

# Formularul pentru crearea/editarea utilizatorilor
from forms import UserForm

# Decorator care verifică dacă utilizatorul este admin și funcția de statistici
from utils import admin_required, get_implant_statistics

# Definim un Blueprint pentru secțiunea de administrare, prefixul URL va fi /admin
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


# =======================
# DASHBOARD ADMIN
# =======================

@admin_bp.route('/dashboard')
@login_required  # Acces permis doar utilizatorilor autentificați
@admin_required  # Acces permis doar administratorilor
def dashboard():
    """Dashboard-ul adminului, cu statistici și grafice"""

    # Obține statistici generale (ex: total implanturi, active, inactive etc.)
    stats = get_implant_statistics()

    # Interogare: cei mai buni 5 doctori după numărul de implanturi gestionate
    doctors_with_implants = db.session.query(
        User.username,
        db.func.count(Implant.id).label('count')
    ).join(
        Implant, User.id == Implant.doctor_id
    ).filter(
        User.role == 'doctor'
    ).group_by(
        User.id, User.username
    ).order_by(
        db.desc('count')
    ).limit(5).all()

    # Transformă rezultatele într-o listă de dicționare pentru template
    top_doctors = [{'name': doctor[0], 'count': doctor[1]} for doctor in doctors_with_implants]

    # Obține ultimele 5 implanturi înregistrate
    recent_implants = Implant.query.order_by(Implant.created_at.desc()).limit(5).all()

    # Returnează pagina HTML cu datele pentru dashboard
    return render_template(
        'admin/dashboard.html',
        stats=stats,
        top_doctors=top_doctors,
        recent_implants=recent_implants,
        title='Admin Dashboard'
    )


# =======================
# PAGINA DE GESTIONARE UTILIZATORI
# =======================

@admin_bp.route('/users')
@login_required
@admin_required
def user_management():
    """Pagina de administrare a utilizatorilor"""

    users = User.query.all()  # Obține toți utilizatorii
    form = UserForm()  # Creează un formular gol
    form.role.choices = [('doctor', 'Doctor'), ('admin', 'Admin')]  # Setează opțiunile pentru rol

    return render_template(
        'admin/user_management.html',
        users=users,
        form=form,
        title='User Management'
    )


# =======================
# ADAUGARE UTILIZATOR
# =======================

@admin_bp.route('/users/add', methods=['POST'])
@login_required
@admin_required
def add_user():
    """Adaugă un nou utilizator în sistem"""
    form = UserForm()
    form.role.choices = [('doctor', 'Doctor'), ('admin', 'Admin')]

    if form.validate_on_submit():
        # Verifică dacă emailul sau username-ul există deja
        existing_email = User.query.filter_by(email=form.email.data).first()
        existing_username = User.query.filter_by(username=form.username.data).first()

        if existing_email:
            flash('Email already registered.', 'danger')
        elif existing_username:
            flash('Username already taken.', 'danger')
        else:
            # Creează noul utilizator și setează atributele
            new_user = User()
            new_user.username = form.username.data
            new_user.email = form.email.data
            # Parola este criptată sau se pune una implicită dacă lipsește
            if form.password.data:
                new_user.password_hash = generate_password_hash(form.password.data)
            else:
                new_user.password_hash = generate_password_hash("default-password")
            new_user.role = form.role.data

            db.session.add(new_user)
            db.session.commit()
            flash(f'User {form.username.data} has been created successfully!', 'success')
    else:
        # Afișează erorile din formular
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{field}: {error}", 'danger')

    return redirect(url_for('admin.user_management'))


# =======================
# EDITARE UTILIZATOR
# =======================

@admin_bp.route('/users/<int:user_id>/edit', methods=['POST'])
@login_required
@admin_required
def edit_user(user_id):
    """Editează un utilizator existent"""

    user = User.query.get_or_404(user_id)  # Găsește utilizatorul sau dă eroare 404
    form = UserForm()
    form.role.choices = [('doctor', 'Doctor'), ('admin', 'Admin')]

    if form.validate_on_submit():
        # Verifică dacă noile date nu se suprapun cu alt utilizator
        email_exists = User.query.filter(User.email == form.email.data, User.id != user_id).first()
        username_exists = User.query.filter(User.username == form.username.data, User.id != user_id).first()

        if email_exists:
            flash('Email already registered.', 'danger')
        elif username_exists:
            flash('Username already taken.', 'danger')
        else:
            user.username = form.username.data
            user.email = form.email.data
            user.role = form.role.data
            # Actualizează parola dacă este furnizată
            if form.password.data:
                user.password_hash = generate_password_hash(form.password.data)

            db.session.commit()
            flash(f'User {user.username} has been updated successfully!', 'success')
    else:
        # Afișează erorile din formular
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{field}: {error}", 'danger')

    return redirect(url_for('admin.user_management'))


# =======================
# ȘTERGERE UTILIZATOR
# =======================

@admin_bp.route('/users/<int:user_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    """Șterge un utilizator (dacă nu e curentul și nu are implanturi asignate)"""

    # Previne ștergerea contului propriu
    if user_id == current_user.id:
        flash('You cannot delete your own account.', 'danger')
        return redirect(url_for('admin.user_management'))

    user = User.query.get_or_404(user_id)

    # Verifică dacă utilizatorul are implanturi înregistrate
    implant_count = Implant.query.filter_by(doctor_id=user.id).count()
    if implant_count > 0:
        flash(f'Cannot delete user. {user.username} has {implant_count} implants assigned.', 'danger')
    else:
        db.session.delete(user)
        db.session.commit()
        flash(f'User {user.username} has been deleted successfully!', 'success')

    return redirect(url_for('admin.user_management'))


# =======================
# API PENTRU STATISTICI
# =======================

@admin_bp.route('/statistics/api')
@login_required
@admin_required
def statistics_api():
    """Endpoint API pentru statistici (grafic dashboard)"""
    stats = get_implant_statistics()  # Obține datele statistice
    return jsonify(stats)  # Returnează JSON pentru interfață (AJAX etc.)
