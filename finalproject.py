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


#returns the search info for the passed restaurant
# def get_foursquare_object(location, restaurant):
#     # Construct the client object
#     CLIENT_ID = u'OO3LVQ50PEU241GACB3GMFGOQCEMBBGMJKXHFP1IYO2MECOI'
#     CLIENT_SECRET = u'TXQPMS1KMG4DBNFFAA4OBEMEEJG3FW0SNPPGZ0IKGNLQIRE1'
#     client = foursquare.Foursquare(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)

#     #get venue id from search
#     venue_info = client.venues.search(params={'near': location, 'query': restaurant, 'limit': 1})
#     venue_id = venue_info['venues'][0]['id']
#     return venue_info

#returns dictionary where restaurant is key and fs rating is value
def fs_rating_dict(location, restaurant):
    CLIENT_ID = u'0XWYP0COUDY2EOQCU0MUXIBRCFXPQUJRAOGFOHINZUONMSL0'
    CLIENT_SECRET = u'4QJNVNR1ZMZQMIZSHF2FZ3ZEBOORMAG0CAW4J1POQU5Y2UP0'
    client = foursquare.Foursquare(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)

    #get venue id from search
    venue_info = client.venues.search(params={'near': location, 'query': restaurant, 'limit': 1})
    venue_id = venue_info['venues'][0]['id']
    rating_dict = {}
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
    CLIENT_ID = u'0XWYP0COUDY2EOQCU0MUXIBRCFXPQUJRAOGFOHINZUONMSL0'
    CLIENT_SECRET = u'4QJNVNR1ZMZQMIZSHF2FZ3ZEBOORMAG0CAW4J1POQU5Y2UP0'
    client = foursquare.Foursquare(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)

    #get venue id from search
    venue_info = client.venues.search(params={'near': location, 'query': restaurant, 'limit': 1})
    venue_id = venue_info['venues'][0]['id']

    price_tier_dict = {}
    
    if len(venue_info['venues']) == 0:
        price_tier_dict[restaurant] = 1000
        return price_tier_dict
    else:
        venue_id = venue_info['venues'][0]['id']
        details = client.venues(venue_id)
        price = details['venue'].get('price')
        price_tier = price.get('tier')

        if price_tier == None:
            price_tier_dict[restaurant] = 1000
        else:
            price_tier_dict[restaurant] = price_tier
        
        return price_tier_dict



def main():
    # city = input("Enter a city name: ")
    city = 'Ann Arbor'
    offset1 = 0
    
    conn = sqlite3.connect('/Users/kristenpicard/Desktop/ratings.sqlite')
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS YelpRating')
    cur.execute('CREATE TABLE YelpRating (city TEXT, restaurants TEXT, avgrating REAL)')
    cur.execute('DROP TABLE IF EXISTS YelpPrice')
    cur.execute('CREATE TABLE YelpPrice (city TEXT, restaurants TEXT, priceTier TEXT)')
    cur.execute('DROP TABLE IF EXISTS FoursquareRating')
    cur.execute('CREATE TABLE FoursquareRating (city TEXT, restaurants TEXT, avgrating REAL)')
    cur.execute('DROP TABLE IF EXISTS FoursquarePrice')
    cur.execute('CREATE TABLE FoursquarePrice (city TEXT, restaurants TEXT, priceTier INTEGER)')
 
    counter = 0
    
    while counter <= 20:
        if counter == 20:
            offset1 += 20
            break
        
        else:
            params = get_search_parameters(city, offset1)
            yelp_obj = get_yelp_data(params)
            print("Getting results 1-20")
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


            
    # while counter <= 40:
    #     if counter == 40:
    #         offset1 += 20
    #         break
        
    #     else:
    #         param1 = get_search_parameters(city, offset1)
    #         data1 = get_yelp_data(param1)
    #         print("Getting results 21-40")
    #         ratings = rating_dict(data1)
    #         for k, v in ratings.items():
    #             cur.execute('INSERT INTO YelpRating (city, restaurants, avgrating) VALUES (?, ?, ?)', (city, k, v))
    #             fs_obj1 = get_foursquare_object(city, k)
    #             if len(fs_obj1.keys()) == 0:
    #                 cur.execute('INSERT INTO FoursquareRating (city, restaurants, avgrating) VALUES (?, ?, ?)', (city, k, 1000))
    #                 counter += 1
    #             else:
    #                 cur.execute('INSERT INTO FoursquareRating (city, restaurants, avgrating) VALUES (?, ?, ?)', (city, k, fs_obj1[k]))
    #                 counter += 1
        
    # while counter <= 60:
    #     if counter == 60:
    #         offset1 += 20
    #         break
        
    #     else:
    #         param1 = get_search_parameters(city, offset1)
    #         data1 = get_yelp_data(param1)
    #         print("Getting results 41-60")
    #         ratings = rating_dict(data1)
    #         for k, v in ratings.items():
    #             cur.execute('INSERT INTO YelpRating (city, restaurants, avgrating) VALUES (?, ?, ?)', (city, k, v))
    #             fs_obj1 = get_foursquare_object(city, k)
    #             if len(fs_obj1.keys()) == 0:
    #                 cur.execute('INSERT INTO FoursquareRating (city, restaurants, avgrating) VALUES (?, ?, ?)', (city, k, 1000))
    #                 counter += 1
    #             else:
    #                 cur.execute('INSERT INTO FoursquareRating (city, restaurants, avgrating) VALUES (?, ?, ?)', (city, k, fs_obj1[k]))
    #                 counter += 1


    # while counter <= 80:
    #     if counter == 80:
    #         offset1 += 20
    #         break
        
    #     else:
    #         param1 = get_search_parameters(city, offset1)
    #         data1 = get_yelp_data(param1)
    #         print("Getting results 61-80")
    #         ratings = rating_dict(data1)
    #         for k, v in ratings.items():
    #             cur.execute('INSERT INTO YelpRating (city, restaurants, avgrating) VALUES (?, ?, ?)', (city, k, v))
    #             fs_obj1 = get_foursquare_object(city, k)
    #             if len(fs_obj1.keys()) == 0:
    #                 cur.execute('INSERT INTO FoursquareRating (city, restaurants, avgrating) VALUES (?, ?, ?)', (city, k, 1000))
    #                 counter += 1
    #             else:
    #                 cur.execute('INSERT INTO FoursquareRating (city, restaurants, avgrating) VALUES (?, ?, ?)', (city, k, fs_obj1[k]))
    #                 counter += 1
    
    # while counter <= 100:
    #     if counter == 100:
    #         offset1 += 20
    #         break
        
    #     else:
    #         param1 = get_search_parameters(city, offset1)
    #         data1 = get_yelp_data(param1)
    #         print("Getting results 81-100")
    #         ratings = rating_dict(data1)
    #         for k, v in ratings.items():
    #             cur.execute('INSERT INTO YelpRating (city, restaurants, avgrating) VALUES (?, ?, ?)', (city, k, v))
    #             fs_obj1 = get_foursquare_object(city, k)
    #             if len(fs_obj1.keys()) == 0:
    #                 cur.execute('INSERT INTO FoursquareRating (city, restaurants, avgrating) VALUES (?, ?, ?)', (city, k, 1000))
    #                 counter += 1
    #             else:
    #                 cur.execute('INSERT INTO FoursquareRating (city, restaurants, avgrating) VALUES (?, ?, ?)', (city, k, fs_obj1[k]))
    #                 counter += 1
    


    

    #make joined table



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


