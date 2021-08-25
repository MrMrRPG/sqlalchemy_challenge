#Dependencies
from flask import Flask, jsonify
import pandas as pd
import numpy as np
import sqlalchemy
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#Creating engine and reflection
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect = True)

station = Base.classes.station
measurement = Base.classes.measurement

session = Session(engine)

#Set up Flask
app = Flask(__name__)

###########################################################

@app.route("/")
def welcome():
    return (
        f"This is the homepage of the Hawaii Weather Station API!<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
        f"To initialize a search, enter the start and end date between the two slashes as yyyy-mm-dd."
        )

@app.route("/api/v1.0/precipitation")
def prcp():
    session = Session(engine)

    # Calculate the date one year from the last date in data set.
    a_year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # a_year_ago

    # Perform a query to retrieve the data and precipitation scores
    date_prcp = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date >= a_year_ago).\
        order_by(measurement.date).all()

    session.close()

    all_date_prcp = list(np.ravel(date_prcp))

    return jsonify(all_date_prcp)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    
    # Perform a query to retrieve the data and precipitation scores
    stations = session.query(station.station, station.name).all()

    session.close()

    all_stations = list(np.ravel(stations))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    
    # Perform a query to retrieve the data and precipitation scores
    tobs = session.query(func.min(measurement.tobs), 
            func.max(measurement.tobs), 
            func.avg(measurement.tobs), 
            func.count(measurement.tobs)).\
            filter(measurement.station == "USC00519281").\
            all()

    session.close()

    all_tobs = list(np.ravel(tobs))

    return jsonify(all_tobs)

@app.route("/api/v1.0/<start>")
def start_date(start):

    start_date = session.query(func.min(measurement.tobs), 
            func.max(measurement.tobs), 
            func.avg(measurement.tobs), 
            func.count(measurement.tobs)).\
            filter(measurement.date >= start).\
            all()
    
    session.close

    start_date_ravel = list(np.ravel(start_date))

    return jsonify(start_date_ravel)

@app.route("/api/v1.0/<start>/<end>")
def end_date(start, end):

    end_date = session.query(func.min(measurement.tobs), 
            func.max(measurement.tobs), 
            func.avg(measurement.tobs), 
            func.count(measurement.tobs)).\
            filter(measurement.date >= start).\
            filter(measurement.date <= end).\
            all()
    
    session.close

    end_date_ravel = list(np.ravel(end_date))

    return jsonify(end_date_ravel)


if __name__ == "__main__":
	app.run(debug=True)