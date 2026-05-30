# =======================
# app.py — Punctul de pornire al aplicației Flask
# =======================

# Biblioteci standard
import os               # Pentru lucrul cu variabile de mediu
import logging          # Pentru loguri în consolă
from datetime import datetime  # Pentru timestamp-uri

# Flask și extensii
from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy         # Integrarea SQLAlchemy cu Flask
from sqlalchemy.orm import DeclarativeBase      # Pentru a crea o clasă de bază personalizată
from flask_login import LoginManager            # Pentru autentificare
from flask_wtf.csrf import CSRFProtect          # Protecție CSRF pentru formulare
from werkzeug.middleware.proxy_fix import ProxyFix  # Middleware pentru servere proxy (ex: Heroku)

# =======================
# CONFIGURARE LOGGING
# =======================
logging.basicConfig(level=logging.DEBUG)  # Afișează toate logurile de nivel DEBUG și mai sus

# =======================
# CLASA DE BAZĂ PENTRU MODELELE ORM
# =======================
class Base(DeclarativeBase):
    pass  # Moștenită de toate modelele definite în `models.py`

# =======================
# INIȚIALIZARE EXTENSII
# =======================
db = SQLAlchemy(model_class=Base)  # Inițializează SQLAlchemy cu modelul de bază
login_manager = LoginManager()     # Gestionare autentificare
csrf = CSRFProtect()               # Protecție împotriva atacurilor CSRF

# =======================
# CREAREA APLICAȚIEI FLASK
# =======================
app = Flask(__name__)  # Creează aplicația Flask
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")  # Cheia secretă pentru sesiuni și CSRF

# Middleware care rezolvă problemele de proxy (folosit mai ales pe Heroku sau servere Nginx)
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# =======================
# CONFIGURARE BAZĂ DE DATE
# =======================
# Obține URL-ul bazei de date din variabilă de mediu (sau folosește SQLite implicit)
database_url = os.environ.get("DATABASE_URL", "sqlite:///hospital.db")

# Corecție: SQLAlchemy vrea `postgresql://`, dar Heroku oferă `postgres://`
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

# Setează configurările pentru SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,     # Refolosește conexiunile vechi
    "pool_pre_ping": True    # Verifică dacă o conexiune e validă
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # Oprește notificările inutile

# =======================
# LEAGĂ EXTENSIILE LA APLICAȚIE
# =======================
db.init_app(app)
login_manager.init_app(app)
csrf.init_app(app)

# Configurează ruta de login implicită pentru @login_required
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'

# =======================
# CONTEXT GLOBAL PENTRU TEMPLATE-URI (valori transmise automat)
# =======================
@app.context_processor
def inject_context():
    return {
        'now': datetime.utcnow(),  # Timpul actual
        'app_name': 'Hospital Implant Tracker'  # Numele aplicației
    }

# =======================
# INIȚIALIZARE LA STARTUL APLICAȚIEI
# =======================
with app.app_context():
    # Importă modelele pentru ca SQLAlchemy să le înregistreze
    from models import User, Implant, ImplantType

    # Importă și înregistrează toate blueprint-urile (grupuri de rute)
    from auth import auth_bp
    from routes import main_bp
    from admin_routes import admin_bp
    from doctor_routes import doctor_bp
    from implant_routes import implant_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(doctor_bp)
    app.register_blueprint(implant_bp)

    # Creează tabelele în baza de date (dacă nu există)
    db.create_all()

    # =======================
    # CREARE UTILIZATOR ȘI TIPURI IMPLICITE (la prima rulare)
    # =======================
    from werkzeug.security import generate_password_hash

    # Verifică dacă există deja un admin
    admin = User.query.filter_by(email='admin@ex.com').first()
    if not admin:
        admin = User()
        admin.username = 'admin'
        admin.email = 'admin@ex.com'
        admin.password_hash = generate_password_hash('admin123')
        admin.role = 'admin'
        db.session.add(admin)

        # Tipuri standard de implanturi
        implant_types = [
            "Hip Replacement",
            "Knee Replacement",
            "Pacemaker",
            "Dental Implant",
            "Cardiac Stent",
            "Breast Implant",
            "Cochlear Implant",
            "Spinal Implant"
        ]

        # Adaugă fiecare tip în baza de date
        for type_name in implant_types:
            implant_type = ImplantType()
            implant_type.name = type_name
            db.session.add(implant_type)

        # Salvează în baza de date
        db.session.commit()
        logging.info("Created default admin user and implant types")

# =======================
# GESTIONARE ERORI
# =======================

# Redirecționează către pagina principală dacă apare o eroare 404
@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('main.index'))

# Redirecționează și în caz de eroare 500 (server error)
@app.errorhandler(500)
def internal_server_error(e):
    return redirect(url_for('main.index'))
