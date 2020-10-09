
from flask import render_template, url_for, flash, redirect, request
from mentor import app, db, bcrypt
from mentor.form import RegistrationForm, LoginForm, UpdateAccountForm
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
    if current_user.is_authenticated:
        return redirect(url_for('dashboard_main'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=form.name.data,username=form.username.data, mobile=form.mobile.data ,email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('registration.html', title='Register', form=form)


@app.route("/login",methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard_main'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('dashboard_main'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')

    return render_template('login.html', title='Login', form=form)


@app.route('/dashboard_main') # about page of the webpage
@login_required
def dashboard_main():
    return render_template('./dashboard_main.html', title='Dashboard')

@app.route('/dashboard_psychoTest') # about page of the webpage
@login_required
def dashboard_psychoTest():
    return render_template('./dashboard_psychoTest.html', title='Dashboard - Psycho Test')

@app.route('/dashboard_academics') # about page of the webpage
@login_required
def dashboard_academics():
    return render_template('./dashboard_academics.html', title='Dashboard - Academics')

@app.route('/dashboard_carrer') # about page of the webpage
@login_required
def dashboard_carrer():
    return render_template('./dashboard_carrer.html', title='Dashboard - Carrer')

@app.route('/dashboard_community') # about page of the webpage
@login_required
def dashboard_community():
    return render_template('./dashboard_community.html', title='Dashboard - Community')

@app.route('/dashboard_profile') # about page of the webpage
@login_required
def dashboard_profile():
    form=UpdateAccountForm()
    image_file = url_for('static', filename='assets/images/profile_pics/' + current_user.image_file)
    return render_template('./dashboard_profile.html', title='Dashboard - Profile', image_file=image_file, form=form)

@app.route('/test') # about page of the webpage
def test():
    form = RegistrationForm()
    return render_template('test.html', title='test', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))
