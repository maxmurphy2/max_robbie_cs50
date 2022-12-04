import os
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
import pandas as pd
import json
import plotly
import plotly.express as px

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def index():
   # Form to allow user to choose what word to search for
   return render_template("index.html")

@app.route("/map")
def map():
      return render_template("map.html", graphJSON=choro())

def choro():
   # Load the GeoJSON (map of the world)
   with open('/Users/maxmurphy/Dropbox (Personal)/My Mac (Max’s MacBook Pro)/Downloads/custom.geo (1).json') as response:
      countries = json.load(response)

   #print(countries["features"][0])

   # Load the Twitter data
   df = pd.read_csv("/Users/maxmurphy/Dropbox (Personal)/My Mac (Max’s MacBook Pro)/Downloads/07_2020.csv")

   # Subselect the country and tweet columns
   twitter_data = df[["file_name", "text"]]

   # Create new df that contains country and proportion of tweets from that country
   # (Proportion might be a better way of doing it, just do normalize = True)

   # WORD THAT IS GOING TO BE SEARCHED FOR (EVENTUALLY GET USER INPUT)
   word = "football"

   # Now filter the df such that we only gets rows that contain this word
   twitter_data = twitter_data[twitter_data['text'].str.contains(word)]

   # print(twitter_data.head())

   # Count the number of tweets per country
   tdf = pd.DataFrame().assign(info=twitter_data['file_name'].value_counts())
   tdf = tdf.reset_index()
   tdf.columns = ['country', 'count']

   # CHOROPLETH MAP

   # Change the max color depending on how many results countries get for the word
   max = tdf['count'].max()

   fig = px.choropleth_mapbox(tdf, geojson=countries, featureidkey='properties.geounit',locations='country', color='count', color_continuous_scale="Viridis", range_color=(0, max), mapbox_style="carto-positron", zoom=3, opacity=0.5, labels={'tweets':'num of tweets'})
   
   fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
   
   graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

   return graphJSON