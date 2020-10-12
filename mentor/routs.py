
from flask import render_template, url_for, flash, redirect, request
from mentor import app, db, bcrypt
from mentor.form import RegistrationForm, LoginForm, UpdateAccountForm
from mentor.models import User
from flask_login import login_user, current_user, logout_user, login_required
import csv
from newsapi import NewsApiClient


questions = {
 #Format is 'question':[options]
 #'Ma\'an
 'I like to work on cars':['Strongly Disagree','Slightly Disagree','Neutral','Slightly Enjoy','Enjoy'],
 'I like to do puzzles':['Strongly Disagree','Slightly Disagree','Neutral','Slightly Enjoy','Enjoy'],
 'I am good at working independently':['Strongly Disagree','Slightly Disagree','Neutral','Slightly Enjoy','Enjoy'],
 'I like to work in teams':['Strongly Disagree','Slightly Disagree','Neutral','Slightly Enjoy','Enjoy'],
 'I am an ambitious person who set goals for myself':['Strongly Disagree','Slightly Disagree','Neutral','Slightly Enjoy','Enjoy'],
 'I like to organize things (files, desks/offices)':['Strongly Disagree','Slightly Disagree','Neutral','Slightly Enjoy','Enjoy'],
 'I like to build things':['Strongly Disagree','Slightly Disagree','Neutral','Slightly Enjoy','Enjoy'],
 'I like to read about art and music':['Strongly Disagree','Slightly Disagree','Neutral','Slightly Enjoy','Enjoy'],
 'I like to have clear instructions to follow':['Strongly Disagree','Slightly Disagree','Neutral','Slightly Enjoy','Enjoy'],
 'I like to try to influence or persuade people':['Strongly Disagree','Slightly Disagree','Neutral','Slightly Enjoy','Enjoy'],
 'I like to do experiments':['Strongly Disagree','Slightly Disagree','Neutral','Slightly Enjoy','Enjoy'],
 'I like to teach or train people':['Strongly Disagree','Slightly Disagree','Neutral','Slightly Enjoy','Enjoy'],
 'I like trying to help people solve their problems':['Strongly Disagree','Slightly Disagree','Neutral','Slightly Enjoy','Enjoy'],
 'I like to take care of animals':['Strongly Disagree','Slightly Disagree','Neutral','Slightly Enjoy','Enjoy'],
 'I wouldn’t mind working 8 hours per day in an office':['Strongly Disagree','Slightly Disagree','Neutral','Slightly Enjoy','Enjoy'],
 'I enjoy creative writing':['Strongly Disagree','Slightly Disagree','Neutral','Slightly Enjoy','Enjoy'],
 'I enjoy science':['Strongly Disagree','Slightly Disagree','Neutral','Slightly Enjoy','Enjoy'],
 'I am quick to take on new responsibilities':['Strongly Disagree','Slightly Disagree','Neutral','Slightly Enjoy','Enjoy'],
 'I am interested in healing people':['Strongly Disagree','Slightly Disagree','Neutral','Slightly Enjoy','Enjoy'],
 'I enjoy trying to figure out how things work':['Strongly Disagree','Slightly Disagree','Neutral','Slightly Enjoy','Enjoy'],
 'I like putting things together or assembling things':['Strongly Disagree','Slightly Disagree','Neutral','Slightly Enjoy','Enjoy'],
 'I am a creative person':['Strongly Disagree','Slightly Disagree','Neutral','Slightly Enjoy','Enjoy'],
 'I pay attention to details':['Strongly Disagree','Slightly Disagree','Neutral','Slightly Enjoy','Enjoy'],
 'I like to do filing or typing':['Strongly Disagree','Slightly Disagree','Neutral','Slightly Enjoy','Enjoy'],
 'I like to analyze things (problems/situations)':['Strongly Disagree','Slightly Disagree','Neutral','Slightly Enjoy','Enjoy'],
 'I like to play instruments or sing':['Strongly Disagree','Slightly Disagree','Neutral','Slightly Enjoy','Enjoy'],
 'I enjoy learning about other cultures':['Strongly Disagree','Slightly Disagree','Neutral','Slightly Enjoy','Enjoy'],
 'I would like to start my own business':['Strongly Disagree','Slightly Disagree','Neutral','Slightly Enjoy','Enjoy'],
 'I like to cook':['Strongly Disagree','Slightly Disagree','Neutral','Slightly Enjoy','Enjoy'],
 'I like acting in plays':['Strongly Disagree','Slightly Disagree','Neutral','Slightly Enjoy','Enjoy'],
 'I am a practical person':['Strongly Disagree','Slightly Disagree','Neutral','Slightly Enjoy','Enjoy'],
 'I like working with numbers or charts':['Strongly Disagree','Slightly Disagree','Neutral','Slightly Enjoy','Enjoy'],
 'I like to get into discussions about issues':['Strongly Disagree','Slightly Disagree','Neutral','Slightly Enjoy','Enjoy'],
 'I am good at keeping records of my work':['Strongly Disagree','Slightly Disagree','Neutral','Slightly Enjoy','Enjoy'],
 'I like to lead':['Strongly Disagree','Slightly Disagree','Neutral','Slightly Enjoy','Enjoy'],
 'I like working outdoors':['Strongly Disagree','Slightly Disagree','Neutral','Slightly Enjoy','Enjoy'],
 'I would like to work in an office':['Strongly Disagree','Slightly Disagree','Neutral','Slightly Enjoy','Enjoy'],
 'I’m good at math':['Strongly Disagree','Slightly Disagree','Neutral','Slightly Enjoy','Enjoy'],
 'I like helping people':['Strongly Disagree','Slightly Disagree','Neutral','Slightly Enjoy','Enjoy'],
 'I like to draw':['Strongly Disagree','Slightly Disagree','Neutral','Slightly Enjoy','Enjoy'],
 'I like to give speeches':['Strongly Disagree','Slightly Disagree','Neutral','Slightly Enjoy','Enjoy']

}







@app.route('/') # root page of the webpage
@app.route('/home') # second rout to home page
def home():
    newsapi = NewsApiClient(api_key="28eb525ffe074035a28c9e5b61958737")
    topheadlines  = newsapi.get_top_headlines(sources="al-jazeera-english")
    articles = topheadlines['articles']

    desc = []
    news = []
    img = []
    nurl = []


    for i in range(len(articles)):
        myarticles = articles[i]


        news.append(myarticles['title'])
        desc.append(myarticles['description'])
        img.append(myarticles['urlToImage'])
        nurl.append(myarticles['url'])




    mylist = zip(news, desc, img, nurl)

    return render_template('home.html', context = mylist)  ## passing argument to template

@app.route('/home_departments') # about page of the webpage
def departments():
  with open('.data/Departments.csv') as csv_file:
    data = csv.reader(csv_file, delimiter=',')
    first_line = True
    departments = []
    for row in data:
      if not first_line:
        departments.append({
            "Department": row[0],
            "dep_url": row[1]
            })
      else:
        first_line = False
  return render_template('home_departments.html', title='Departments', departments=departments)

@app.route('/home_course/<departments>') # about page of the webpage
def course(departments):
  with open('.data/course.csv') as csv_file:
    #reader = csv.DictReader(csv_file)
    data = csv.reader(csv_file, delimiter=',')
    first_line = True
    courses = []
    for row in data:
      if not first_line:
        if departments in row[4]:
          courses.append({
            "Sate": row[0],
            "City": row[1],
            "College name": row[2],
            "College URL": row[3],
            "Department": row[4],
            "Cource": row[5],
            "Description": row[6],
            "img_url": row[7]
            })
      else:
        first_line = False
  return render_template('home_course.html', title='Course', courses=courses,departments=departments)

@app.route('/home_course_details/<course>') # course_details page of the webpage
def course_details(course):
  with open('.data/course.csv') as csv_file:
    data = csv.reader(csv_file, delimiter=',')
    first_line = True
    courses = []
    for row in data:
      if not first_line:
        if course in row[5] == course:
          courses.append({
              "Sate": row[0],
              "City": row[1],
              "College name": row[2],
              "College URL": row[3],
              "Department": row[4],
              "Cource": row[5],
              "Description": row[6],
              "img_url": row[7]
              })
      else:
        first_line = False
  return render_template('home_course_details.html', title='Course Detail', courses=courses)

@app.route('/home_news') # about page of the webpage
def news():
    newsapi = NewsApiClient(api_key="28eb525ffe074035a28c9e5b61958737")
    topheadlines  = newsapi.get_everything(sources='al-jazeera-english,the-times-of-india,cnn,the-washington-post',q='education')
    articles = topheadlines ['articles']

    desc = []
    news = []
    img = []
    nurl = []


    for i in range(len(articles)):
        myarticles = articles[i]


        news.append(myarticles['title'])
        desc.append(myarticles['description'])
        img.append(myarticles['urlToImage'])
        nurl.append(myarticles['url'])




    mylist = zip(news, desc, img, nurl)


    return render_template('home_news.html', title='News', context = mylist)

@app.route('/home_community') # about page of the webpage
def community():
    return render_template('home_community.html', title='Community')

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
    return render_template('home_registration.html', title='Register', form=form)


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

    return render_template('home_login.html', title='Login', form=form)


@app.route('/dashboard_main') # about page of the webpage
@login_required
def dashboard_main():
    return render_template('./dashboard_main.html', title='Dashboard')

@app.route('/dashboard_psychoTest') # about page of the webpage
@login_required
def dashboard_psychoTest():
    return render_template('./dashboard_psychoTest.html', title='Dashboard - Psycho Test',questions=questions)

@app.route('/dashboard_academics') # about page of the webpage
@login_required
def dashboard_academics():
    return render_template('./dashboard_academics.html', title='Dashboard - Academics')

@app.route('/dashboard_carrer') # about page of the webpage
@login_required
def dashboard_carrer():
    return render_template('./dashboard_carrer.html', title='Dashboard - Carrer')

@app.route('/dashboard_courses') # about page of the webpage
@login_required
def dashboard_courses():
    return render_template('./dashboard_courses.html', title='Dashboard - courses')



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
