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
    try:
        search_results = yelp_api.search_query(term = params['term'], location=params['location'], limit = params['limit'], offset = params['offset'])
    except:
            print('Exception')
            return None
    return search_results

# #returns a dictionary of restaurant name as key and rating as value
def yelp_rating_dict(search_results):
    restaurant_ratings = {}
    lst = search_results['businesses']
    for item in lst:
        name = item['name']
        rating = item['rating']
        restaurant_ratings[name] = rating
    return restaurant_ratings

#returns a dictionary of restaurant as key and price tier as value
def yelp_price_tier_dict(search_results):
    price_tier_dict = {}
    lst = search_results['businesses']
    for item in lst:
        name = item['name']
        price_tier = item.get('price')
        price_tier_dict[name] = price_tier
    return price_tier_dict

#returns dictionary where restaurant is key and fs rating is value
def fs_rating_dict(location, restaurant):
    CLIENT_ID = u'DAJHGJUV1YKN0VP3HCPIMD0DW24CPOEC2UKODDBUGRV2JE0B'
    CLIENT_SECRET = u'CDBG4J2PHRLVS3JM4KMJCGNGWBPHT4LWLAFCPXUJUVNYQAVC'
    client = foursquare.Foursquare(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    rating_dict = {}
    #get venue id from search
    venue_info = client.venues.search(params={'near': location, 'query': restaurant, 'limit': 1})
    if len(venue_info['venues']) == 0:
        rating_dict[restaurant] = 1000
        return rating_dict
    else:  
        venue_id = venue_info['venues'][0]['id']
        if len(venue_info['venues']) == 0:
            rating_dict[restaurant] = 1000
            return rating_dict
        else:
            venue_id = venue_info['venues'][0]['id']
            #get average rating
            details = client.venues(venue_id)
            rating = details['venue'].get('rating')
            
            if rating == None:
                rating_dict[restaurant] = 1000
            else:
                #divide by 2 to compare to yelp's ratings
                adjusted_rating = rating/2
                rating_dict[restaurant] = adjusted_rating
        
        return rating_dict

#returns a dictionary where restaurant is key and price tier is value (integer 1-4)
def fs_price_tier_dict(location, restaurant):
    CLIENT_ID = u'DAJHGJUV1YKN0VP3HCPIMD0DW24CPOEC2UKODDBUGRV2JE0B'
    CLIENT_SECRET = u'CDBG4J2PHRLVS3JM4KMJCGNGWBPHT4LWLAFCPXUJUVNYQAVC'
    client = foursquare.Foursquare(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    price_tier_dict = {}
    #get venue id from search
    venue_info = client.venues.search(params={'near': location, 'query': restaurant, 'limit': 1})
    
    if venue_info['venues'] == None:
        price_tier_dict[restaurant] = 1000
    else:
        if len(venue_info['venues']) == 0:
            price_tier_dict[restaurant] = 1000
            return price_tier_dict
        else:
            venue_id = venue_info['venues'][0]['id']
            details = client.venues(venue_id)
            price = details['venue'].get('price')
            if price == None:
                price_tier = 1000
                price_tier_dict[restaurant] = price_tier
            else:
                price_tier = price.get('tier')
                price_tier_dict[restaurant] = price_tier
            
        return price_tier_dict



def main():
    city = input("Enter a city name: ")
    offset1 = input("Offset: ")
    
    conn = sqlite3.connect('/Users/kristenpicard/Desktop/ratings.sqlite')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS 'YelpRating' ('city' TEXT, 'restaurants' TEXT UNIQUE, 'avgrating' REAL)")
    cur.execute("CREATE TABLE IF NOT EXISTS 'YelpPrice' ('city' TEXT, 'restaurants' TEXT UNIQUE, 'priceTier' TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS 'FoursquareRating' ('city' TEXT, 'restaurants' TEXT UNIQUE, 'avgrating' REAL)")
    cur.execute("CREATE TABLE IF NOT EXISTS 'FoursquarePrice' ('city' TEXT, 'restaurants' TEXT UNIQUE, 'priceTier' INTEGER)")

 
    counter = 0
    
    while counter <= 20:
        if counter == 20:
            break
        
        else:
            params = get_search_parameters(city, offset1)
            yelp_obj = get_yelp_data(params)
            print("Getting results")
            yelp_ratings = yelp_rating_dict(yelp_obj)
            yelp_price_tiers = yelp_price_tier_dict(yelp_obj)
            
            for k, v in yelp_ratings.items():
                cur.execute('INSERT INTO YelpRating (city, restaurants, avgrating) VALUES (?, ?, ?)', (city, k, v))
                fs_obj_rating = fs_rating_dict(city, k)

                if len(fs_obj_rating.keys()) == 0:
                    cur.execute('INSERT INTO FoursquareRating (city, restaurants, avgrating) VALUES (?, ?, ?)', (city, k, 1000))
                else:
                    cur.execute('INSERT INTO FoursquareRating (city, restaurants, avgrating) VALUES (?, ?, ?)', (city, k, fs_obj_rating[k]))
            
            for k, v in yelp_price_tiers.items(): 
                cur.execute('INSERT INTO YelpPrice (city, restaurants, priceTier) VALUES (?, ?, ?)', (city, k, v))
                fs_obj_price = fs_price_tier_dict(city, k)

                if len(fs_obj_price.keys()) == 0:
                    cur.execute('INSERT INTO FoursquarePrice (city, restaurants, priceTier) VALUES (?, ?, ?)', (city, k, 1000))
                    counter += 1
                else:
                    cur.execute('INSERT INTO FoursquarePrice (city, restaurants, priceTier) VALUES (?, ?, ?)', (city, k, fs_obj_price[k]))
                    counter += 1

    
    #make joined table
    cur.execute('SELECT YelpRating.restaurants, YelpRating.avgrating, FoursquareRating.avgrating FROM YelpRating LEFT JOIN FoursquareRating ON YelpRating.restaurants = FoursquareRating.restaurants')

    print('Restaurant Power Ratings')
    for row in cur.fetchall():
        if not (row[1] and row[2]):
            print('{} has no power rating.'.format(row[0]))
        else:
            power_rating = row[1] + row[2]
            print('{}: {}'.format(row[0], power_rating))

        # else:
        #     power_rating = row[1] + row[2]
        #     print('{}: {}'.format(row[0], power_rating))


    # for row in cur:
    #     power_rating = float(row[1]) + float(row[2])
    #     print('{}: {}'.format(row[0], power_rating))


    conn.commit()
    cur.close()
    
if __name__ == "__main__":
    main()


