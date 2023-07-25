"""Alert script"""
from datetime import date
from model import connect_to_db, User, AlertType, IndividualAlerts
import requests, crud
import json
# import jsonify
import os
import twilio
from twilio.rest import Client
from pprint import pprint

os.system("source secrets.sh")


account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']   
client = Client(account_sid, auth_token)
twilio_phone_number = os.environ['TWILIO_PHONE_NUMBER']
openweatherkey = os.environ['OPENWEATHER_KEY']

def get_user():
    """Gets users, calls API, alerts users."""

    # retrieve opted-in user location (city) data using SQLAlchemy 
    users = User.query.filter_by(opted_in="Yes").all() 

    # a set of all the users' unique cities 
    cities = set()

    for user in users:
        cities.add(user.city)

    results = dict() 

    for city in cities: 
        payload = {'q': city,
                'appid': openweatherkey,
                'units': 'imperial',
                'cnt': 8}

        response = requests.get('http://api.openweathermap.org/data/2.5/forecast?',
                        params=payload)

        weather = response.json()

        pprint(weather)

        # extract data returned from API call
        weather_results = weather['list']
        
        heat_indexes = []

        # loop over the 40 weather results to get timestamp, temp, and humidity (for each city)
        for i in range(len(weather_results)): 
            temp = weather_results[i]['main'].get('temp')
            humidity = weather_results[i]['main'].get('humidity')
            heat_index = crud.calculate_heat_index(temp, humidity) # run calculate_heat_index for each timestamp
            heat_indexes.append(heat_index)

        results[city] = max(heat_indexes)
    
    # Twilio API calls: loop over users -  if they are in city, send message
    i = 0
    date_sent = date.today()
    print(date_sent)
                
    for user in users:
        if user.city in results:
            if results[user.city] >= 40: 
                message = client.messages.create(
                        body=AlertType.query.filter_by(temp_range="129.3+").first().alert_text,
                        from_=twilio_phone_number,
                        to=user.phone 
                    )
                print(message.sid)
                alert = AlertType.query.filter_by(temp_range="129.3+").first()

                individual_alert = crud.create_individual_alert(user.user_id, alert.alert_type_id, date_sent) # create individual alert record
        
            elif results[user.city] >= 30:
                message = client.messages.create(
                        body=AlertType.query.filter_by(temp_range="105.9-129.2").first().alert_text,
                        from_=twilio_phone_number,
                        to=user.phone 
                    )
                print(message.sid)
                alert = AlertType.query.filter_by(temp_range="105.9-129.2").first()
                
                individual_alert = crud.create_individual_alert(user.user_id, alert.alert_type_id, date_sent) # create individual alert record

            elif results[user.city] >= 20:
                message = client.messages.create(
                        body=AlertType.query.filter_by(temp_range="89.7-105.8").first().alert_text,
                        from_=twilio_phone_number,
                        to=user.phone 
                    )
                print(message.sid)
                alert = AlertType.query.filter_by(temp_range="89.7-105.8").first()
                
                individual_alert = crud.create_individual_alert(user.user_id, alert.alert_type_id, date_sent) # create individual alert record

            elif results[user.city] >= 10:
                message = client.messages.create(
                        body=AlertType.query.filter_by(temp_range="78.8-89.6").first().alert_text,
                        from_=twilio_phone_number,
                        to=user.phone
                    )
                print(message.sid)
                alert = AlertType.query.filter_by(temp_range="89.7-105.8").first()
                
                individual_alert = crud.create_individual_alert(user.user_id, alert.alert_type_id, date_sent) # create individual alert record

            i += 1   
        else:
            return

if __name__ == "__main__":
    # DebugToolbarExtension(app)
    from server import app
    connect_to_db(app, 'heat-resilience-app')
    get_user()

