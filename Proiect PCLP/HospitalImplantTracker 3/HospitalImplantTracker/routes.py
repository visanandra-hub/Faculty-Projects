from flask import Blueprint, redirect, url_for
from flask_login import current_user

# Creează un blueprint numit 'main', care va gestiona rutele principale ale aplicației
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Ruta principală care redirecționează utilizatorul în funcție de rolul său"""
    
    # Verifică dacă utilizatorul este autentificat
    if current_user.is_authenticated:
        # Dacă este admin, redirecționează către dashboard-ul de admin
        if current_user.is_admin():
            return redirect(url_for('admin.dashboard'))
        else:
            # Altfel, este doctor și e redirecționat către dashboard-ul de doctor
            return redirect(url_for('doctor.dashboard'))
    else:
        # Dacă utilizatorul nu este autentificat, este redirecționat către pagina de login
        return redirect(url_for('auth.login'))
