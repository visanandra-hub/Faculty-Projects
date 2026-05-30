# Importăm clasele necesare pentru formulare din Flask-WTF și WTForms
from flask_wtf import FlaskForm                               # Bază pentru toate formularele din Flask
from wtforms import StringField, PasswordField, BooleanField, SelectField, DateField, TextAreaField
# Importăm validatorii pentru validarea datelor introduse de utilizator
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional

# Formular pentru logarea utilizatorului
class LoginForm(FlaskForm):
    """Form for user login"""

    # Câmp pentru email, obligatoriu și validat ca email
    email = StringField('Email', validators=[DataRequired(), Email()])

    # Câmp pentru parolă, obligatoriu
    password = PasswordField('Password', validators=[DataRequired()])

    # Checkbox pentru reținerea sesiunii (Remember Me)
    remember = BooleanField('Remember Me')

# Formular pentru crearea sau editarea utilizatorilor
class UserForm(FlaskForm):
    """Form for creating/editing users"""

    # Câmp pentru username, obligatoriu, cu lungime între 3 și 64 caractere
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])

    # Câmp pentru email, obligatoriu, validat ca email, lungime maximă 120
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])

    # Câmp pentru parolă, opțional (în cazul în care se editează un utilizator),
    # dar dacă este completat, trebuie să aibă minim 6 caractere
    password = PasswordField('Password', validators=[
        Optional(),  # Parola este opțională la editare
        Length(min=6, message='Password must be at least 6 characters')
    ])

    # Câmp select pentru rolul utilizatorului: doctor sau admin
    role = SelectField('Role', validators=[DataRequired()],
                       choices=[('doctor', 'Doctor'), ('admin', 'Admin')])

# Formular pentru crearea sau editarea înregistrărilor de implanturi
class ImplantForm(FlaskForm):
    """Form for creating/editing implant records"""

    # Selectăm tipul de implant (coerce=int transformă valoarea selectată în întreg)
    type_id = SelectField('Implant Type', validators=[DataRequired()], coerce=int)

    # Numele pacientului, obligatoriu, cu lungime maximă de 100 caractere
    patient_name = StringField('Patient Name', validators=[DataRequired(), Length(max=100)])

    # Selectăm doctorul responsabil de implant (ID întreg)
    doctor_id = SelectField('Doctor', validators=[DataRequired()], coerce=int)

    # Data implantului, obligatorie
    implant_date = DateField('Implant Date', validators=[DataRequired()])

    # Selectăm statusul implantului: activ, eliminat sau înlocuit
    status = SelectField('Status', validators=[DataRequired()],
                         choices=[('Active', 'Active'), ('Removed', 'Removed'), ('Replaced', 'Replaced')])

    # Câmp opțional pentru note suplimentare
    notes = TextAreaField('Notes', validators=[Optional()])
