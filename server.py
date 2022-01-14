"""Server for the app."""
import os

os.system("source secrets.sh") #runs command line script in console 

import crud
import re
import model
import requests
import alert
import datetime
from twilio.rest import Client

from flask import (Flask, render_template, request, flash, session,
                   redirect, json, jsonify)
from model import connect_to_db, User, AlertType, IndividualAlerts, db
from jinja2 import StrictUndefined 

secretkey = os.environ['SECRET_KEY']

app = Flask(__name__)
app.secret_key = secretkey 
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def show_homepage():
    """Show the homepage"""

    return render_template('homepage.html')

@app.route('/dashboard')
def show_dashboard():
    """Show the dashboard"""
    
    user = crud.get_user_by_email(session['user_email'])
    fname = user.fname

    alerts = crud.get_total_alerts(user.email)
    return render_template('dashboard.html', alerts=alerts, fname=fname)

@app.route('/total-alerts')
def get_total_alerts():
    """Get total alerts (count) for each user."""

    user = crud.get_user_by_email(session['user_email'])

    total_alerts = crud.get_total_alerts(user.email)

    return total_alerts

@app.route('/monthly-alerts.json')
def get_monthly_alerts():
    """Get alerts by month for current year."""

    user = crud.get_user_by_email(session['user_email'])

    date = datetime.date.today()

    year = date.year
    
    monthly_alerts = crud.get_monthly_alerts(user.email) #returns list

    alerts_this_month = []
    for date, total in monthly_alerts:
        alerts_this_month.append({'month': date,
                                'alerts': total})

    return jsonify({'data': alerts_this_month})

@app.route('/users', methods=['POST'])
def create_account():
    """Create user account."""

    fname = request.form.get('fname')
    city = request.form.get('city')
    country_code = request.form.get('country_code')
    phone = request.form.get('phone')
    email = request.form.get('email')
    password = request.form.get('password')
    opted_in = request.form.get('optin')

    # convert phone number for Twilio
    if re.search("^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$", phone):
        pass

    else:
        flash('Please input a valid phone number.')
        return False

    # get the user
    user = crud.get_user_by_email(email)

    if user is None:
        user = crud.create_user(fname, city, country_code, phone, email, password, opted_in)
        flash('Your account was created successfully! You can now log in.')

    else:
        flash('That email is already in use! Please try again.')
    
    return redirect("/") 
    
# route that handles login
@app.route('/login', methods=['POST'])
def handle_login():
    """Log user into application."""

    email = request.form.get('loginemail') 
    password = request.form.get('loginpassword')

    # get user by email
    user = crud.get_user_by_email(email)

    if user is None:
        flash('Wrong email or password!')
        return redirect('/')
    
    elif email == user.email and password == user.password:
        session['user_email'] = user.email 
        # flash(f'Logged in as {user.email}!') 
        return redirect('/dashboard')
    
    else:
        flash('Wrong password!')
        return redirect('/')

@app.route('/user-settings')
def get_settings():
    """Get and show a user's settings."""

    # get user and info from the database using sessions
    user = crud.get_user_by_email(session['user_email'])

    fname = user.fname
    lname = user.lname
    email = user.email
    city = user.city
    country_code = user.country_code
    phone = user.phone
    age = user.age
    ideal_temp = user.ideal_temp_f
    opted_in = user.opted_in

    #show info using Jinja template
    return render_template('settings.html', fname=fname, lname=lname, email=email, city=city, 
                            country_code=country_code, phone=phone, age=age,
                            ideal_temp=ideal_temp, opted_in=opted_in)

@app.route('/user-settings-update', methods=['GET','POST'])
def update_user_settings():
    """Update user's settings based on user input."""

    user = crud.get_user_by_email(session['user_email'])

    if request.method == 'POST':
        # get the user - modify the dict
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        city = request.form.get('city')
        country_code = request.form.get('country_code')
        phone = request.form.get('phone')
        age = request.form.get('age')
        ideal_temp_f = request.form.get('idealtemp')
        email = request.form.get('email')
        password = request.form.get('password')
        opted_in = ("Yes" if request.form.get('optin') else "No") #ternary expression

        # standardize data
        fname = fname.title()
        lname = lname.title()
        city = city.title()
        email = email.lower()


        new_settings_dict = {
            'fname': fname,
            'lname': lname,
            'city': city,
            'country_code': country_code,
            'phone': phone,
            'age': age,
            'ideal_temp_f': ideal_temp_f,
            'email': email,
            'password': password,
            'opted_in': opted_in 
        }

        # use the user's email to update settings via crud file
        updated_user = crud.update_settings(user, new_settings_dict)
    
        
        flash('Your settings have been updated!')

        return render_template('update_settings.html', user=updated_user)
    
    else:
        return render_template('update_settings.html', user=user)

@app.route('/reset-password', methods=['GET','POST'])
def reset_password():
    """Resets a password."""
    

    if request.method == 'POST':
        email = request.form.get('resetemail')
        password = request.form.get('resetpassword')

        user = crud.get_user_by_email(email)

        new_password_dict = {
            'password': password
        }

        updated_user = crud.update_settings(user, new_password_dict)

        flash('Your password has been updated!')
        
        return redirect("/")
    
    else:
        return render_template('reset_password.html')

@app.route('/alert')
def click_alert():
    """Gets text alert on click - for demo only."""

    alert.get_user()

    return redirect('/dashboard')

@app.route('/logout')
def logout():
    """Log a user out"""

    del session['user_email']
    
    flash("You have logged out.")
    
    return redirect("/")

@app.route('/resilience-resources')
def show_resilience():
    """Show the Resilience Resources page"""

    return render_template('resources.html')


@app.route('/about')
def show_about():
    """Show the About page"""

    return render_template('about.html')

# Helps execute code
if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app, 'heat-resilience-app')
    # app.run(host="0.0.0.0", debug=True) #removed for prod