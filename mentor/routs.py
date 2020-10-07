
from flask import render_template, url_for, flash, redirect, request
from mentor import app, db, bcrypt
from mentor.form import RegistrationForm, LoginForm
from mentor.models import User
from flask_login import login_user, current_user, logout_user, login_required





@app.route('/') # root page of the webpage
@app.route('/home') # second rout to home page
def home():
    return render_template('home.html')  ## passing argument to template

@app.route('/course') # about page of the webpage
def course():
    return render_template('course.html', title='Course')

@app.route('/news') # about page of the webpage
def news():
    return render_template('news.html', title='News')

@app.route('/community') # about page of the webpage
def community():
    return render_template('community.html', title='Community')

@app.route('/registration',methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=form.name.data, mobile=form.mobile.data ,email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('registration.html', title='Register', form=form)


@app.route("/login",methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')

    return render_template('login.html', title='Login', form=form)

@app.route('/dashboard') # about page of the webpage
def dashboard():
    return render_template('./dashboard.html', title='Dashboard')

@app.route('/test') # about page of the webpage
def test():
    form = RegistrationForm()
    return render_template('test.html', title='test', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')
