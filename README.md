# max_robbie_cs50
Max Murphy and Robbie Owen's repository for CS50 final project.

To run our project, please copy our repository into the CS50 codespace or a new codespace with the relevant downloads of python, flask, flasksession, etc. Once it is set up, type 'flask run' into the terminal to visit our website. 

Our website creates a choropleth map (like a heat map) of tweets globally. In order to generate this map, we take whatever query you would like to search for, and search for it in a database of (geotagged) tweets taken from July 2020. To search for your tweet and create the corresponding choropleth map enter your tag into the search bar and press search! Since our dataset has millions of lines of data, creating this map may take a few seconds. 

To navigate the heat map use the menu options in the top right hand of the map. To pan across the map click and drag. There are multiple options available for users:
1. Press the camera icon to download the plot as a png.
2. Press the box select icon to select a region of the plot in a box for emphasis.
3. Press the lasso select icon to select a region of the plot in a lasso selection for emphasis.
4. Zoom in or out by scrolling up and down or by pressing the zoom in/out icons in the menu of the plot. 
5. Press the house icon to reset your view. 
6. Press the toggle button to change whether a pop up will appear when you hover your mouse over a country. This pop up shows what the country is and how many tweets were recorded in that region in our dataset. 

We also have a drop down menu in the top right of the website which allows you to navigate to our homepage and back to our map. You cannot navigate to the map unless you have already created a search. If you try to navigate to the map without an input you will receive an error page with a special message from Twitter CEO Elon Musk. You can also return to the homepage by pressing the TWorldMap icon in the top left of any page. 

IMPORTANT!:

Because of how massive the original datasets were, the website took a long time to render. Since a massive amount of tweets came from the US and UK, we opted to use a dataset that did not include tweets from these two countries. We believe this is a sacrifice worth taking and gives our website a more international leaning rather than being traditionally American-centric. (With more compute, we would have been able to extend to these datasets!)
