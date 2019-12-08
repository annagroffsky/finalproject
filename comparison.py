import matplotlib
import matplotlib.pyplot as pyplot

# power ratings 
r = arrange(5, 10, 15, 20)
c = arrange(10, 20, 30, 40, 50)

plt.bar(r,c, align="center", alpha = 0.5)
plt.xticks(r, c)

plt.xlabel('Power Rating')
plt.ylabel('# of AA Restaurants')
plt.title ('AA Restaurant Power Ratings')
plt.show()

# 4s vs yelp
r = 
c =

plt.plot(r,c)

plt.xlabel('Yelp')
plt.ylabel('Foursquare')
plt.title('Yelp vs Foursquare Reviews')
plt.show()


#cur.fetchall() = list of tuples of each row 

#https://www.dataquest.io/blog/python-pandas-databases/