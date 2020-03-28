%matplotlib inline
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)

@app.route("/")
def welcome():
    return (
        f"This is the Hawaii weather API.<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    max_date = dt.date(2017, 8, 23)
    year_ago = max_date - dt.timedelta(days=365)
    data_pre = (session.query(Measurement.date, Measurement.prcp)
               .filter(Measurement.date <= max_date)
               .filter(Measurement.date >= year_ago)
               .order_by(Measurement.date).all())
    precipit = {date: prcp for date, prcp in data_pre}
    return jsonify(precipit)

@app.route("/api/v1.0/stations")
def stations():
    sta_name = session.query(Station.station).all()
    return jsonify(sta_name)

@app.route("/api/v1.0/tobs")
def tobs():
    max_date = dt.date(2017, 8, 23)
    year_ago = max_date - dt.timedelta(days=365)
    temp_obs = (session.query(Measurement.date, Measurement.station, Measurement.tobs)
               .filter(Measurement.date <= max_date)
               .filter(Measurement.date >= year_ago)
               .order_by(Measurement.tobs).all())
    return jsonify(temp_obs)

@app.route("/api/v1.0/<start>")
def start(start=None):
    day_temp = (session.query(Measurement.tobs).filter(Measurement.date.between(start, '2017, 8, 23').all())
    tobs_sta = pd.DataFrame(day_temp)
    tmin_sta = tobs_sta['tobs'].min()
    tavg_sta = tobs_sta['tobs'].mean()
    tmax_sta = tobs_sta['tobs'].max()
    return jsonify(tmin_sta, tavg_sta, tmax_sta)

@app.route("/api/v1.0/<start>/<end>")
def startend(start=None, end=None):
    multiday = (session.query(Measurement.tobs).filter(Measurement.date.between(start, end).all())
    tobs_s_e = pd.DataFrame(multiday)
    tmin_s_e = tobs_s_e['tobs'].min()
    tavg_s_e = tobs_s_e['tobs'].mean()
    tmax_s_e = tobs_s_e['tobs'].max()
    return jsonify(tmin_s_e, tavg_s_e, tmax_s_e)

if __name__ == "__main__":
    app.run(debug=True)
