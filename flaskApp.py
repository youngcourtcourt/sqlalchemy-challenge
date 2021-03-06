# Import dependencies

import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from dateutil import parser

from flask import Flask, jsonify

#Create engine and reflect db

engine = create_engine("sqlite:///hawaii.sqlite")

Base=automap_base()

Base.prepare(engine, reflect=True)

#Create both measurement and station tables from classes

Measurement=Base.classes.measurement

Station=Base.classes.station

#Initialize flask app

app=Flask(__name__)

#Define Index route 

@app.route("/")
def welcome():
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<start><br/>"
        f"/api/v1.0/start<start>/end<end>"
    )

#Define precipitation reoute

@app.route("/api/v1.0/precipitation")
def precipitation():

    #Connect to database and query for all dates and respective precipitation

    session=Session(engine)

    results=session.query(Measurement.date, Measurement.prcp)

    session.close()

    prcps=[]

    #Cycle through results and store in a dictionary, then append dictionary to list

    for date, prcp in results:
        prcpDict={}
        prcpDict['date']=date
        prcpDict['prcp']=prcp
        prcps.append(prcpDict)
    
    return jsonify(prcps)

@app.route("/api/v1.0/stations")
def stations():

#Connect to database and query for stations

    session=Session(engine)

    results=session.query(Station.name).all()

    session.close()

    stations=[]
    
#Cycle through results and store in a dictionary, then append dictionary to list


    for station in results:
        statDict={}
        statDict['name']=station
        stations.append(statDict)

    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():

#Connect to database and query, filtering for most active station

    
    session=Session(engine)

    lastTwelveStations=session.query(Measurement.date, Measurement.tobs).filter(Measurement.station=='USC00519281').filter(Measurement.date<='2017-08-23').filter(Measurement.date>='2016-08-23')

    session.close()

    temps=[]

#Cycle through results and store in a dictionary, then append dictionary to list

    for date, tob in lastTwelveStations:
        tempDict={}
        tempDict['date']=date
        tempDict['tobs']=tob

        temps.append(tempDict)

    return jsonify(temps)

@app.route("/api/v1.0/<startDate>")
def start(startDate):
    
#Normalize date to YYYY-MM-DD format

    for dash in startDate.splitlines():

        date = parser.parse(dash)
        standardizedDate=date.strftime("%Y-%m-%d")
    
#Connect to database

    session=Session(engine)

#Store min, max and avg queries into variables for better readability

    Min=func.min(Measurement.tobs)
    Max=func.max(Measurement.tobs)
    Avg=func.avg(Measurement.tobs)

#Query the database, filtering on date defined by user and calculate the min, max and avg for each date

    startDates=session.query(Measurement.date, Min, Max, Avg).filter(Measurement.date>=standardizedDate).group_by(Measurement.date).all()

    session.close

    startList=[]

#Unpack database query into 4 variables, store variables in dictionary

    for date, minTemp, maxTemp, avgTemp in startDates:
        startDict={}
        startDict['TMin']=minTemp
        startDict['TMax']=maxTemp
        startDict['TAvg']=avgTemp
        startList.append(startDict)
    
    return jsonify(startList)


if __name__ == '__main__':
    app.run(debug=True)