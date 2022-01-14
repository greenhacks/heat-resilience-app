"""Alert script"""
from datetime import date
from model import connect_to_db, User, AlertType, IndividualAlerts
import requests, crud
import json
# import jsonify
import os
from twilio.rest import Client
from pprint import pprint

os.system('source secrets.sh') #runs command line script in console 

# Twilio info:
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']   
client = Client(account_sid, auth_token)

# OpenWeather info:
openweatherkey = os.environ['OPENWEATHER_KEY']

def get_user():
    """Gets users, calls API, alerts users."""

    # retrieve opted-in user location (city) data using SQLAlchemy 
    users = User.query.filter_by(opted_in="Yes").all() # returns a list

    # make a set of all the users' unique cities 
    cities = set()

    for user in users:
        cities.add(user.city) # attribute

    results = dict() # needs to be outside of the city for-loop, or else it will get reset

    # after getting user city data, loop over it and make API call to OpenWeather with the city data retrieved above
    # to get temp and relative humidity for one day (8 timestamps) (https://www.weather.gov/media/unr/heatindex.pdf)
    for city in cities: 
        payload = {'q': city,
                'appid': openweatherkey,
                'units': 'imperial',
                'cnt': 8}

        response = requests.get('http://api.openweathermap.org/data/2.5/forecast?',
                        params=payload)

        weather = response.json() #--> turn JSON response into Python dict

        pprint(weather)

        # extract data returned from API call
        weather_results = weather['list'] # a list of dictionaries

        # print(weather_results)
        
        heat_indexes = []

        # loop over the 40 weather results to get timestamp, temp, and humidity (for each city)
        for i in range(len(weather_results)): 

            # timestamp = weather_results[i].get('dt_txt') #value
            temp = weather_results[i]['main'].get('temp')
            humidity = weather_results[i]['main'].get('humidity')

            # run calculate_heat_index for each timestamp
            heat_index = crud.calculate_heat_index(temp, humidity)
            
            # update heat indexes list - get 8 heat indexes per city
            # heat_indexes.append((heat_index, timestamp)) #--> with timestamp
            heat_indexes.append(heat_index)

        results[city] = max(heat_indexes) #heat_indexes is a list that will be the value (original)
    
    # Twilio API calls: loop over users -  if they are in city, send message
    i = 0
    date_sent = date.today()
    print(date_sent)
                
    for user in users:
        if user.city in results:
            if results[user.city] >= 129: 
                # send message       
                message = client.messages.create(
                        body=AlertType.query.filter_by(temp_range="129.3+").first().alert_text,
                        from_='+18509034729',
                        to=user.phone 
                    )
                print(message.sid) #prints to terminal
                alert = AlertType.query.filter_by(temp_range="129.3+").first()

                individual_alert = crud.create_individual_alert(user.user_id, alert.alert_type_id, date_sent) # create individual alert record
        
            elif results[user.city] >= 106:
                message = client.messages.create(
                        body=AlertType.query.filter_by(temp_range="105.9-129.2").first().alert_text,
                        from_='+18509034729',
                        to=user.phone 
                    )
                print(message.sid)
                alert = AlertType.query.filter_by(temp_range="105.9-129.2").first()
                
                individual_alert = crud.create_individual_alert(user.user_id, alert.alert_type_id, date_sent) # create individual alert record

            elif results[user.city] >= 90:
                message = client.messages.create(
                        body=AlertType.query.filter_by(temp_range="89.7-105.8").first().alert_text,
                        from_='+18509034729',
                        to=user.phone 
                    )
                print(message.sid)
                alert = AlertType.query.filter_by(temp_range="89.7-105.8").first()
                
                individual_alert = crud.create_individual_alert(user.user_id, alert.alert_type_id, date_sent) # create individual alert record

            elif results[user.city] >= 40:
                message = client.messages.create(
                        body=AlertType.query.filter_by(temp_range="78.8-89.6").first().alert_text,
                        from_='+18509034729',
                        to=user.phone # need to replace with a user's number
                    )
                print(message.sid)
                alert = AlertType.query.filter_by(temp_range="89.7-105.8").first()
                
                individual_alert = crud.create_individual_alert(user.user_id, alert.alert_type_id, date_sent) # create individual alert record

            i += 1   
        else:
            return

#2.0 - if the calculated heat index is 20% hotter than the ideal temperature provided, send tailored alert

# Helps execute code
if __name__ == "__main__":
    # DebugToolbarExtension(app)
    from server import app
    connect_to_db(app, 'heat-resilience-app')
    # get_user()
    # app.run(host="0.0.0.0", debug=True) #--> don't need to run app

# schedule the code for every day at 12am
# Every day at 12am or 00:00 time get_user() is called
# schedule.every().day.at("00:00").do(get_user)

# # Loop so that the scheduling task
# # keeps on running all time.
# while True:  
#     # Checks whether a scheduled task 
#     # is pending to run or not
#     schedule.run_pending()
#     time.sleep(1)


