import tweepy
from textblob import TextBlob
import csv
import sys

#these are essential, code will not execute without!

consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

if len(sys.argv) != 2:
    print("Proper syntax is analysis.py arg1")
    print("arg1: the query you want to search for")
    exit()

with open('sentiment.csv', mode="w", encoding='utf-8') as file:
    #these counters will keep track of what the sentiment feels
    positive = 0
    negative = 0
    #open csvwriter
    writer = csv.writer(file, delimiter=',')

    #loop through the tweets and collect data
    try:
        for tweet in tweepy.Cursor(api.search,
                                   q=sys.argv[1],
                                   count = 200,
                                   result_type = 'recent').items():
            blob = TextBlob(tweet.text)
            print(blob)
            print(blob.sentiment)
            #if there is any usable data in the sentiment and polarity we will write it to the CSV
            if blob.sentiment.polarity != 0 and blob.sentiment.subjectivity != 0:
                #determine sentiment
                if blob.sentiment.polarity > 0.0 and blob.sentiment.subjectivity > 0.3:
                    positive += 1
                elif blob.sentiment.polarity < 0.0 and blob.sentiment.subjectivity > 0.3:
                    negative += 1
                #export data to CSV
                writer.writerow([blob, blob.sentiment])

        #At the end we will export the counters for positive and negative sentiment
        writer.writerow(["Positive: ", positive, "Negative: ", negative])
        #output to terminal for user
        print("Positive Tweets: " + str(positive))
        print("Negative Tweets: " + str(negative))

    #catch any errors. the most common one will be that users do not put in their credentials
    except tweepy.TweepError as error:
        if '401' in str(error):
            print("Missing or incorrect authentication credentials. Please open analysis.py and add in proper credentials")
        else:
            print(error)