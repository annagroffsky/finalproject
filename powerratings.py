import sqlite3
import json 
import matplotlib
import matplotlib.pyplot as pyplot
import numpy as np

#connect to database
conn = sqlite3.connect(".sqlite")
cur = conn.cursor()

cur.execute("SELECT * FROM ")
#make a dict so {rating number: number of restaurants}
power_ratings = {}
for row in cur: 

#name a text file and write the results to that 
with open('.text', 'w') as outfile: 
    json.dump(power_ratings, outfile)

#assign x axis to rating number and y to number of restaurants 
x_restaurants = power_ratings.keys()
y_ratings = power_ratings.values()

#formatting
index = np.arrange(len(x_restaurants))
plt.bar(index, y_ratings, align="center", width=".5", color=["red"])
plt.xticks(index, x_restaurants, fontsize=4)

#naming axes 
plt.xlabel("Combined Yelp and Foursquare Rating Number")
plt.ylabel("Number of AA Restaurants with Power Rating")
plt.title("Power Ratings of AA Restaurants ")

#where to save the figure 
plt.savefig("power_ratings.png")

plt.show()


