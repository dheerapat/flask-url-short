from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os.path

app = Flask(__name__)
app.secret_key = 'secretyouonlyknow' # because we have to sent message in the app

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/your-url', methods=['GET','POST'])
def your_url():
    if request.method == 'POST': # if http request is post request
        urls = {}
        # check if file urls.json exist in the app
        if os.path.exists('urls.json'):
            with open('urls.json') as urls_file:
                urls = json.load(urls_file)
        #check if input name 'code' is a urls dict key
        if request.form['code'] in urls.keys():
            flash('already taken, select another name')
            return redirect(url_for('home'))

        urls[request.form['code']] = {'url':request.form['url']}

        with open('urls.json','w') as url_file:
            json.dump(urls, url_file)
        
        return render_template('your_url.html', code = request.form['code'])
    else:
        return redirect(url_for('home')) # if http request is get request