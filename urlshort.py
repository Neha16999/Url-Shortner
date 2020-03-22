from flask import Flask     #importing the class Flask from flask lib
from flask import render_template, request     #importing the method render_template from flask lib
from flask import redirect, url_for, flash, abort, session, jsonify
import json
import os.path

app = Flask(__name__)        #creating instance of class flask
app.secret_key='abarakadabra'


@app.route('/')     #route to homepage
def index():         #this function will trigger when route is called
    return render_template('index.html',codes=session.keys())

@app.route('/your-url', methods = ['GET','POST'])     #route to about page
def your_url():         #this function will trigger when about is called
    if request.method == 'POST':
        urls={}     #creating an empty dictionary
        if os.path.exists('urls.json'):
            with open ('urls.json') as urls_file:
                urls=json.load(urls_file)
        if request.form['code'] in urls.keys():     #if the code already exists it will be redirected to indexpage
            flash('The short name has already been taken. Please use another name')
            return redirect(url_for('index'))

        urls[request.form['code']]={'url':request.form['url']}      #saving the url in the dictionary
        with open('urls.json','w') as url_file :
            json.dump(urls,url_file)
            session[request.form['code']]=True
        return render_template('your_url.html',code=request.form['code'])   #this takes value of var code and from the form and sends it to display on the page
    else:
        return redirect(url_for('index'))

@app.route('/<string:code>')        #string var stores the value of code to which we can redirect
def redirect_to_url(code):
    if os.path.exists('urls.json'):
            with open ('urls.json') as urls_file:
                urls=json.load(urls_file)
                if code in urls.keys(): 
                    if 'url' in urls[code].keys():
                        return redirect(urls[code]['url'])
    return abort(404)                   

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'),404


@app.route('/api')
def session_api():
    return jsonify(list(session.keys()))