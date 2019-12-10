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
yelp_ratings = {}
for row in cur: 
    
#name a text file and write the results to that 
with open('yelp_ratings.text', 'w') as outfile: 
    json.dump(yelp_ratings, outfile)

#assign x axis to rating number and y to number of restaurants 
x_names = yelp_ratings.keys()
y_ratings = yelp_ratings.values()

#formatting
index = np.arrange(len(x_restaurants))
plt.bar(index, y_ratings, align="center", width=".5", color=["red"])
plt.xticks(index, x_restaurants, fontsize=4)

#naming axes 
plt.xlabel("Restaurants")
plt.ylabel("Average Yelp Rating")
plt.title("Yelp Ratings of AA Restaurants ")

#where to save the figure 
plt.savefig("yelp_ratings.png")

plt.show()


