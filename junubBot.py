###********** START **********
###********** START **********
###********** START **********
###********** Import all the needed **********
import tweepy #Library for interacting with Twitter
from tweepy import Stream #For streaming tweets
from tweepy import OAuthHandler # handles Authentication
from tweepy.streaming import StreamListener #To listen on live tweets
from tweepy import API #Twitter API to interact with Twitter
from tweepy import Cursor #For returning data object to be looped through. Not used though
from os import environ #For keeping secret keys - so that no one sees them on GitHub

###********** Authentication Keys **********
CONSUMER_KEY = environ['CONSUMER_KEY']
CONSUMER_SECRET = environ['CONSUMER_SECRET']
ACCESS_KEY = environ['ACCESS_KEY']
ACCESS_SECRET = environ['ACCESS_SECRET']

###********** Authentication **********
auth = tweepy.OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY,ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)

###********** Build a streamListener class that will listen to tweets based on a track list **********
class StreamListener(tweepy.StreamListener):
    #The first method is the constructor, which takes the API for Authentication
    def __init__(self, api):
        self.api = api
        self.me = api.me()

    #There are mainly 2 methods
    #The on_data methods is good for returning or updating a data file. on_status does the opposite
    def on_status(self, status):
        #Ignores the tweet so long as I am the Author, or it's a reply to a tweet
        if status.in_reply_to_status_id is not None or \
            status.user.id == self.me.id:
            return

        #Otherwise if a tweet that meets the criteria isn't liked yet, then it should be liked *favourite()*
        if not status.favorited:
            try:
                status.favorite()
            except Exception as e:
                print("Error on_data %s" % str(e))
                return True
        #If the tweet is not retweeted, retweet() method is called.
        if not status.retweeted:
            try:
                status.retweet()
            except:
                print("Error on_data %s" % str(e))
                return True
        print(status.text) #Prints the text of the tweet. This can be commented out after deploying
        #print(dir(status))

    #status code 420 prevents our code from reaching Twitter limits and warnings.
    def on_error(self, status_code):
        if status_code == 420:
            return False

#Calling the class
stream_listener = StreamListener(api)
#Connecting the listener to the Stream
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
#Passing a items into a list that will be used as a track list. The bot retweets anything that mentions the following
ssd_list = ["South Sudan","south sudan","#SouthSudan","#southsudan","#SSOT", "#ssot", "@junuBot"]
#The dot filter method takes one parameter, the list to be tracked.
stream.filter(track= ssd_list)
###********** END **********
###********** END **********
###********** END **********
