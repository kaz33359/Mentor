from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from form import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__) #setting app variable with flask instancce

app.config['SECRET_KEY'] = '5973c53e6d26093ab3e5e1b1caa8d407'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    mobile = db.Column(db.Integer, unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

def __repr__(self):
        return f"Post('{self.name}', '{self.email}', '{self.image_file}')"
        

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


# Anouther way to run flask module
if __name__ == '__main__':
    app.run(debug=True)
