import uuid

from sqlite3 import connect 
from flask import Flask, render_template, request, redirect, session
from datetime import datetime 
from flask_session import Session 
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError 
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required

# Application configuration
app = Flask(__name__, static_url_path='/static')

# Ensuring the templates are auto-reloaded 
app.config['TEMPLATES_AUTO_RELOAD'] = True 

#Ensure responses aren't cached 
@app.after_request
def after_request(response):
    response.headers['Cache-control'] = 'no-cache, no-store, must-validate'
    response.headers['Expires'] = 0
    response.headers['Pragma'] = 'no-cache'
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config['SESSION_FILE_DIR'] = mkdtemp()
app.config['SESSION_PERMANENT'] = False 
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Routes goes here 
# login_required
@app.route('/')
@login_required
def index():
    """Show list of all todoes """
    conn = connect('project.db')
    tasks = []
    result = conn.execute('SELECT * FROM tasks')
    for task in result:
        tasks.append(task)
    conn.close()
    return render_template('index.html', tasks=tasks)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Log user in"""
    session.clear() 

    if request.method == 'POST':
        if not request.form.get('username'):
            return 'must provide username'
        elif not request.form.get('password'):
            return 'must provide passsword'
        conn = connect('project.db')
        username = request.form.get('username')
        password = request.form.get('password')
        users = conn.execute('SELECT * FROM users').fetchall()

        fetched_user = 0
        exists = False 
        for user in users:
            if username in user:
                fetched_user = user
                exists = True
                break  
        if exists == True and check_password_hash(fetched_user[2], request.form.get('password')):
            session['user_id'] = fetched_user[0]
            return redirect('/')
        else:
            return redirect('/login')
    
    else: 
        return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    """Log user out """
    session.clear()
    return redirect('/')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if not request.form.get('username'):
            return 'you must provide email'
        if not request.form.get('password'):
            return 'you must provide password'
        if not request.form.get('rpassword'):
            return 'you must confirm password'
        if request.form.get('password') != request.form.get('rpassword'):
            return 'passwords do not match'
        # Registering the user to the database 
        email = request.form.get('username')
        password_hash = generate_password_hash(request.form.get('password'))
        conn = connect('project.db')
        conn.execute('INSERT INTO users(email, hash) VALUES(?, ?)', (email, password_hash))
        conn.commit()
        conn.close()
        return redirect('/')
    else:
        return render_template('register.html')

@app.route('/add', methods=['GET', 'POST'])
@login_required
def addtask():
    if request.method == 'POST':
        if not request.form.get('task'):
            return 'must provide task'
        conn = connect('project.db')
        user_id = 2 
        title = request.form.get('task')
        timestamp = datetime.timestamp(datetime.now())
        conn.execute("INSERT INTO tasks(user_id, title, timestamp) VALUES \
        (?, ?, ?)", (user_id, title, timestamp))
        conn.commit()
        conn.close()
        return redirect('/')
    else:
        return render_template('addtask.html')

@app.route('/delete', methods=['GET', 'POST'])
@login_required
def delete():
    if request.method == 'POST':
        task_id = int(request.json['id'])
        conn = connect('project.db')
        conn.execute('INSERT INTO history(user_id, title) VALUES(?, ?)', (session.get('user_id'), request.json['title']))
        conn.commit()
        conn.execute(f'DELETE FROM tasks WHERE task_id={task_id}')
        conn.commit()
        conn.close()
        return redirect('/')
    else:
        return redirect('/')

@app.route('/history')
@login_required
def history():
    conn = connect('project.db')
    user_id = session.get('user_id')
    history = conn.execute(f'SELECT * FROM history WHERE user_id={user_id}')
    tasks = history.fetchall()
    print(tasks)
    conn.close()
    return render_template('history.html', tasks=tasks) 

if __name__ == "__main__":
    app.run(debug=True)
