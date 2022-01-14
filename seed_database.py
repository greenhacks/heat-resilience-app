""""Automatically populates the database sample data and alert texts"""

import os
import json
from random import choice, randint
from datetime import datetime

import crud
from model import connect_to_db, db
import server

phone_num = os.environ['PHONE_NUMBER']

# executes command line code in console
os.system('dropdb heat-resilience-app')
os.system('createdb heat-resilience-app')

# connects to the database 
connect_to_db(server.app, 'heat-resilience-app')

# creates tables
db.create_all()

# sample_cities = ['Los Angeles', 'Seattle', 'Miami', 'Houston', 'Raleigh', 'Little Rock', 'Philadelphia', 'Chicago', 'Tucson', 'Nashville']

# creates users based on sample_cities
# n = 0
# for city in sample_cities:
#     fname = f'TestUser {n + 1}'
#     # zipcode = f'{n + 90000}'
#     city = sample_cities[n]
#     country_code = "US"
#     phone = '+16616076032'
#     email = f'user{n + 1}@test.com'  
#     password = f'test{n + 1}'
#     opted_in = True
#     n += 1

# creates 10 fake users - loops; change 
# for n in range(10):
#     fname = f'TestUser {n + 1}'
#     # zipcode = f'{n + 90000}'
#     city = "Los Angeles"
#     country_code = "US"
#     phone = '+16616076032'
#     email = f'user{n + 1}@test.com'  
#     password = f'test{n + 1}'
#     opted_in = True

    # create a user here
    #db_user = crud.create_user(fname, city, country_code, phone, email, password, opted_in) 

# creates 10 fake users - loops; change 
# for n in range(6):
#     fname = f'User {n + 1}'
#     # zipcode = f'{n + 90000}'
#     city = "Los Angeles"
#     country_code = "US"
#     phone = phone_num
#     email = f'user{n + 1}@test.com'  
#     password = f'test{n + 1}'
#     opted_in = "Yes"

#     db_user = crud.create_user(fname, city, country_code, phone, email, password, opted_in) 

fname = "User1"
# zipcode = f'{n + 90000}'
city = "Los Angeles"
country_code = "US"
phone = phone_num
email = 'user1@test.com'
password = 'test1'
opted_in = 'Yes'

db_user = crud.create_user(fname, city, country_code, phone, email, password, opted_in) 
    
msg_1 = """Caution. The heat index may fall between 80-90 degrees (F). Fatigue is possible with prolonged exposure and/or physical activity."""

msg_2 = """Extreme caution. The heat index may fall between 90-106 degrees (F). Heat stroke, heat cramps, or heat exhaustion possible with prolonged exposure and/or physical activity."""

msg_3 = """Danger. The heat index may fall between 106 to 129 degrees (F). Heat cramps or heat exhaustion likely. Heat stroke possible with prolonged exposure and/or physical activity. Run your AC."""

msg_4 = """Extreme danger. The heat index may be above 129 degrees (F). Heat stroke likely. Run your AC."""

# create the alert messages
threshold_1 = crud.create_alert(msg_1, "78.8-89.6")

threshold_2 = crud.create_alert(msg_2, "89.7-105.8")

threshold_3 = crud.create_alert(msg_3, "105.9-129.2")

threshold_4 = crud.create_alert(msg_4, "129.3+")

# create test individual alerts for test user
format = "%d-%b-%Y"

for _ in range(12):
    date_str1 = "12-Mar-2021"
    date1 = datetime.strptime(date_str1, format)
    alert_type_id = 1
    db_test_alerts = crud.create_individual_alert(1, alert_type_id, date1)

for _ in range(25):
    date_str2 = "11-May-2021"
    date2 = datetime.strptime(date_str2, format)
    alert_type_id = 2
    db_test_alerts = crud.create_individual_alert(1, alert_type_id, date2)

for _ in range(30):
    date_str2 = "11-Jul-2021"
    date2 = datetime.strptime(date_str2, format)
    alert_type_id = 3
    db_test_alerts = crud.create_individual_alert(1, alert_type_id, date2)

for _ in range(30):
    date_str3 = "01-Aug-2021"
    date3 = datetime.strptime(date_str3, format)
    alert_type_id = 3
    db_test_alerts = crud.create_individual_alert(1, alert_type_id, date3)

for _ in range(5):
    date_str4 = "11-Dec-2021"
    date4 = datetime.strptime(date_str4, format)
    alert_type_id = 1
    db_test_alerts = crud.create_individual_alert(1, alert_type_id, date4)
