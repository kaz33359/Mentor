from flask import Flask, render_template, url_for #import flask class
app = Flask(__name__) #setting app variable with flask instancce

app.config['SECRET_KEY'] = '5973c53e6d26093ab3e5e1b1caa8d407'


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

@app.route('/login') # about page of the webpage
def login():
    from = LoginFrom()
    return render_template('login.html', title='Login', form=form)

@app.route('/registration') # about page of the webpage
def registration():
    from = RegistrationForm()
    return render_template('registration.html', title='Register', form=form)


# Anouther way to run flask module
if __name__ == '__main__':
    app.run(debug=True)
