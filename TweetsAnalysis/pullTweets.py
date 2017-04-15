from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream, API
#from twitter_key import *
from twitter_key2 import *
from datetime import datetime
import json
from countminsketch import CountMinSketch
from pytz import timezone
from datetime import datetime
from dateutil.parser import parse
import pandas as pd
from email.utils import parsedate_tz, mktime_tz
import re
import time
import logging
from httplib import IncompleteRead  # Python 2
import urllib3.exceptions
from urllib3.exceptions import ReadTimeoutError


''' Twitter dat time format'''
fmt = "%a %b %d %H:%M:%S +0000 %Y"

''' Get the current name of the week'''
current_day = datetime.now(timezone('EST')).strftime("%A")

''' Get the current time of the day'''
current_hour = datetime.now(timezone('EST')).hour

''' misra-gries '''

'''stop words list'''
file = open("stopWords.txt", "r")
cachedStopWords = file.read()

'''logger '''
logging.basicConfig()
logger = logging.getLogger('countingTweets')
hdlr = logging.FileHandler('countTweet.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)

''' Class to get Twitter streem'''


class TweetStreamListener(StreamListener):
    def __init__(self, start_time, time_limit=240):
        self.time = start_time
        self.limit = time_limit
        self.finish = start_time + time_limit
        self.tweet_count = 0
        ''' File name to be set when we get the first tweet of the stream'''
        self.fileName = ''
        ''' count min sketch'''
        self.tweetsWordsCount = CountMinSketch(100, 10)


    # on success
    def on_data(self, data):
        try:
            ''' load tweet json'''
            tweet = json.loads(data)
            ''' convert tweet time from UTC to EST "Newyork time""'''
            tweet_time = tweet['created_at']
            timestamp = mktime_tz(parsedate_tz(tweet_time))
            eastern_dt = datetime.fromtimestamp(timestamp, timezone('America/New_York'))
            ny_local_time = eastern_dt.strftime(fmt)

            ''' Get the current name of the week'''
            current_day = eastern_dt.strftime("%A")

            ''' Get the current time of the day'''
            current_hour = eastern_dt.hour

            '''file name'''
            self.fileName = current_day + '_' + str(current_hour)

            '''load data of same day and hour into countmin tables'''
            self.tweetsWordsCount.loadDataToTables(self.fileName)

            ''' save original tweets -without urls '''
            saveFile = open('tweets/' + self.fileName + '.csv', 'a')
            saveFile.write(re.sub(r"http\S+", "", tweet['text']).encode("utf-8"))
            saveFile.write('\n')
            saveFile.close()

            ''' clean tweet'''
            tweetText = tweet['text'].lower()
            noURLtweet = re.sub(r"http\S+", "", tweetText)
            nospcialChar = re.sub('[^A-Za-z0-9#@_]+', ' ', noURLtweet)
            tweet_bow = [word.encode("utf-8") for word in nospcialChar.split() if word not in cachedStopWords]
            # print 'bow:', tweet_bow

            ''' update counter'''
            self.tweet_count += 1

            '''count each word in a tweet'''
            for w in tweet_bow:
                self.tweetsWordsCount.add(w)

            if (time.time() > self.finish):
                print "time done"
                logger.info("time done")
                logger.info("Number of tweets is: " + str(self.tweet_count))
                ''' save tables in a file'''
                self.tweetsWordsCount.saveDataToFile(self.fileName)
                logger.info("count min are saved")
                # self.time = time.time()
                self.tweet_count = 0
                return False

            return True

        except BaseException, e:
            print 'failed ondata,' + str(e)
            time.sleep(5)
            pass


    # on failure
    def on_error(self, status):
        print (datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ":  Error receiving data " )
        logger.info("Number of tweets is: " + str(self.tweet_count))
        ''' save tables in a file'''
        self.tweetsWordsCount.saveDataToFile(self.fileName)
        logger.error("error streaming: " + status)
        return


def main():
    try:
        logger.info("Script started")
        start_time = time.time()  # grabs the system time
        listener = TweetStreamListener(start_time)
        # set twitter keys/tokens
        auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
        stream = Stream(auth, listener)
        ''' Get tweets from Newyork'''
        stream.filter(languages=["en"], locations=[-74, 40, -73, 41])
    except IncompleteRead:
        # Oh well, reconnect and keep trucking
        logger.error('Incomplete read')
        listener.tweetsWordsCount.saveDataToFile(listener.fileName)
        logger.info('save data after Incomplete read error caught')
    except ReadTimeoutError:
        logger.error('Read time out error')
        listener.tweetsWordsCount.saveDataToFile(listener.fileName)
        logger.info('save data after Read time out error caught')
    except KeyboardInterrupt:
        # Or however you want to exit this loop
        listener.tweetsWordsCount.saveDataToFile(listener.fileName)
        logger.info('save data after keyword interrupt')
        stream.disconnect()

