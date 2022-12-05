Stage 1: setting up
Create a shared codespace. DONE.
Work out who is going to do which of the steps below, and when by. 

Stage 2: Frontend (Max - I’ll start with this?)
Create a website that has a map of the world on it
‘All files from github’ ​​https://github.com/CrazyDaffodils/Interactive-Choropleth-Map-Using-Python 
Render world map https://www.naturalearthdata.com/downloads/110m-cultural-vectors/
(NOT NECESSARY BUT WE WILL MAKE A PARALLEL) Data used in obesity example Share of adults that are obese, 2016




 
Put a drop-down bar in the top right that enables users to query key words/phrases. 
To start with, just read in a CSV/excel file which has all the data. Once this works, THEN we can connect to the Twitter API instead (see below). 
Color-code the maps by country according to the results from the Twitter query. 

Stage 3: Backend
Get signed up to Twitter’s API. DONE. 
Make sure both of us can access Twitter API. 
Choose a set of 5 key words/phrases that we want to query for. 
Work out how to group these queries by country. 

How we can scope this a bit more

Let’s just look at Tweets between January-June 2022 or something, otherwise we will have too many Tweets. 

Instead of a query search bar at first, I think we should have a drop down menu which has a few choices that users can query for.

Twitter data options

​​https://github.com/shaypal5/awesome-twitter-data

Helpful info

API Key
czSH3h3wAbx123m0rFnvs3zqU

API Key Secret
rWu5tNjUq1yMBEeNbOTvyb5QeF04rF4CiVB3eMX1VwWIp7GxBI

Bearer Token
AAAAAAAAAAAAAAAAAAAAAKBPjgEAAAAA5uj95lPVk3kyFLUJyn9BBYf3iQk%3D2Z0AXQ1px9UZbjJSS7ouVi33H5EhD8vvPCgJ0g5CwxxwUFDvoj

Access token
2567164875-Sb51Yr1oIjc3pr1JEyaJoKbmfmTTiUL02M3Gpo7

Access token secret
H1IBTHeHC28vF6znTT0Y6s5mdyJERWE6Vl8SVE8Nrhd6k

Backend links

https://developer.twitter.com/en/docs/tutorials/filtering-tweets-by-location

https://developer.twitter.com/en/docs/twitter-api/v1/trends/trends-for-location/api-reference/get-trends-place



Frontend links

Best thing to use is something called Dash (here are the docs) and Plotly. 

And this seems to be the best tutorial of how to use it https://towardsdatascience.com/choropleth-maps-in-practice-with-plotly-and-python-672a5eef3a19 and https://towardsdatascience.com/choropleth-maps-in-practice-with-plotly-and-python-672a5eef3a19

https://www.youtube.com/watch?v=7m0Bq1EGPPg&t=0s

https://towardsdatascience.com/a-complete-guide-to-an-interactive-geographical-map-using-python-f4c5197e23e0

https://community.plotly.com/t/interactive-map-with-clickable-countries/39495/14


Sort out the navigation bar

Do description at front of first page
