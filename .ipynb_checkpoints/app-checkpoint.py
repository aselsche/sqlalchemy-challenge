### Step 2 - Climate App
#Now that you have completed your initial analysis, design a Flask API based on the queries that you have just developed.

# 1. Import Flask and other dependencies
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify

# Database setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

#reflect an existing database into a new model
Base = automap_base()

#reflect the tables
Base.prepare(engine, reflect=True)

#Save the reference to the table
Passenger = Base.classes.measurement

#create session link from python to the DB
session=Session(engine)

# Flask setup
app = Flask(__name__)

# Flask routes
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return "Welcome to my 'Home page!"
    links = []
    for rule in app.url_map.iter_rules():
        if len(rule.defaults) >= len(rule.arguments):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append((url, rule.endpoint))
    return render_template("all_links.html", links=links)


# 4. Define main behavior
if __name__ == "__main__":
    app.run(debug=True)
