import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import datetime as dt
from datetime import datetime

#Database setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect existing database into a new model
Base = automap_base()

# Reflect the tables
Base.prepare(engine, reflect=True)

# Saving reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#Flask setup
app = Flask(__name__)

#Flask routes
@app.route("/")
def home():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/stations")
def stations():
    session= Session(engine)
    results=session.query(Station.name).all()
    session.close()
    
    stations=list(np.ravel(results))
    
    return jsonify(stations)


@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    
    results=session.query(Measurement.date, Measurement.prcp).all()
    session.close()
    
    rain=[]
    for date, prcp in results:
        rain_dict={}
        rain_dict['date'] = date
        rain_dict['prcp'] = prcp
        rain.append(rain_dict)
    
    return jsonify(rain)


@app.route("/api/v1.0/tobs")
def temperature():
    session = Session(engine)
    
    #Find last date of measurements in dataset, convert to datetime.date object
    last_date=session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    last_date=datetime.strptime(last_date, '%Y-%m-%d').date()
   
    #Subtract 12 months to find first date 
    first_date = last_date - dt.timedelta(days=365)
    
    results= session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > first_date).all()
    
    session.close()
    
    temp=list(np.ravel(results))
    
    return jsonify(temp)


@app.route("/api/v1.0/<start>")
def summ_from(start):
    session = Session(engine)
    
    results= session.query(Measurement.date, func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date>start).all()
    
    session.close()

    summ_temp=list(np.ravel(results))
    
    return jsonify(summ_temp)

'''
@app.route("/api/v1.0/<start>/<end>")
def summ_range(start, end):
    session = Session(engine)
    
    results=session.query(Measurement.date, Measurement.prcp).all()
    session.close()
    
    return jsonify()

'''

if __name__ == '__main__':
    app.run(debug=True)
    
    
    
    
    
    
    
    