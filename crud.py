"""CRUD operations."""

from model import db, User, AlertType, IndividualAlerts
import server
import requests
import twilio
from flask import (session, request)


def create_alert(alert_text, temp_range):
    """Create the four alerts for the database."""

    alert = AlertType(alert_text=alert_text, temp_range=temp_range)

    db.session.add(alert)
    db.session.commit()

    return alert

def create_individual_alert(user_id, alert_type_id, date_sent):
    """Create the individual instance of the alert"""
    individual_alert = IndividualAlerts(user_id=user_id, alert_type_id=alert_type_id, date_sent=date_sent)

    db.session.add(individual_alert)
    db.session.commit() #persists data

    return individual_alert

def create_user(fname, city, country_code, phone, email, password, opted_in):
    """Create and return a new user."""

    user = User(fname=fname, city=city, country_code=country_code, phone=phone, email=email, 
                password=password, opted_in=opted_in)

    db.session.add(user)
    db.session.commit() #persists data

    return user

def get_user_by_email(email):
    """Get a user by email."""
    
    # query the User table in the database w/ SQLAlchemy to get the first email
    user = User.query.filter(User.email == email).one() #needs to be .one because we want a unique user
   
    return user # user will be either the user or None
    
def update_settings(user, new_settings_dict):
    """Update a user's settings per user input."""

    # for every key and values in the dictionary
    for key, value in new_settings_dict.items():
        if value == "None":
            pass
        elif value != "" or value != "None": # if the value is not an empty string or None
            setattr(user, key, value) #as long as the key in the dict matches the attribute
                # in the model, the attribute will be updated to the value

        db.session.add(user)
        db.session.commit() # persist data

    return user

def calculate_heat_index(temperature, humidity):
    """Calculates heat index.
    This function takes in temperature (F) and relative humidity (%). See the
    equation given here: https://www.wpc.ncep.noaa.gov/html/heatindex_equation.shtml"""
    humidity = humidity/100

    heat_index = (-42.379 + (2.04901523*temperature) + (10.14333127*humidity) - (0.22475541*temperature*humidity) - 
    (0.00683783*temperature*temperature) - (0.05481717*humidity*humidity) + 
    (0.00122874*temperature*temperature*humidity) + 
    (0.00085282*temperature*humidity*humidity) - (0.00000199*temperature*temperature*humidity*humidity))

    return int(heat_index)

def get_total_alerts(email):
    """Gets total number of alerts a user has received"""
    user = get_user_by_email(email)

    total_alerts = IndividualAlerts.query.filter_by(user_id=user.user_id).count() #SQLAlchemy 

    if total_alerts == None:
        return 0

    else:
        return total_alerts

# Helps execute code
if __name__ == "__main__":
    from model import connect_to_db
    from server import app

    connect_to_db(app, "heat-resilience-app")