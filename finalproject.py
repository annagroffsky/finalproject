import requests
import json
import unittest
import sqlite3
import os
from yelpapi import YelpAPI

# define a function to go through the yelp api-produce a dictionary of key: restuarant name, value: # of 5 star reviews 

#define a function to go through the twitter api-take in the keys from the yelp and create either another value w/ follower or a separate dict

#define a function that graphs both sets of values on the same graph 

#define a function that combines number of reviews vs number of 5 stars-sort from highest to lowest based on value

#visualizatoins: 1. scatterplot of # of followers vs # of 5 stars 2. map showing dots of restaurants relative to their cumulative score


# #gets parameters to be called in the yelp api--only focusing on restaurants, an input location, and getting 20 results with each call
# #returns params
def get_search_parameters(location):
    params = {}
    params['term'] = 'restaurant'
    params['location'] = location
    params['limit'] = '20'

    return params

# #takes in params and makes api request to yelp
# #retuns a dictionary called search results
# #if request doesn't work prints "exception"
def get_yelp_data(params):
    api_key = 'm2Fz_n7pVC_-u3GTRpW392W_IpIWLL1e7ACybtxbOIulWzuhQ1U-mSWuCmNPZepBpWAzSq6kKmL9HF-rqMGYARNXy1y1016FU6_jEEFVHtivYJQlmpNxaHdBNnrdXXYx'
    yelp_api = YelpAPI(api_key, timeout_s=3.0)

    print('Fetching for {}'.format(params["location"]))
    try:
        search_results = yelp_api.search_query(term = params['term'], location=params['location'], sorty_by = 'rating', limit = params['limit'])
    except:
            print('Exception')
            return None
    return search_results

# #returns a dictionary of restaurant name as key and rating as value
def rating_dict(search_results):
    restaurant_ratings = {}
    lst = search_results['businesses']
    for item in lst:
        name = item['name']
        rating = item['rating']
        restaurant_ratings[name] = rating
    return restaurant_ratings

# def yelp_database():
# conn = sqlite3.connect('/Users/AnnaGroffsky/Desktop/ratings.sqlite')
# cur = conn.cursor()
# cur.execute('DROP TABLE IF EXISTS Restaurants')
# cur.execute('CREATE TABLE Restaurants (restaurants TEXT, avgrating INTEGER)')
# cur.execute('INSERT INTO Restaurants (restaurants, avgrating) VALUES (?, ?)', ('Zingermans', 5))
# cur.execute('INSERT INTO Restaurants (restaurants, avgrating) VALUES (?, ?)', ("Savas", 4.5))
# cur.execute('INSERT INTO Restaurants (restaurants, avgrating) VALUES (?, ?)', ("Aventura", 4.8))
# conn.commit()
# cur.close()

def main():
    #test getting the data from the api
    param1 = get_search_parameters('Ann Arbor')
    data1 = get_yelp_data(param1)
    ratings= rating_dict(data1)
    print(ratings)

    conn = sqlite3.connect('/Users/AnnaGroffsky/Desktop/ratings.sqlite')
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS Restaurants')
    cur.execute('CREATE TABLE Restaurants (restaurants TEXT, avgrating INTEGER)')
    cur.execute('INSERT INTO Restaurants (restaurants, avgrating) VALUES (?, ?)', ("Savas", 4.5))
    cur.execute('INSERT INTO Restaurants (restaurants, avgrating) VALUES (?, ?)', ("Anna", 5.0))
    conn.commit()
    cur.close()



if __name__ == "__main__":
    main()


