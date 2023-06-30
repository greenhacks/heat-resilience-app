"""CRUD operations."""

from model import db, User, AlertType, IndividualAlerts
from time import strftime


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
    db.session.commit() 

    return individual_alert

def create_user(fname, city, country_code, phone, email, password, opted_in):
    """Create and return a new user."""

    # Standardize input
    fname = str(fname).title()
    city = str(city).title()
    email = str(email).lower()
    password = str(password)

    # instantiate user
    user = User(fname=fname, city=city, country_code=country_code, phone=phone, email=email, 
                password=password, opted_in=opted_in)

    db.session.add(user)
    db.session.commit()

    return user

def get_user_by_email(email):
    """Get a user by email."""

    try:
        user = User.query.filter(User.email == email).one() 
        return user

    except Exception as e:
        print(e)
        print('\n'*10)
        return None

    
def update_settings(user, new_settings_dict):
    """Update a user's settings per user input."""

    for key, value in new_settings_dict.items():
        if value == "None" or value == "" or value == None:
            pass
        else: 
            setattr(user, key, value) 

        db.session.add(user)
        db.session.commit()

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

    total_alerts = IndividualAlerts.query.filter_by(user_id=user.user_id).count() 

    if total_alerts == None:
        return 0

    else:
        return total_alerts

def get_monthly_alerts(email):
    """Gets monthly number of alerts for the current year a user has received."""

    user = get_user_by_email(email)

    new_dict = {}

    months_num = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    monthly_alerts = IndividualAlerts.query.filter_by(user=user).all() 

    for alert in monthly_alerts:    
        interim = alert.date_sent
        month = int(interim.strftime("%m"))
        new_dict[month] = new_dict.get(month, 0) + 1

    for month in months_num:
        if month not in new_dict:
            new_dict[month] = 0

    # returns a list of tuples
    return list(new_dict.items())


if __name__ == "__main__":
    from model import connect_to_db
    from server import app

    connect_to_db(app, "heat-resilience-app")