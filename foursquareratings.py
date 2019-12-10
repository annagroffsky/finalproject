import sqlite3
import json 
import matplotlib
import matplotlib.pyplot as pyplot
import numpy as np

#connect to database
conn = sqlite3.connect("ratings.sqlite")
cur = conn.cursor()

cur.execute("SELECT * FROM ")
#make a dict so {rating number: number of restaurants}
foursquare_ratings = {}
for row in cur: 
    
#name a text file and write the results to that 
with open('foursquare_ratings.text', 'w') as outfile: 
    json.dump(foursquare_ratings, outfile)

#assign x axis to rating number and y to number of restaurants 
x_restaurantss = foursquare_ratings.keys()
y_ratings = foursquare_ratings.values()

#formatting
index = np.arrange(len(x_restaurants))
plt.bar(index, y_ratings, align="center", width=".5", color=["red"])
plt.xticks(index, x_restaurants, fontsize=4)

#naming axes 
plt.xlabel("Restaurants")
plt.ylabel("Average Foursquare Rating")
plt.title("Foursquare Ratings of AA Restaurants ")

#where to save the figure 
plt.savefig("foursquare_ratings.png")

plt.show()


