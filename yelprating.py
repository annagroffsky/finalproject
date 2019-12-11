import sqlite3
import json 
import os
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

#connect to database
root = os.path.dirname(os.path.abspath(__file__)) + os.sep
file_name = root + 'ratings.sqlite'
conn = sqlite3.connect(file_name)
cur =  conn.cursor()
cur.execute("SELECT restaurants, avgrating FROM YelpRating")
#make a dict 
yelp_ratings = {}
for row in cur: 
    yelp_ratings[row[0]] = row[1]


#name a text file and write the results to that 
with open('yelp_ratings.text', 'w') as outfile: 
    json.dump(yelp_ratings, outfile)

#assign x and y
x_restaurants = yelp_ratings.keys()
y_ratings = yelp_ratings.values()

#formatting
index = np.arange(len(x_restaurants))
plt.tight_layout()
plt.gcf().subplots_adjust(bottom=0.25)
plt.bar(index, y_ratings, align="center", width=0.5, color=["red"])
plt.xticks(index, x_restaurants, rotation="vertical", fontsize=6)

#naming axes 
plt.xlabel("Restaurants")
plt.ylabel("Average Yelp Rating")
plt.title("Yelp Ratings of AA Restaurants ")

#where to save the figure 
plt.savefig("yelp_ratings.png")

plt.show()


