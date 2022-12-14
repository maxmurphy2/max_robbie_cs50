import os
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
import pandas as pd
import json
import plotly
import plotly.express as px
from apology import apology

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Global variable that we will update later
user_input = None

# Homepage
@app.route("/", methods=["GET", "POST"])
def index():
   if request.method == "GET":
      # Show form to allow user to choose what word to search for
      return render_template("index.html")

   elif request.method == "POST":
      global user_input
      user_input = request.form.get("text")

      # Send user to the /map page
      return redirect("/map")

# Map page
@app.route("/map", methods=["GET", "POST"])
def map():
      # Check that user has entered an input
      if user_input == None:
         return apology("Please enter an input. Go back to home page.")
   
      else:
         # Load the GeoJSON (map of the world)
         with open('custom.geo (1).json') as response:
            countries = json.load(response)

         # Load the Twitter data
         df = pd.read_csv("07_2020.csv")

         # Subselect the country and tweet columns
         twitter_data = df[["file_name", "text"]]

         # Create new df that contains country and number of tweets from that country

         # Now filter the df such that we only gets rows that contain this word
         twitter_data = twitter_data[twitter_data['text'].str.contains(user_input)]

         # Count the number of tweets per country
         tdf = pd.DataFrame().assign(info=twitter_data['file_name'].value_counts())
         tdf = tdf.reset_index()
         tdf.columns = ['country', 'count']

         # CHOROPLETH MAP

         # Change the max color depending on how many results countries get for the word
         max = tdf['count'].max()

         total_tweets = tdf['count'].value_counts().sum()

         fig = px.choropleth_mapbox(tdf, geojson=countries, featureidkey='properties.geounit',locations='country', color='count', color_continuous_scale="Viridis", range_color=(0, max), mapbox_style="carto-positron", zoom=3, opacity=0.5, labels={'tweets':'num of tweets'})
         
         fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
         
         graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

         return render_template("map.html", graphJSON=graphJSON, total_tweets=total_tweets, user_input=user_input)
