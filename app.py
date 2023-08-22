from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
import os
import subprocess
import psycopg2


app = Flask(__name__)
app.secret_key = 'your_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin):
    def __init__(self, username, password):
        self.id = username
        self.username = username
        self.password = password

    def get_id(self):
        return self.id


@login_manager.user_loader
def load_user(username):
    # Connect to the PostgreSQL database
    try:
        '''В 29 строке аргумент password необходимо изменить на Ваш пароль от пользователя'''
        conn = psycopg2.connect(database='IP_in', user='postgres', host='localhost', port='5432', password='8989')
        cursor = conn.cursor()
        cursor.execute("SELECT name, password FROM Users")
        row = cursor.fetchall()

        if row is not None:
            users = {'admin': User(row[0][0], row[0][1]), 'devops': User(row[1][0], row[1][1])}
            return users.get(username)
    except Exception:
        print("No database connection")

    # If no user is found, return None
    return None


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = load_user(username)
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('index'))
        return render_template('login.html', error='Invalid username or password')

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/')
@login_required
def index():
    interfaces = []
    output = subprocess.check_output(['ip', 'addr', 'show']).decode('utf-8')

    lines = output.split('\n')
    for line in lines:
        if 'inet ' in line:
            parts = line.strip().split(' ')
            name = parts[-1].split(':')[0]
            ip = parts[1].split('/')[0]
            interfaces.append({'name': name, 'ip': ip})

    return render_template('index.html', interfaces=interfaces)


@app.route('/add_ip', methods=['POST'])
@login_required
def add_ip():
    interface = request.form['interface']
    ip = request.form['ip']
    os.system(f'sudo ip addr add {ip} dev {interface}')
    return redirect(url_for('index'))


@app.route('/edit_ip', methods=['POST'])
@login_required
def edit_ip():
    interface = request.form['interface']
    old_ip = request.form['old_ip']
    new_ip = request.form['new_ip']
    os.system(f'sudo ip addr del {old_ip} dev {interface}')
    os.system(f'sudo ip addr add {new_ip} dev {interface}')
    return redirect(url_for('index'))


@app.route('/clear_ip', methods=['POST'])
@login_required
def clear_ip():
    interface = request.form['interface']
    ip = request.form['ip']
    os.system(f'sudo ip addr del {ip} dev {interface}')
    return redirect(url_for('index'))


@app.route('/rename_interface', methods=['POST'])
@login_required
def rename_interface():
    old_name = request.form['old_name']
    new_name = request.form['new_name']
    os.system(f'sudo ip link set {old_name} down')
    os.system(f'sudo ip link set {old_name} name {new_name}')
    os.system(f'sudo ip link set {new_name} up')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
