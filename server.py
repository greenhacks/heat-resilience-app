"""Server for the app."""
import crud
import model
import os
import requests
import alert
import datetime
from twilio.rest import Client

from flask import (Flask, render_template, request, flash, session,
                   redirect, json, jsonify)
from model import connect_to_db, User, AlertType, IndividualAlerts, db
from jinja2 import StrictUndefined #Add comments

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

    year=date.year
    
    monthly_alerts = crud.get_monthly_alerts(user.email, year)

    return monthly_alerts


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

    email = request.form.get('loginemail') # gets email from form
    password = request.form.get('loginpassword') # gets password from form

    # get user by email
    user = crud.get_user_by_email(email)
    # userpassword = crud.get_user_by_password(password) --> COMMENTED OUT: causes security issues

    if password == user.password:   # password needs to equal the user's password
        session['user_email'] = user.email # couldn't add the entire user object to the session
        flash(f'Logged in as {user.email}') #need to edit to reflect a name, not an email
        return redirect('/dashboard')

    else:
        flash('Wrong password!')
        return redirect('/')

# route that handles settings updates - get settings data
@app.route('/user-settings')
def get_settings():
    """Get and show a user's settings."""
    # print(session['user_email'])
    # print("\n"*20)

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
    
    # print(dir(user))

    if request.method == 'POST':
        # get the user - modify the dict
        new_settings_dict = {
            'fname': request.form.get('fname'),
            'lname': request.form.get('lname'),
            'city': request.form.get('city'),
            'country_code': request.form.get('country'),
            'phone': request.form.get('phone'),
            'age': request.form.get('age'),
            'ideal_temp_f': request.form.get('idealtemp'),
            'email': request.form.get('email'),
            'password': request.form.get('password'),
            'opted_in': request.form.get('optin')
        }
        # use the user's email to update settings via crud file
        updated_user = crud.update_settings(user, new_settings_dict) 

        
        flash('Your settings have been updated!')

        return render_template('update_settings.html', user=updated_user)
    
    else:
        return render_template('update_settings.html', user=user)


# @app.route('/logout')
# def logout():
#     """Log a user out"""

#     del session['user_email']
    
#     flash("You have successfully logged out.")
    
#     return redirect("/")

# route for a user to see their alerts on the dashboard
# @app.route('/dashboard')

# # route for static resilience page - can be accessed through homepage?
# @app.route('/resilience')

# # route for static about page - can be accessed through homepage?
# @app.route('/about')


# Helps execute code
if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app, 'heat-resilience-app')
    app.run(host="0.0.0.0", debug=True)