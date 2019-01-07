#!/usr/bin/env python3

from flask import Flask, render_template, request, redirect, session, flash
import connexion
from models import model


def get_ticker_price(ticker='aapl'):
    return model.apiget(ticker)

# app = connexion.App(__name__, specification_dir='./')

app = Flask(__name__)

# app.add_api('swagger.yml')

app.secret_key = 'the session needs this'

def date_format(datestring):
    date = dateutil.parser.parse(datestring)
    week_day_index = date.weekday()
    clock_time = date.strftime("%H:%M:%S")
    date_string = f"{calendar.day_abbr[week_day_index]} {date.day} {calendar.month_name[date.month]} "+ clock_time
    return date_string
    
# context_processor does not work with connexion
# @app.context_processor
# def context_processor():
#     return dict(date_format = date_format)



@app.route('/', methods=['GET'])
def send_to_login():
        return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():    
    if request.method == 'GET':
        print(session)
        if 'username' in session:
            return render_template('login_logged.html')
        return render_template('login.html')
    else:
        try:
            username = request.form['username']
            password = request.form['password']
            user_object = model.set_user_object(username)
        except:
            flash("Invalid Login")
            return redirect('/login')
        if user_object.check_password(user_object.pass_hash, password):
            session['username'] = username
            flash(f'User {username} successfully logged in!')
            return redirect('/login')
        else:
            flash("Invalid Login")
            return redirect('/login')


if __name__=='__main__':
    app.debug = True
    app.run(port=8080)
    
