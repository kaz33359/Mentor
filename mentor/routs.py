
from flask import render_template, url_for, flash, redirect
from mentor import app
from mentor.form import RegistrationForm, LoginForm
from mentor.models import User






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
        flash(f'Account created for {form.name.data}!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('registration.html', title='Register', form=form)


@app.route("/login",methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@mentor.com' and form.password.data == 'admin':
            flash('You have been logged in!', 'success')
            #flash(f'Welcome Back  {form.email.data}!')
            return redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/dashboard') # about page of the webpage
def dashboard():
    return render_template('./dashboard.html', title='Dashboard')

@app.route('/test') # about page of the webpage
def test():
    form = RegistrationForm()
    return render_template('test.html', title='test', form=form)
