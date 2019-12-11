import sqlite3
import json 
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

#connect to database
conn = sqlite3.connect("/Users/AnnaGroffsky/Desktop/ratings.sqlite")
cur = conn.cursor()

cur.execute("SELECT restaurants, avgrating FROM YelpRating")
#make a dict so {rating number: number of restaurants}
yelp_ratings = {}
for row in cur: 
    yelp_ratings[row[0]] = row[1]


#name a text file and write the results to that 
with open('yelp_ratings.text', 'w') as outfile: 
    json.dump(yelp_ratings, outfile)

#assign x axis to rating number and y to number of restaurants 
x_restaurants = yelp_ratings.keys()
y_ratings = yelp_ratings.values()

#formatting
index = np.arange(len(x_restaurants))
plt.tight_layout()
plt.gcf().subplots_adjust(bottom=0.15)
plt.bar(index, y_ratings, align="center", width=0.5, color=["red"])
plt.xticks(index, x_restaurants, rotation="vertical", fontsize=3)

#naming axes 
plt.xlabel("Restaurants")
plt.ylabel("Average Yelp Rating")
plt.title("Yelp Ratings of AA Restaurants ")

#where to save the figure 
plt.savefig("yelp_ratings.png")

plt.show()


