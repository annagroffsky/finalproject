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

cur.execute("SELECT restaurants, priceTier FROM YelpPrice")
#make a dict 
yelp_price = {}
for row in cur: 
    if row[1] == None:
        yelp_price[row[0]] = 0
    else:
        yelp_price[row[0]] =  len(row[1])

#name a text file and write the results to that 
with open('yelp_price.text', 'w') as outfile: 
    json.dump(yelp_price, outfile)

#assign x and y
x_restaurants = yelp_price.keys()
y_ratings = yelp_price.values()

#formatting
index = np.arange(len(x_restaurants))
plt.tight_layout()
plt.gcf().subplots_adjust(bottom=0.25)
plt.bar(index, y_ratings, align="center", width=0.5, color=["green"])
plt.xticks(index, x_restaurants, rotation="vertical", fontsize=6)

#naming axes 
plt.xlabel("Restaurants")
plt.ylabel("Price Tier")
plt.title("Price Tier Rating of AA Restaurants (from Yelp)")

#where to save the figure 
plt.savefig("yelp_price.png")

plt.show()


