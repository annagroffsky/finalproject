import requests
import json
import unittest
import os

#define a function to go through the yelp api-produce a dictionary of key: restuarant name, value: # of 5 star reviews 

#define a function to go through the twitter api-take in the keys from the yelp and create either another value w/ follower or a separate dict

#define a function that graphs both sets of values on the same graph 

#define a function that combines number of reviews vs number of 5 stars-sort from highest to lowest based on value

#visualizatoins: 1. scatterplot of # of followers vs # of 5 stars 2. map showing dots of restaurants relative to their cumulative score



base_url="https://api.twitter.com/1.1/friends/list.json" 
