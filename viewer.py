#!usr/bin/env python

print("loading libraries...")

from datetime import date
import tweepy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
from credentials import *

print("setting up the api call...")

# get API connection set up
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

if len(sys.argv) != 2:
    sys.exit('Usage: python viewer.py <username>')

# assign a twitter user
twitterid = sys.argv[1] 

print("fetching data...")

# make the API call and sort the data by year
tweets = []
for tweet in tweepy.Cursor(api.user_timeline, include_rts=True,
                           id=twitterid).items():
    tweets.append((tweet.created_at.year, tweet.created_at.month))

print("processing data...")
# create the DataFrame
df = pd.DataFrame(data=tweets)
df = df.groupby([0, 1]).size()

years = range(2006, date.today().year + 1)
months = range(1, 13)

# for months without a value, add a zero value
for year in years:
    for month in months:
        try:
            df[year, month]
        except IndexError and KeyError:
            df.loc[year, month] = 0
        else:
            pass
# exclude years where all months are zero
    if df.sum(level=0)[year] == 0:
        df.drop(year, inplace=True)

# sort the data; set the chart type
df = df.sort_index()
ax = df.plot(kind='bar', width=1, title='Tweets per month by: '+ twitterid)

# name the axes and ticks
ax.set_xlabel('months')
ax.set_ylabel('tweets')
plt.xticks(np.arange(0, len(df), 12),
           range(df.index[0][0], df.index[len(df) - 1][0] + 1, 1))

# show thechart
plt.show()
