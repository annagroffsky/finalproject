import sqlite3
import json 
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os

#connect to database
root = os.path.dirname(os.path.abspath(__file__)) + os.sep
file_name = root + 'ratings.sqlite'
conn = sqlite3.connect(file_name)
cur =  conn.cursor()
cur.execute("SELECT restaurants, avgrating FROM FoursquareRating")
#make a dict 
foursquare_ratings = {}
for row in cur: 
    foursquare_ratings[row[0]] =  row[1]

#name a text file and write the results to that 
with open('foursquare_ratings.text', 'w') as outfile: 
    json.dump(foursquare_ratings, outfile)

#assign x and y
x_restaurants = foursquare_ratings.keys()
y_ratings = foursquare_ratings.values()

#formatting
index = np.arange(len(x_restaurants))
plt.tight_layout()
plt.gcf().subplots_adjust(bottom=0.25)
plt.bar(index, y_ratings, align="center", width=0.5, color=["indigo"])
plt.xticks(index, x_restaurants, rotation="vertical", fontsize=6)

#naming axes 
plt.xlabel("Restaurants")
plt.ylabel("Average Foursquare Rating")
plt.title("Foursquare Ratings of AA Restaurants ")

#where to save the figure 
plt.savefig("Foursquare_ratings.png")

plt.show()


