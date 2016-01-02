#!usr/bin/env python

import tweepy
import pandas as pd
import matplotlib.pyplot as plt
from credentials import *

# get API connection set up
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

# assign a twitter user and create the lists that will contain the data
twitterid = "kbcclibrary"
tweets2014 = []
tweets2015 = []
tweets2016 = []

# make the API call and sort the data by year
for tweet in tweepy.Cursor(api.user_timeline, include_rts=True,
                           id=twitterid).items():
    if tweet.created_at.year == 2016:
        tweets2016.append(tweet.created_at)
        print(tweet.created_at)
    elif tweet.created_at.year == 2015:
        tweets2015.append(tweet.created_at)
        print(tweet.created_at)
    elif tweet.created_at.year == 2014:
        tweets2014.append(tweet.created_at)
        print(tweet.created_at)
    else:
        print("error")

# create the DataFrame
d = {'Tweets2014': tweets2014, 'Tweets2015': tweets2015,
     'Tweets2016': tweets2016}
df = pd.DataFrame.from_dict(data=d, orient='index')
df = df.transpose()

# turn dates into just months
df['Tweets2014'] = pd.to_datetime(df.Tweets2014).dt.month
df['Tweets2015'] = pd.to_datetime(df.Tweets2015).dt.month
df['Tweets2016'] = pd.to_datetime(df.Tweets2016).dt.month

# count the number of occcurences of each month
df['Tweets2014'] = df['Tweets2014'].value_counts()
df['Tweets2015'] = df['Tweets2015'].value_counts()
df['Tweets2016'] = df['Tweets2016'].value_counts()

# slice out the part of DataFrame we want to plot
df = df[1:13]

# put the columns in the right order
df = df.reindex_axis(sorted(df.columns), axis=1)

# plot the chart; add title
ax = df.plot(kind='bar', title='Tweets per month')

# name the axes and ticks
ax.set_xlabel('month')
ax.set_ylabel('tweets')
plt.xticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], ['Jan', 'Feb', 'Mar',
                                                    'Apr', 'May', 'Jun',
                                                    'Jul', 'Aug', 'Sep',
                                                    'Oct', 'Nov', 'Dec'])
# show the chart
plt.show()
