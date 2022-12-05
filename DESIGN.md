INTRODUCTION

We decided to build TWorldMap to solve the problem of the sheer information-overload that exists on Twitter. There is simply too much information out there for people to make sense of. To scope this problem, we decided to focus on a specific component of this: how to identify where in the world certain topics on Twitter are being spoken about the most, and visualize this in as simple a way as possible. 

Initially, we planned to connect to Twitter's API and query recent tweets to do this. However, we realized (having spent a significant amount of time exploring the API!) that it was not possible to access geo-tagged tweets unless we had access to the Enterprise version of the API. As such, we chose to instead use an open-source dataset that contained the necessary data. 

There were two main components to our project: (i) wrangling the twitter dataset using the pandas library and (ii) creating a choropleth map using the plotly library. We then had to make sure that the two fit together! To best explain how we did this, we have decided to break down each file (starting with app.py since it is the most important), going from top to bottom:

SECTION 1: datasets

Given that we could not use the Twitter API, we used a dataset that contained geo-tagged tweets from July 2020. The reason why we chose this particular dataset is because it contained tweets from many countries around the world (with the notable exceptions of the US and UK because if we included these the dataset would have been too big). 

The dataset we used to create a global map was from https://geojson-maps.ash.ms/. We chose medium resolution so we had a high degree of quality without taking up too much memory. 

SECTION 2: app.py

We begin by importing the relevant libraries, namely flask (to run our site), pandas (to wrangle the twitter dataset), plotly (to create the choropleth map), and apology (more on this below). Then, the application and session are configured. A global variable called 'user-input' is defined which will later be updated to what the user wants to query. Under # Homepage, we designed the homepage of our site. We made sure that if a user accessed this page using the 'GET' method, they would be shown index.html, and if they accessed this page using the 'POST' method (i.e. by filling out the form), 'user_input' would be updated and the user would be sent to the "map" page. 

The most critical code in our application comes from Line 35 onwards. First, we defined a function called map(). It begins by checking that a user has entered a value in the form, and then loads the GEoJSON map of the world. This was necessary to build our choropleth map. Then, we load in the Twitter dataset as a dataframe called df, and selected the country and tweet columns since these were the ones of interest. After this, we searched the dataset for all the rows where the user's input appears in the 'text' column. The number of tweets per country is then found by using 'value_counts()', and we chose to assign this to a new dataframe called 'tdf'. In order to split the new column that this creates into two separate ones, we  did 'reset_index()' and renamed the columns. (These few lines took us a lot of time!) 

Having prepared the dataframe, we could begin to create the choropleth map. First, to ensure that the color spectrum was roughly the same for every query regardless of the number of tweets, we created a variable called 'max' that took the country with the highest number of tweets for this query. This is later used as the upper-bound of the map creation. Then, we calculated the total number of countries that mentioned the query as 'total_tweets' (we did this so the user gets some more helpful information on the "/map" page). On line 70, we created the choropleth map. Using the 'plotly express' library, we load in the 'tdf' dataframe, set the 'geojson' argument to 'countries' (which is the name of the custom map dataset we loaded in), put the featureidkey to 'properties.geounit' (since in the 'countries' dataset, there is a dictionary within a dictionary, and this is the name of the key that contains the country names), set locations to 'country' (as this is the column in 'tdf' that has the country names), the color to 'count' (as we want to vary the color depending on the number of tweets), color_continuous_scale to 'viridis' (we chose this from many options, cf. https://plotly.com/python/builtin-colorscales/), range_color was set between 0 (since you can't have a negative number of tweets) and max (which is the aforementioned maximum number of tweets any given country has for that query), mapbox_style (again, chose this from this site https://plotly.com/python/mapbox-layers/), the zoom and opacity were chosen after experimentation for best visual effect, and finally labels were set to tweets and number of tweets (the keys of this dictionary correspond to the column names). Since the plotly site requires that the plot is encoded is JSON, we use json.dumps() (which comes with plotly) to convert the plot to JSON. Finally, we render the map.html template, sending the necessary variables over. 

SECTION 3: apology.py

We adapted this file from the Finance PSet but implemented a different apology image with a message from Twitter CEO Elon Musk. After development, this is only used if the user tries to jump to the world map without putting in a search query. 

SECTION 4: Templates (html files)

This contains our html pages and the actual design and structure of what we see on the TWorldMap website. The basic layout.html file provides the structure that our other pages rely on. All pages have the TWorldMap logo and a drop down menu for website navigation. index.html is the search page and has a twitter logo as well as a search bar with buttons. apology.html is for when errors are thrown and map.html is the page with the choropleth map.  
SECTION 3: static/styles.css

styles.css contains our css sheet with different styles for different html tags.
