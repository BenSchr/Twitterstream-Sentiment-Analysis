from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from kafka import KafkaProducer
import json
from datetime import datetime
from datetime import timezone

access_token = "Get this from twitter"
access_token_secret =  "and this"
consumer_key =  "and this"
consumer_secret =  "and this"




def cleantweet(data):
    rawtweet = json.loads(data)
    tweet={}
    tweet["date"] = datetime.strptime(rawtweet["created_at"],'%a %b %d %H:%M:%S %z %Y')\
        .replace(tzinfo=timezone.utc).astimezone(tz=None).strftime('%Y-%m-%d %H:%M:%S')
    tweet["user"] = rawtweet["user"]["screen_name"]
    if "extended_tweet" in rawtweet:
        tweet["text"] = rawtweet["extended_tweet"]["full_text"]
    else:
        tweet["text"] = rawtweet["text"]
    return json.dumps(tweet)



class StdOutListener(StreamListener):
    def on_data(self, data):
        newdata = cleantweet(data)
        producer.send("tweets", newdata)
        print(newdata)
        return True
    def on_error(self, status):
        print (status)



producer = KafkaProducer(bootstrap_servers='YourHostWithKafka:9092', api_version=(0, 10, 1),value_serializer=lambda m: json.dumps(m).encode('ascii'))
l = StdOutListener()
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
stream = Stream(auth, l,tweet_mode='extended')
stream.filter(track=["#worldkidnessday"], languages=["en"])

