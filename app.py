from flask import Flask, render_template, request, redirect, url_for, session
import pymysql
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'

db = pymysql.connect(host='10.3.29.20', port=33060, user='user_gr2', password='portatil123', database='gr2_db')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cursor = db.cursor()
        cursor.execute("SELECT id, password_hash FROM usuarios WHERE email = %s", (email,))
        user = cursor.fetchone()
        if user and check_password_hash(user[1], password):
            session['user_id'] = user[0]
            return redirect(url_for('dashboard'))  # Redirige a dashboard después de iniciar sesión correctamente
        else:
            return "Credenciales incorrectas", 401
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        cursor = db.cursor()
        cursor.execute("INSERT INTO usuarios (username, email, password_hash) VALUES (%s, %s, %s)", 
                       (username, email, password))
        db.commit()
        
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Si no está logueado, redirige a login
    cursor = db.cursor()
    cursor.execute("SELECT * FROM portatiles")
    portatiles = cursor.fetchall()
    return render_template('dashboard.html', portatiles=portatiles)

@app.route('/alquilar/<int:portatil_id>')
def alquilar(portatil_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Si no está logueado, redirige a login

    user_id = session['user_id']
    inicio = datetime.now()
    fin = inicio.replace(hour=23, minute=59, second=59)  # Suponiendo alquiler de un día

    cursor = db.cursor()

    # Verifica si ya hay una reserva para ese usuario y portatil
    cursor.execute("SELECT * FROM fecha WHERE id_usuarios = %s AND id_portatiles = %s", (user_id, portatil_id))
    existing_reservation = cursor.fetchone()

    if existing_reservation:
        # Si ya hay una reserva, devuelve un mensaje de error o redirige a otra página
        return "Ya tienes una reserva para este portatil.", 400

    # Si no existe la reserva, inserta la nueva
    try:
        cursor.execute("INSERT INTO fecha (id_usuarios, id_portatiles, inicio, fin) VALUES (%s, %s, %s, %s)",
                       (user_id, portatil_id, inicio, fin))
        db.commit()
    except pymysql.MySQLError as e:
        return f"Error al hacer la reserva: {e}", 500

    return redirect(url_for('dashboard'))

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        correo = request.form['correo']
        password = request.form['password']
        
        cursor = db.cursor()
        cursor.execute("SELECT id, password FROM admin WHERE correo = %s", (correo,))
        admin = cursor.fetchone()
        
        if admin and admin[1] == password:
            session['admin_id'] = admin[0]
            return redirect(url_for('admin_dashboard'))
        else:
            return "Correo o contraseña incorrectos", 401

    return render_template('admin_login.html')

@app.route('/admin_dashboard')
def admin_dashboard():
    if 'admin_id' not in session:
        return redirect(url_for('admin_login'))  # Si no está logueado como admin, redirige al login
    
    cursor = db.cursor()
    
    # Consulta para obtener los portátiles y las reservas
    cursor.execute("""
        SELECT p.id, p.marca, p.estado, p.almacenamiento, p.OS, r.inicio, u.username, u.email
        FROM portatiles p
        LEFT JOIN fecha r ON p.id = r.id_portatiles
        LEFT JOIN usuarios u ON r.id_usuarios = u.id
        ORDER BY r.inicio DESC
    """)
    portatiles_reservados = cursor.fetchall()

    return render_template('admin_dashboard.html', portatiles_reservados=portatiles_reservados)

@app.route('/reservados')
def reservados():
    if 'admin_id' not in session:
        return redirect(url_for('admin_login'))  # Si no está logueado como admin, redirige al login
    
    cursor = db.cursor()
    
    # Consulta para obtener los portátiles y las reservas
    cursor.execute("""
        SELECT p.id, p.marca, p.estado, p.almacenamiento, p.OS, r.inicio, u.username, u.email
        FROM portatiles p
        LEFT JOIN fecha r ON p.id = r.id_portatiles
        LEFT JOIN usuarios u ON r.id_usuarios = u.id
        ORDER BY r.inicio DESC
    """)
    portatiles_reservados = cursor.fetchall()

    return render_template('reservados.html', portatiles_reservados=portatiles_reservados)

@app.route('/mis_reservas')
def mis_reservas():
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Si no está logueado, redirige a login

    user_id = session['user_id']
    cursor = db.cursor()

    # Consulta para obtener las reservas del usuario
    cursor.execute("""
        SELECT p.id, p.marca, f.inicio
        FROM portatiles p
        JOIN fecha f ON p.id = f.id_portatiles
        WHERE f.id_usuarios = %s
        ORDER BY f.inicio DESC
    """, (user_id,))
    reservas = cursor.fetchall()

    return render_template('mis_reservas.html', reservas=reservas)

@app.route('/logout')
def logout():
    session.pop('admin_id', None)
    session.pop('user_id', None)  # Elimina al usuario también si está logueado
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
