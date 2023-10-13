

from flask import Flask, render_template, request, redirect, url_for, session,make_response
from pymongo import MongoClient
import re
import time
app = Flask(__name__,static_url_path='/static')
 
 
app.secret_key = 'your secret key'
 
client = MongoClient('mongodb://localhost:27017/')
db=client['geeklogin']
collection = db["ram"]

@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        account=db.accounts.find_one({'username':username,'password':password})
        if account:
            session['loggedin'] = True
            session['id'] = str(account['_id'])
            session['username'] = account['username']
            msg = 'Logged in successfully !'
            return render_template('indexab.html', msg = msg)
        else:
            msg = 'Incorrect username / password !'
    
    elif 'loggedin' in session:
        return redirect(url_for('view_ideas'))
    return render_template('login.html', msg = msg)
 
@app.route('/logining')
def logining():
    return render_template('login.html')
@app.route('/loger1')
def loger1():
    return render_template('hom1.html')

@app.route('/loger2')
def loger2():
    return render_template('hom2.html')

@app.route('/loger3')
def loger3():
    return render_template('hom3.html')
@app.route('/loger5')
def loger5():
    return render_template('register.html')
    

@app.route('/loger4', methods =['GET', 'POST'])
def loger4():
    return render_template('index.html')

@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        account = db.accounts.find_one({'username':username}) 
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            db.accounts.insert_one({'username':username,'password':password,'email':email})
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)



@app.route('/submit_idea', methods=['GET','POST'])
def submit_idea():
    if 'loggedin' in session:
        if request.method == 'POST' and 'idea_title' in request.form and 'idea_description' in request.form and 'idea_file' in request.files:
            idea_title = request.form['idea_title']
            idea_description = request.form['idea_description']
            idea_file = request.files['idea_file']

            # Save the file to the database along with the idea data
            file_data = idea_file.read()
            idea_document={
                'username': session['username'],
                'title': idea_title,
                'description': idea_description,
                'file_data': file_data
            }
            db.ideas.insert_one(idea_document)

            return redirect(url_for('view_ideas'))
        return render_template('my.html')
    return redirect(url_for('login'))



@app.route('/view_ideas',methods=['GET'])
def view_ideas():
    if 'loggedin' in session:
        # Retrieve the user's posted ideas
        user_ideas = db.ideas.find({'username': session['username']})

        return render_template('view_ideas.html', ideas=user_ideas)

    return redirect(url_for('login'))


@app.route('/', methods=["GET", "POST"])
def man():
    if request.method == "POST":
        search_query = request.form.get("search_query")
        # Perform a query to find relevant topics based on the search_query
        # You can customize this query based on your data schema and requirements.
        results = collection.find({"topic1": search_query})
        topics = list(results)
        return render_template('index.html', topics=topics)

    return render_template("index.html", topics=[])
    

if __name__ == '__main__':
    app.debug=True
    app.run()
    app.run(debug=True)
