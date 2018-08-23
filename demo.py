import csv
import pandas
import tweepy
from textblob import TextBlob

tok = pandas.read_csv('/home/dave/Documents/tokens.csv')
# Step 1 - Authenticate

consumer_key = tok.iat[0,0]
consumer_secret = tok.iat[0,1]
access_token = tok.iat[0,2]
access_token_secret = tok.iat[0,3]


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

#Step 3 - Retrieve Tweets
#public_tweets = api.search('Trump')

public_tweets = tweepy.Cursor(api.search, q="Trump", rpp=100, count=20, result_type="recent", include_entities=True, lang="en").items(200)

#CHALLENGE - Instead of printing out each tweet, save each Tweet to a CSV file
#and label each one as either 'positive' or 'negative', depending on the sentiment 
#You can decide the sentiment polarity threshold yourself


def weight_sent(num):
    if num < 0:
        weight = 'negative'
    elif num > 0:
        weight = 'positive'
    else:
        weight = 'neutral'
    return weight


with open('trump_csv.csv', 'w', newline='') as csvfile:
    the_writer = csv.writer(csvfile)

    the_writer.writerow(['tweet', 'polarity', 'subjectivity', 'classification'])

    for tweet in public_tweets:
        tweetText = tweet.text
        analysis = TextBlob(tweetText)
        sentAnaly = analysis.sentiment

        weight = weight_sent(sentAnaly[0])

        roundPol = "{0:.2f}".format(sentAnaly[0])
        roundSub = "{0:.2f}".format(sentAnaly[1])

        the_writer.writerow([tweetText, roundPol, roundSub, weight])

df = pandas.read_csv('trump_csv.csv')

bin = pandas.value_counts(df['classification'])
print(bin)
