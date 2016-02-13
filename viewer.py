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

# make the API call and sort the data by year
tweets = []
for tweet in tweepy.Cursor(api.user_timeline, include_rts=True,
                           id=twitterid).items():
    tweets.append((tweet.created_at.year, tweet.created_at.month))

# create the DataFrame
df = pd.DataFrame(data=tweets)
df = df.groupby([0, 1]).size()

years = range(2006, 2016)
months = range(1, 13)

for year in years:
    for month in months:
        print year, month
        try:
            df[year, month]
        except IndexError and KeyError:
            df.loc[year, month] = 0
        else:
            pass
    if df.sum(level=0)[year] == 0:
        df.drop(year, inplace=True)
        
df.sort_values()

ax = df.plot(kind='bar', title='Tweets per month')

# name the axes and ticks
ax.set_xlabel('months')
ax.set_ylabel('tweets')

# show the chart
plt.show()
