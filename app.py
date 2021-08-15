### Step 2 - Climate App
#Now that you have completed your initial analysis, design a Flask API based on the queries that you have just developed.

# 1. Import Flask and other dependencies
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify, url_for, render_template

# Database setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

#reflect an existing database into a new model
Base = automap_base()

#reflect the tables
Base.prepare(engine, reflect=True)

#Save the reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# using value throughout the API
QUERY_DATE = dt.date(2017, 8, 23) - dt.timedelta(days=365)

# Flask setup
app = Flask(__name__)

# Flask routes
@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Welcome to Climate App APIs! <br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;"
    )

@app.route("/api/v1/precipitation")
def precipitation():
    #create session link from python to the DB
    session=Session(engine)
    
    # Return a list of prcp measurements by date
    # Query all prcp
    lst = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= QUERY_DATE).\
        group_by(Measurement.date).all()
    
    # convert the results to a dictionary
    prcp_dict = {}
    for result in lst:
        prcp_dict[result[0]] = result[1]

    # close session so it doesn't hog resources
    session.close()

    return jsonify(prcp_dict)

@app.route("/api/v1/stations")
def stations():
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    #create session link from python to the DB
    session=Session(engine)
    
    # Return a list of all station names
    stations = [
            {
                "station": station.station,
                "name": station.name,
                "latitude": station.latitude,
                "longitude": station.longitude,
                "elevation": station.elevation
        
            } for station in session.query(Station).all()
        ]

    session.close()

    return jsonify(stations)

@app.route("/api/v1/tobs")
def tobs():
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    #create session link from python to the DB
    session=Session(engine)
    
    # find most active station by number of rows
    station = session.query(Measurement.station).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.station).desc()).first()

    tobs = session.query(Measurement.date, Measurement.tobs).\
        filter(
            Measurement.station == station.station,
            Measurement.date >= QUERY_DATE
        ).\
        all()

    # convert the results to a dictionary
    tobs_dict = {}
    for result in tobs:
        tobs_dict[result[0]] = result[1]    

    # convert to dict so it can be serialized
    station_dict = {
        "station": station.station,
        "tobs": tobs_dict
    }

    # most_active_stations
    # lst = session.query(Measurement.date, Measurement.prcp).\
    #     filter(Measurement.date >= QUERY_DATE).\
    #     group_by(Measurement.date).all()

    session.close()

    return jsonify(station_dict)

# This function called `calc_temps` will accept start date and end date in the format '%Y-%m-%d' 
# and return the minimum, average, and maximum temperatures for that range of dates
# reusing calc_temps from jupyter notebook exercise
def calc_temps(start_date, end_date=None):
    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """
    #create session link from python to the DB
    session=Session(engine)
    
    # intermediate query as we will add another filter if
    # end date was passed
    int_qry = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date)
    
    # if end_date is truthy then compare add filter
    if end_date:
        int_qry = int_qry.filter(Measurement.date <= end_date)
            
    # run the query after adding second conditional filter
    results = int_qry.first()
    
    session.close()

    # return results to calling route
    return results

@app.route("/api/v1/<start>")
@app.route("/api/v1/<start>/<end>")
def main(start, end=None):
    # see calc_temps function for most logic
    # assigning from results tuple there
    [tmin, tave, tmax] = calc_temps(start, end)
    # building json response from above variables
    return jsonify({
        "tmin": tmin,
        "tave": tave,
        "tmax": tmax
    })

# 4. Define main behavior
if __name__ == "__main__":
    app.run(debug=True)
