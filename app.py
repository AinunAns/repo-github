from flask import Flask, render_template, request, redirect, url_for, session
from models import init_db, check_user, register_user, add_record, get_history
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'
init_db()

# Konfigurasi Database
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')  # Diatur oleh Heroku
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if check_user(username, password):
            session['username'] = username
            return redirect(url_for('diagnosis'))
        else:
            return "Invalid credentials. Please try again."
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if register_user(username, password):
            return redirect(url_for('login'))
        else:
            return "Username already exists. Please choose another one."
    return render_template('register.html')

@app.route('/diagnosis', methods=['GET', 'POST'])
def diagnosis():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        gender = request.form['gender']
        age = request.form['age']
        blood_pressure = request.form['blood_pressure']
        heart_disease = request.form['heart_disease']
        smoking = request.form['smoking']
        bmi = request.form['bmi']
        glucose_level = request.form['glucose_level']
        blood_sugar = request.form['blood_sugar']

        if int(blood_sugar) > 200:
            diagnosis = 'Diabetes'
        else:
            diagnosis = 'Non-Diabetes'

        add_record(session['username'], gender, age, blood_pressure, heart_disease, smoking, bmi, glucose_level, blood_sugar, diagnosis)
        return render_template('result.html', diagnosis=diagnosis)
    return render_template('diagnosis.html')

@app.route('/history')
def history():
    if 'username' not in session:
        return redirect(url_for('login'))
    records = get_history(session['username'])
    return render_template('history.html', records=records)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
