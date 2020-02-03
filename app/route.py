from app import app, db, login_manager, bcrypt
from app import LoginForm, RegisterForm
from app import tblUser
from flask import redirect, render_template, request, url_for, flash
import uuid


@app.route('/')
def index():
    return 'Hello World'

@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            username = request.form['username']
            gender = request.form['gender']
            birthdate = request.form['birthdate']
            email = request.form['email']
            password = request.form['password']
            #Hash password
            hashed = bcrypt.generate_password_hash(password).decode('utf-8')
            #Unique Id
            id = str(uuid.uuid4())
            User = tblUser(id= id, name= username, gender= gender, email= email, password= hashed)
            try:
                db.session.add(User)
                db.session.commit()
                return redirect('/')
            except:
                flash(f'Register failed!')
                return 'Register failed!'
            return 'Posted'
    return render_template('views/register.html', form = form)