import sqlite3
import json 
import matplotlib
import matplotlib.pyplot as pyplot
import numpy as np

#connect to database
# conn = sqlite3.connect("powerRating.sqlite")
# cur = conn.cursor()

# cur.execute("SELECT * FROM ")
# #make a dict so {restaurant: yelp}
# comparison1 = {}
# # for row in cur: 
   
# #name a text file and write the results to that 
# # with open('.text', 'w') as outfile: 
# #     json.dump(power_ratings, outfile)
# #make a dict so {restaurant: 4square}
# cur.execute("SELECT FROM")
# comparison2 = {}

# #assign x axis to rating number and y to number of restaurants 
# x_restaurants = comparison1.values()
# y_ratings = comparison2.values()

# #formatting
# index = np.arrange(len(x_restaurants))
# plt.plot(index, width=".5", color=["red"])
# plt.xticks(index, fontsize=4)

# #naming axes 
# plt.xlabel("Yelp Ratings")
# plt.ylabel("Foursquare Ratings")
# plt.title("Comparison of Yelp and Foursquare Ratings of AA Restaurants")

# #where to save the figure 
# plt.savefig("comparison.png")

# plt.show()


    cur.execute('DROP TABLE IF EXISTS PowerRating')
    cur.execute('CREATE TABLE PowerRating (restaurants TEXT, yelpRating REAL, foursquareRating REAL, powerRating REAL)')
    
    cur.execute('SELECT Yelp.restaurants, Yelp.avgrating, Foursquare.avgrating')
    cur.execute('FROM Yelp')
    cur.execute('LEFT OUTER JOIN Foursquare')
    cur.execute('ON Yelp.restaurants = Foursquare.restaurants')