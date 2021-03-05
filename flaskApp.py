import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///hawaii.sqlite")

Base=automap_base()

Base.prepare(engine, reflect=True)

Measurement=Base.classes.measurement
Station=Base.classes.station

app=Flask(__name__)

@app.route("/")
def welcome():
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    session=Session(engine)

    results=session.query(Measurement.date, Measurement.prcp)

    session.close()

    prcps=[]

    for date, prcp in results:
        prcpDict={}
        prcpDict['date']=date
        prcpDict['prcp']=prcp
        prcps.append(prcpDict)
    
    return jsonify(prcps)

@app.route("/api/v1.0/stations")
def stations():

    session=Session(engine)

    results=session.query(Station.name).all()

    session.close()

    stations=[]

    for station in results:
        statDict={}
        statDict['name']=station
        stations.append(statDict)

    return jsonify(stations)

if __name__ == '__main__':
    app.run(debug=True)