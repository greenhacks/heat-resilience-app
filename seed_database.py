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

fname = 'TestUser1'
# zipcode = f'{n + 90000}'
city = "Los Angeles"
country_code = "US"
phone = phone_num
email = 'user1@test.com'
password = 'test1'
opted_in = True

db_user = crud.create_user(fname, city, country_code, phone, email, password, opted_in) 
    

# create the alert messages
threshold_1 = crud.create_alert("Caution 1", "78.8-89.6")

threshold_2 = crud.create_alert("Caution 2", "89.7-105.8")

threshold_3 = crud.create_alert("Caution 3", "105.9-129.2")

threshold_4 = crud.create_alert("Caution 4", "129.3+")

# create 10 individual alerts for test user
date_str = "22-Dec-2021"
format = "%d-%b-%Y"
date = datetime.strptime(date_str, format)

for n in range(11):
    alert_type_id = 1
    db_test_alerts = crud.create_individual_alert(1, alert_type_id, date)