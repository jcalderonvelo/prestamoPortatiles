from flask import Flask, render_template, request, redirect, url_for, session
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash

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
            return redirect(url_for('dashboard'))
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
        return redirect(url_for('login'))
    cursor = db.cursor()
    cursor.execute("SELECT * FROM portatiles")
    portatiles = cursor.fetchall()
    return render_template('dashboard.html', portatiles=portatiles)

if __name__ == '__main__':
    app.run(debug=True)
