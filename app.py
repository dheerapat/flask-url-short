from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os.path
from werkzeug.utils import secure_filename

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
        #if user click submit button it will check what is the key of the request whether it a url or file
        if 'url' in request.form.keys():
            urls[request.form['code']] = {'url':request.form['url']}
        else:
            f = request.files['file']
            full_name = request.form['code'] + secure_filename(f.filename)
            f.save('/home/dheerapat/Desktop/project/flask-url-short/static/user_file/' + full_name)
            urls[request.form['code']] = {'file':full_name}

        with open('urls.json','w') as url_file:
            json.dump(urls, url_file)
        
        return render_template('your_url.html', code = request.form['code'])
    else:
        return redirect(url_for('home')) # if http request is get request

@app.route('/<string:code>')
def redirect_to_url(code):
    if os.path.exists('urls.json'):
        with open('urls.json') as urls_file:
            urls = json.load(urls_file)
            #look for 'code' key in json file associate in route fn.
            if code in urls.keys():
                #each json key have dictionary as a value so we want to return that dictionary value out
                if 'url' in urls[code].keys():
                    return redirect(urls[code]['url'])
                else:
                    return redirect(url_for('static',filename='user_file/' + urls[code]['file']))