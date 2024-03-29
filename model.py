"""Models for heat resilience app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_to_db(app, db_name):
    """Connect to database."""

    app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql:///{db_name}"
    app.config["SQLALCHEMY_ECHO"] = True
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = app
    db.init_app(app)
    app.app_context().push()

    with app.app_context(): 
        db.create_all()

class User(db.Model):
    """A user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    fname = db.Column(db.String(25), nullable=False)
    lname = db.Column(db.String(25))
    city = db.Column(db.String(50), nullable=False)
    country_code = db.Column(db.String(30), nullable=False)
    phone = db.Column(db.String(15), nullable=False) 
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer)
    ideal_temp_f = db.Column(db.Integer) 
    opted_in = db.Column(db.String)

    indiv_alerts = db.relationship("IndividualAlerts", back_populates="user")  

    def __repr__(self):
        return f'<User user_id={self.user_id} email={self.email}>'

class AlertType(db.Model):
    """An alert."""

    __tablename__ = "alerttype"

    alert_type_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    alert_text = db.Column(db.String(200))
    temp_range = db.Column(db.String(12))

    indiv_alerts = db.relationship("IndividualAlerts", back_populates="alert_type")


    def __repr__(self):
        return f'<Alert type: alert_type_id={self.alert_type_id}, temp_range={self.temp_range}>'


class IndividualAlerts(db.Model):
    """An individual alert."""

    __tablename__ = "individualalerts"

    indiv_alert_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    alert_type_id = db.Column(db.Integer, db.ForeignKey("alerttype.alert_type_id"), nullable=False)
    date_sent = db.Column(db.DateTime)

    user = db.relationship("User", back_populates="indiv_alerts")
    alert_type = db.relationship("AlertType", back_populates="indiv_alerts")  

    def __repr__(self):
        return f'<Indiv alert: indiv_alert_id={self.indiv_alert_id}, user_id={self.user_id}, date_sent={self.date_sent}>'


if __name__ == "__main__":
    from server import app
    app.app_context()
    connect_to_db(app, "heat-resilience-app")