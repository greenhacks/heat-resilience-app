# heat-resilience-app

This is a full-stack create-read-update-delete (CRUD) app dedicated to improving users' thermal comfort and increasing heat resilience.

## MVP 
Users will be able to:

- Create a profile
- Log in and modify their settings (e.g. opt in or out of notifications)
- Receive automated text message alerts based on heat index (function of air temperature and relative humidity)
- Keep track of how many alerts they have received over time on a Dashboard
- Visit About & Resilience Resources pages

## 2.0
- Refactor with FastAPI for handling async/await, promises

## APIs Required
- OpenWeather API - https://openweathermap.org/api
- Twilio Messaging API - https://www.twilio.com/docs/usage/api#send-an-sms-with-twilios-api

## Tech Stack
- Python,  Flask,  Javascript, HTML, CSS, Chart.js, Bootstrap, PostgreSQL, SQLAlchemy, AJAX, Jinja, Pytest

## How to Start the App
- Clone this repo into your local machine
- Run `virtualenv env` to create a virtual environment on your machine
- Run `source env/bin/activate` to activate the virtual environment
- Run `pip3 install -r requirements.txt`
- Run `source secrets.sh`
- Run `python3 server.py`


## Images
- Homepage: ![homepage](https://github.com/greenhacks/heat-resilience-app/blob/main/static/homepage.png)

- Dashboard Chart: ![chart](https://github.com/greenhacks/heat-resilience-app/blob/main/static/dashboard-chart.png)

- View Settings: ![view-settings](https://github.com/greenhacks/heat-resilience-app/blob/main/static/view-settings.png)

- Update Settings: ![update-settings](https://github.com/greenhacks/heat-resilience-app/blob/main/static/update-settings.png)

- Resilience Resources: ![resilience](https://github.com/greenhacks/heat-resilience-app/blob/main/static/resilience-resources.png)

- Twilio Text Message: ![text-alerts](https://github.com/greenhacks/heat-resilience-app/blob/main/static/text-alert.png)

## System Architecture
- The database has normalized data.