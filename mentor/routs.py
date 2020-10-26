
from flask import render_template, url_for, flash, redirect, request
from mentor import app, db, bcrypt
from mentor.form import RegistrationForm, LoginForm, UpdateAccountForm
from mentor.models import User
from flask_login import login_user, current_user, logout_user, login_required
import csv
from newsapi import NewsApiClient
import pandas as pd
import chardet
#Choosing the maximum 3 Codes
from operator import itemgetter as it
from itertools import repeat
from similarity.cosine import Cosine
import json


questions = {
 #Format is 'question':[options]
 #'Ma\'an
 'I like to work on cars':['Strongly Disagree','Slightly Disagree','Neutral','Slightly Enjoy','Enjoy'],
 'I like to do puzzles':['Strongly Disagree','Slightly Disagree','Neutral','Slightly Enjoy','Enjoy'],
 'I am good at working independently':['Strongly Disagree','Slightly Disagree','Neutral','Slightly Enjoy','Enjoy'],
 'I like to work in teams':['Strongly Disagree','Slightly Disagree','Neutral','Slightly Enjoy','Enjoy'],
 'I am an ambitious person who set goals for myself':['Strongly Disagree','Slightly Disagree','Neutral','Slightly Enjoy','Enjoy'],
 'I like to organize things':['Strongly Disagree','Slightly Disagree','Neutral','Slightly Enjoy','Enjoy'],
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
 'I like working with numbers  or charts':['Strongly Disagree','Slightly Disagree','Neutral','Slightly Enjoy','Enjoy'],
 'I like to get into discussions about issues around me':['Strongly Disagree','Slightly Disagree','Neutral','Slightly Enjoy','Enjoy'],
 'I am good at keeping records of my work':['Strongly Disagree','Slightly Disagree','Neutral','Slightly Enjoy','Enjoy'],
 'I like to lead':['Strongly Disagree','Slightly Disagree','Neutral','Slightly Enjoy','Enjoy'],
 'I like working outdoors':['Strongly Disagree','Slightly Disagree','Neutral','Slightly Enjoy','Enjoy'],
 'I would like to work in an office':['Strongly Disagree','Slightly Disagree','Neutral','Slightly Enjoy','Enjoy'],
 'I am good at math':['Strongly Disagree','Slightly Disagree','Neutral','Slightly Enjoy','Enjoy'],
 'I like helping people':['Strongly Disagree','Slightly Disagree','Neutral','Slightly Enjoy','Enjoy'],
 'I like to draw':['Strongly Disagree','Slightly Disagree','Neutral','Slightly Enjoy','Enjoy'],
 'I like to give speeches':['Strongly Disagree','Slightly Disagree','Neutral','Slightly Enjoy','Enjoy'],
 'I like selling things':['Strongly Disagree','Slightly Disagree','Neutral','Slightly Enjoy','Enjoy']

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
            "State": row[0],
              "City": row[1],
              "College_name": row[2],
              "College_URL": row[3],
              "Department": row[4],
              "Course_short": row[5],
              "Course_full": row[6],
              "Description": row[7],
              "Course_url": row[8],
              "img_url": row[9],
              "related_jobs": row[10]
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
              "State": row[0],
              "City": row[1],
              "College_name": row[2],
              "College_URL": row[3],
              "Department": row[4],
              "Course_short": row[5],
              "Course_full": row[6],
              "Description": row[7],
              "Course_url": row[8],
              "img_url": row[9],
              "related_jobs": row[10]
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

@app.route('/dashboard_psychoTest', methods=['GET', 'POST']) # about page of the webpage
@login_required
def dashboard_psychoTest():
  # This is to make sure the HTTP method is POST and not any other
    if request.method == 'POST':
      q1=[]
      for i in questions:
        q1.append(request.form[i])
        continue


      with open('.data/test.csv','w') as inFile:
        fieldnames = ['I like to work on cars',
        'I like to do puzzles',
        'I am good at working independently',
        'I like to work in teams',
        'I am an ambitious person who set goals for myself',
        'I like to organize things',
        'I like to build things',
        'I like to read about art and music',
        'I like to have clear instructions to follow',
        'I like to try to influence or persuade people',
        'I like to do experiments',
        'I like to teach or train people',
        'I like trying to help people solve their problems',
        'I like to take care of animals',
        'I wouldn’t mind working 8 hours per day in an office',
        'I enjoy creative writing',
        'I enjoy science',
        'I am quick to take on new responsibilities',
        'I am interested in healing people',
        'I enjoy trying to figure out how things work',
        'I like putting things together or assembling things',
        'I am a creative person',
        'I pay attention to details',
        'I like to do filing or typing',
        'I like to analyze things (problems/situations)',
        'I like to play instruments or sing',
        'I enjoy learning about other cultures',
        'I would like to start my own business',
        'I like to cook',
        'I like acting in plays',
        'I am a practical person',
        'I like working with numbers  or charts',
        'I like to get into discussions about issues around me',
        'I am good at keeping records of my work',
        'I like to lead',
        'I like working outdoors',
        'I would like to work in an office',
        'I am good at math',
        'I like helping people',
        'I like to draw',
        'I like to give speeches',
        'I like selling things']

        writer = csv.DictWriter(inFile, fieldnames=fieldnames)
        writer.writeheader()
        #writerow() will write a row in your csv file
        writer.writerow({'I like to work on cars': q1[0],
        'I like to do puzzles': q1[1],
        'I am good at working independently': q1[2],
        'I like to work in teams': q1[3],
        'I am an ambitious person who set goals for myself': q1[4],
        'I like to organize things': q1[5],
        'I like to build things': q1[6],
        'I like to read about art and music': q1[7],
        'I like to have clear instructions to follow': q1[8],
        'I like to try to influence or persuade people': q1[9],
        'I like to do experiments': q1[10],
        'I like to teach or train people': q1[11],
        'I like trying to help people solve their problems': q1[12],
        'I like to take care of animals': q1[13],
        'I wouldn’t mind working 8 hours per day in an office': q1[14],
        'I enjoy creative writing': q1[15],
        'I enjoy science': q1[16],
        'I am quick to take on new responsibilities': q1[17],
        'I am interested in healing people': q1[18],
        'I enjoy trying to figure out how things work': q1[19],
        'I like putting things together or assembling things': q1[20],
        'I am a creative person': q1[21],
        'I pay attention to details': q1[22],
        'I like to do filing or typing': q1[23],
        'I like to analyze things (problems/situations)': q1[24],
        'I like to play instruments or sing': q1[25],
        'I enjoy learning about other cultures': q1[26],
        'I would like to start my own business': q1[27],
        'I like to cook': q1[28],
        'I like acting in plays': q1[29],
        'I am a practical person': q1[30],
        'I like working with numbers  or charts': q1[31],
        'I like to get into discussions about issues around me': q1[32],
        'I am good at keeping records of my work': q1[33],
        'I like to lead': q1[34],
        'I like working outdoors': q1[35],
        'I would like to work in an office': q1[36],
        'I am good at math': q1[37],
        'I like helping people': q1[38],
        'I like to draw': q1[39],
        'I like to give speeches': q1[40],
        'I like selling things':q1[41]
         })
    return render_template('./dashboard_psychoTest.html', title='Dashboard - Psycho Test',questions=questions)

@app.route('/dashboard_academics') # about page of the webpage
@login_required
def dashboard_academics():
    return render_template('./dashboard_academics.html', title='Dashboard - Academics')

@app.route('/dashboard_carrer', methods=['GET', 'POST']) # about page of the webpage
@login_required
def dashboard_carrer():

  with open('.data/test.csv', 'rb') as f:
      result = chardet.detect(f.read())

  p_test = pd.read_csv(".data/test.csv",encoding =result['encoding'])
  #Encoding
  p_test=p_test.replace('Enjoy',5)
  p_test=p_test.replace('Slightly Enjoy',4)
  p_test=p_test.replace('Neutral',3)
  p_test=p_test.replace('Slightly Disagree',2)
  p_test=p_test.replace('Strongly Disagree',1)

  #Realistic Questions
  realistic = p_test[['I like to work on cars','I like to build things','I like to take care of animals','I like putting things together or assembling things','I like to cook','I am a practical person','I like working outdoors']]
  #Investigative Questions
  investigative = p_test[['I like to do puzzles','I like to do experiments','I enjoy science','I enjoy trying to figure out how things work','I like to analyze things (problems/situations)','I like working with numbers  or charts','I am good at math']]
  #Artistic Questions
  artistic = p_test[['I am good at working independently','I like to read about art and music','I enjoy creative writing','I am a creative person','I like to play instruments or sing','I like acting in plays','I like to draw']]
  #Social Questions
  social = p_test[['I like to work in teams','I like to teach or train people','I like trying to help people solve their problems','I am interested in healing people','I enjoy learning about other cultures','I like to get into discussions about issues around me','I like helping people']]
  #Enterprising Questions
  enterprising = p_test[['I am an ambitious person who set goals for myself','I like to try to influence or persuade people','I like selling things','I am quick to take on new responsibilities','I would like to start my own business','I like to give speeches','I like to lead']]
  #Conventional Questions
  conventional = p_test[['I like to organize things','I wouldn’t mind working 8 hours per day in an office','I pay attention to details','I like to do filing or typing','I am good at keeping records of my work','I would like to work in an office']]

  #Summing Up
  realistic['R'] = realistic.sum(axis=1)
  investigative['I']=investigative.sum(axis=1)
  artistic['A']=artistic.sum(axis=1)
  social['S']=social.sum(axis=1)
  enterprising['E']=enterprising.sum(axis=1)
  conventional['C']=conventional.sum(axis=1)

  code= realistic['R']
  code = code.to_frame()
  code['I']=investigative['I']
  code['A']=artistic['A']
  code['S']=social['S']
  code['E']=enterprising['E']
  code['C']=conventional['C']

  n = 3

  new_d = [list(map(it(0),(row[1:].sort_values(ascending=False)[:n].iteritems())))for _, row in code.iterrows()]

  std = pd.DataFrame(new_d)

  std['code']=std[0]+std[1]+std[2]

  #std has the test code
  std = std.drop([0,1,2],axis=1)


  #Read the course data
  course = pd.read_csv(".data/course.csv")

  df = pd.MultiIndex.from_product(
    [std["code"], course["course_code"], course["Course_short"]], names=["code", "course_code","course"]).to_frame(index=False)

  df = df.dropna()

  #Cosine Similarity
  cosine = Cosine(2)
  df["p0"] = df["code"].apply(lambda s: cosine.get_profile(s))
  df["p1"] = df["course_code"].apply(lambda s: cosine.get_profile(s))
  df["cosine_sim"] = [cosine.similarity_profiles(p0,p1) for p0,p1 in zip(df["p0"],df["p1"])]
  df.drop(["p0", "p1"], axis=1,inplace=True)

  #Sorting the Values
  top_n = df.sort_values(['cosine_sim'],ascending=False).groupby(df['code'].values).head(3)

  options = top_n["course"].to_numpy()

  # selecting rows based on condition
  rec = course.loc[course['Course_short'].isin(options)]

  recommendations = json.loads(rec.to_json(orient='records'))

  return render_template('./dashboard_carrer.html', title='Dashboard - Carrer',std=std,recommendations=recommendations)

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
