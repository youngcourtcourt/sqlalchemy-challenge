import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from dateutil import parser

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
        f"/api/v1.0/<start>/end<end>"
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

@app.route("/api/v1.0/tobs")
def tobs():
    
    session=Session(engine)

    lastTwelveStations=session.query(Measurement.date, Measurement.tobs).filter(Measurement.station=='USC00519281').filter(Measurement.date<='2017-08-23').filter(Measurement.date>='2016-08-23')

    session.close()

    temps=[]

    for date, tob in lastTwelveStations:
        tempDict={}
        tempDict['date']=date
        tempDict['tobs']=tob

        temps.append(tempDict)

    return jsonify(temps)

@app.route("/api/v1.0/<startDate>")
def start(startDate):
    
    for dash in startDate.splitlines():

        # newDash=dash.replace("/", "-")
        date = parser.parse(dash)
        standardizedDate=date.strftime("%Y-%m-%d")
    
    session=Session(engine)

    startDates=session.query(Measurement.date, Measurement.tobs).filter(Measurement.date>=standardizedDate)

    session.close

    startList=[]

    for date, tob in startDates:
        startDict={}
        startDict['date']=date
        startDict['tobs']=tob
        startList.append(startDict)
    
    return jsonify(startList)

if __name__ == '__main__':
    app.run(debug=True)