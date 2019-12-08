import requests
import json
import unittest
import sqlite3
import os
from yelpapi import YelpAPI
import foursquare
import time


#define a function that graphs both sets of values on the same graph 

#define a function that combines number of reviews vs number of 5 stars-sort from highest to lowest based on value

#visualizatoins: 1. scatterplot of # of followers vs # of 5 stars 2. map showing dots of restaurants relative to their cumulative score


# #gets parameters to be called in the yelp api--only focusing on restaurants, an input location, and getting 20 results with each call
# #returns params
def get_search_parameters(location, offset):
    params = {}
    params['term'] = 'restaurant'
    params['location'] = location
    params['limit'] = 20
    params['offset'] = offset

    return params

# #takes in params and makes api request to yelp
# #retuns a dictionary called search results
# #if request doesn't work prints "exception"
def get_yelp_data(params):
    api_key = 'm2Fz_n7pVC_-u3GTRpW392W_IpIWLL1e7ACybtxbOIulWzuhQ1U-mSWuCmNPZepBpWAzSq6kKmL9HF-rqMGYARNXy1y1016FU6_jEEFVHtivYJQlmpNxaHdBNnrdXXYx'
    yelp_api = YelpAPI(api_key, timeout_s=3.0)

    print('Fetching for {}'.format(params["location"]))
    try:
        search_results = yelp_api.search_query(term = params['term'], location=params['location'], limit = params['limit'], offset = params['offset'])
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

#returns a dictionary fs_restaurant_info_dict
#keys are the passed restaurant names
#values are a tuple with most popular hours for the venue and the day on which they occur
    #Monday = 1... Sunday = 7

def get_foursquare_object(location, restaurant):
    # Construct the client object
    CLIENT_ID = u'BEBAAJUVQVTM15PTUP3DFUQ52FXMXEMENN3RZKF0MIGYAQJG'
    CLIENT_SECRET = u'QQ43LLAMSWS5TD1EQP1KUPH5XCYE1MN0QCN0OLYLP3TXSLND'
    client = foursquare.Foursquare(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)

    fs_restaurant_info_dict = {}

    
    # rest_list = []
    #get venue id from search
    venue_info = client.venues.search(params={'near': location, 'query': restaurant, 'limit': 1})
    venue_id = venue_info['venues'][0]['id']
    #get most popular times and day on which that occurs
    # hours = client.venues.hours(venue_id)
    
    # if hours['popular'] == None:
    #     most_popular_hours_day = 100
    #     most_popular_hours_start = 100
    #     most_popular_hours_end = 100
    # else:
    #     most_popular_hours_day = hours['popular']['timeframes'][0]['days'][0]
        
    #     if hours['popular']['timeframes'][0]['open'][0]['start'] == None:
    #         most_popular_hours_start = 100
    #     else: 
    #         most_popular_hours_start = int(hours['popular']['timeframes'][0]['open'][0]['start'])
    #     if hours['popular']['timeframes'][0]['open'][0]['end'] == None:
    #         most_popular_hours_end = 100
    #     else:
    #         most_popular_hours_end = int(hours['popular']['timeframes'][0]['open'][0]['end'])
    
    # popular_day_start_end_tup = (most_popular_hours_day, most_popular_hours_start, most_popular_hours_end)
    # #add popular hours tuple to rest_list
    # rest_list.append(popular_day_start_end_tup)
    
    #get average rating
    details = client.venues(venue_id)
    rating = details.get('rating')
    # i think it has something to do with the underlined client  
    #bc when i tried to do it with the Venues it suggests it gave a diff error 

    if rating == None:
        adjusted_rating = 1000
    else:
        #divide by 2 to compare to yelp's ratings
        adjusted_rating = rating/2
    #add adjusted_rating to rest_list
    # rest_list.append(adjusted_rating)
    #add rest_list to dictionary
    fs_restaurant_info_dict[restaurant] = adjusted_rating
        
    return fs_restaurant_info_dict

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
    # city = input("Enter a city name: ")
    city = 'Ann Arbor'
    offset1 = 0
    
    conn = sqlite3.connect('/Users/AnnaGroffsky/Desktop/ratings.sqlite')
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS Yelp')
    cur.execute('CREATE TABLE Yelp (city TEXT, restaurants TEXT, avgrating REAL)')
    cur.execute('DROP TABLE IF EXISTS Foursquare')
    cur.execute('CREATE TABLE Foursquare (city TEXT, restaurants TEXT, avgrating REAL)')
    
    counter = 0
    
    while counter<=100:
        if counter>1 and counter%20 == 0:
            offset1 += 20
            break
        else:
            param1 = get_search_parameters(city, offset1)
            data1 = get_yelp_data(param1)
            print("Getting results 1-20")
            ratings= rating_dict(data1)
            for k, v in ratings.items():
                fs_obj1 = get_foursquare_object(city, k)
                cur.execute('INSERT INTO Yelp (city, restaurants, avgrating) VALUES (?, ?, ?)', (city, k, v))
                cur.execute('INSERT INTO Foursquare (city, restaurants, avgrating) VALUES (?, ?, ?)', (city, k, fs_obj1[k]))
                counter += 1
                continue
    
    while counter<=100:
        if counter>21 and counter%20 == 0:
            offset1 += 20
            break
        else:
            param1 = get_search_parameters(city, offset1)
            data1 = get_yelp_data(param1)
            print('Getting results 21-40')
            ratings= rating_dict(data1)
            for k, v in ratings.items():
                cur.execute('INSERT INTO Yelp (city, restaurants, avgrating) VALUES (?, ?, ?)', (city, k, v))
                counter += 1
                continue

    while counter<=100:
        if counter>41 and counter%20 == 0:
            offset1 += 20
            break
        else:
            param1 = get_search_parameters(city, offset1)
            data1 = get_yelp_data(param1)
            print('Getting results 41-60')
            ratings= rating_dict(data1)
            for k, v in ratings.items():
                cur.execute('INSERT INTO Yelp (city, restaurants, avgrating) VALUES (?, ?, ?)', (city, k, v))
                counter += 1
                continue
    
    while counter<=100:
        if counter>61 and counter%20 == 0:
            offset1 += 20
            break
        else:
            param1 = get_search_parameters(city, offset1)
            data1 = get_yelp_data(param1)
            print('Getting results 61-80')
            ratings= rating_dict(data1)
            for k, v in ratings.items():
                cur.execute('INSERT INTO Yelp (city, restaurants, avgrating) VALUES (?, ?, ?)', (city, k, v))
                counter += 1
                continue

    while counter<=100:
        if counter>81 and counter%20 == 0:
            offset1 += 20
            break
        else:
            param1 = get_search_parameters(city, offset1)
            data1 = get_yelp_data(param1)
            print('Getting results 81-100')
            ratings= rating_dict(data1)
            for k, v in ratings.items():
                cur.execute('INSERT INTO yelp (city, restaurants, avgrating) VALUES (?, ?, ?)', (city, k, v))
                counter += 1
                continue


    #for loop for foursquare
    conn.commit()
    cur.close()
    
    
    
    # cur.execute('INSERT INTO Restaurant (city, restaurants, avgrating) VALUES (?, ?, ?)', ("Ann Arbor", "Aventura", 5.0))
    # conn.commit()
    # cur.close() 

    # conn = sqlite3.connect('/Users/AnnaGroffsky/Desktop/foursquare.sqlite')
    # # cur = conn.cursor()
    # cur.execute('DROP TABLE IF EXISTS Foursquare')
    # cur.execute('CREATE TABLE Foursquare (city TEXT, restaurants TEXT, ratings INTEGER, busyhourstart INTEGER, busyhourend INTEGER)')
    # cur.execute('INSERT INTO Foursquare (city, restaurants, ratings, busyhourstart, busyhourend) VALUES (?, ?, ?, ?, ?)', ("Ann Arbor", "Savas", 4.5, 1200, 1400))
    # conn.commit()
    # cur.close()

    #check the start of every time you run: if statement :)

    #increment the request 

    #UNIQUE 

    #if not in database, insert

    #set max as 100 then do if statements 

    #if length< xyz then add 20 * 4

if __name__ == "__main__":
    main()


