# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Station = Base.classes.station
Measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available API routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/Precipitation<br/>"
        f"/api/v1.0/Stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/custom<br/>"
    )
@app.route("/api/v1.0/Precipitation")
def Precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Retrieve only the last 12 months of data"""
    # Query precipitation data
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date > "2016-08-23").all()

    session.close()

    # Convert list of tuples into normal list
    date_results = [station[0] for station in results]
    precip_results = [station[1] for station in results]

    return jsonify(date_results,precip_results)

@app.route("/api/v1.0/Stations")
def station():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Retrieve list of stations"""
    # Query stations data
    active_stations = session.query(Station.station).all()

    session.close()

    station_list = [station[0] for station in active_stations]

    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Retrieve dates and temperatures observations of the most active station"""
    # Query precipitation data
    
    most_active_station_id  = session.query(Measurement.station).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).first()[0]
    
    temperature_stats = session.query(
        func.min(Measurement.tobs).label('min_temp'),
        func.max(Measurement.tobs).label('max_temp'),
        func.avg(Measurement.tobs).label('avg_temp')
        ).filter(Measurement.station == most_active_station_id).all()

    session.close()

    min_temp = [measurement[0] for measurement in temperature_stats]
    max_temp = [measurement[1] for measurement in temperature_stats]
    avg_temp = [measurement[2] for measurement in temperature_stats]

    #return jsonify(most_active_station_id)
    return jsonify (min_temp,max_temp,avg_temp)

@app.route("/api/v1.0/custom")
def custom():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Retrieve min, avg and max temperatures"""
    # Query precipitation data

    most_active_station_id  = session.query(Measurement.station).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).first()[0]
    
    temperature_stats = session.query(
        func.min(Measurement.tobs).label('min_temp'),
        func.max(Measurement.tobs).label('max_temp'),
        func.avg(Measurement.tobs).label('avg_temp')
        ).filter(Measurement.station == most_active_station_id,Measurement.date > "2016-08-23").all()

    session.close()

    min_temp = [measurement[0] for measurement in temperature_stats]
    max_temp = [measurement[1] for measurement in temperature_stats]
    avg_temp = [measurement[2] for measurement in temperature_stats]
    
    return jsonify (min_temp,max_temp,avg_temp)

if __name__ == '__main__':
    app.run(debug=True)

##MAOV##