# ================================
# auth.py — Gestionarea autentificării utilizatorilor
# ================================

from flask import Blueprint, render_template, redirect, url_for, flash, request  # Importuri esențiale pentru rutare, redirecționare și mesaje
from flask_login import login_user, logout_user, login_required, current_user    # Funcții de autentificare din Flask-Login
from werkzeug.security import check_password_hash                                # Verificarea parolei criptate

from app import db               # Instanța bazei de date SQLAlchemy
from models import User          # Modelul User definit în models.py
from forms import LoginForm      # Formularul pentru autentificare (email, parolă, remember me)

auth_bp = Blueprint('auth', __name__)  # Creează blueprint-ul pentru zona de autentificare

@auth_bp.route('/login', methods=['GET', 'POST'])  # Rută pentru login, permite GET și POST
def login():
    # Dacă utilizatorul este deja autentificat, îl redirecționează spre dashboard-ul său
    if current_user.is_authenticated:
        if current_user.is_admin():                         # Dacă este admin
            return redirect(url_for('admin.dashboard'))     # Trimite către dashboard-ul adminului
        else:
            return redirect(url_for('doctor.dashboard'))    # Altfel, către dashboard-ul doctorului

    form = LoginForm()  # Creează instanța formularului de login

    # Dacă formularul a fost trimis (POST) și datele sunt valide
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()  # Caută utilizatorul după email

        # Verifică dacă utilizatorul există și parola introdusă este corectă
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user, remember=form.remember.data)  # Autentifică utilizatorul, setează remember me dacă e bifat
            next_page = request.args.get('next')           # Verifică dacă utilizatorul a venit de la o pagină protejată

            # Redirecționează în funcție de rolul utilizatorului
            if user.is_admin():
                return redirect(next_page or url_for('admin.dashboard'))   # Dacă e admin → dashboard admin
            else:
                return redirect(next_page or url_for('doctor.dashboard'))  # Dacă e doctor → dashboard doctor
        else:
            flash('Invalid email or password. Please try again.', 'danger')  # Dacă datele nu sunt valide

    # Dacă e GET sau POST invalid → afișează formularul de login
    return render_template('login.html', form=form, title='Login')  # Afișează pagina HTML cu formularul

@auth_bp.route('/logout')  # Rută pentru delogare
@login_required             # Doar utilizatorii autentificați pot accesa
def logout():
    logout_user()  # Deconectează utilizatorul curent
    flash('You have been logged out successfully.', 'success')  # Afișează mesaj de succes
    return redirect(url_for('auth.login'))  # Redirecționează către pagina de login
