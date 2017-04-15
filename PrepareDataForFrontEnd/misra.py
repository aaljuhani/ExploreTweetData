import numpy
from config import TWEETS_FILE_PATH
from config import DAYS
from config import HOURS
from config import MISRA_COUNT
from config import OUTPUT_FILE_PATH
from config import cachedStopWords
import csv
import re
from collections import Counter

class MisraGries(object):
# source: https://github.com/kalaidin/data-streams-algorithms/blob/master/misragries.py
    def __init__(self, k):
        self.k = k
        self.a = Counter()

    def process(self, stream):
        for j in stream:
            if j in self.a:
                self.a.update([j])
            elif len(self.a) < self.k - 1:
                self.a[j] = 1
            else:
                for l in self.a.keys():
                    self.a[l] -= 1
                    if self.a[l] == 0:
                        del self.a[l]

    def estimate(self, q):
        return self.a[q] if q in self.a else 0


def misra(day,time):
    tweet_file = TWEETS_FILE_PATH+day+'_'+time+'.csv'
    with open(tweet_file) as t_file:
        tweets = t_file.read()
        clean_tweets = re.sub('[^A-Za-z0-9#@_]+', ' ', tweets.lower())
        tweet_bow = [word.encode("utf-8") for word in clean_tweets.split() if word not in cachedStopWords]

    mg = MisraGries(MISRA_COUNT)
    mg.process(tweet_bow)
    misra_count = open(OUTPUT_FILE_PATH+'misra.csv', 'a')
    for key, count in mg.a.iteritems():
        misra_count.write(day+','+time+','+key+','+str(count)+'\n')
    return

def misra_day(day):
    #combine files
    with open(OUTPUT_FILE_PATH+'tweets/'+day+'.csv', 'w') as output:
        for h in HOURS:
            with open(TWEETS_FILE_PATH+day+'_'+h+'.csv',) as d_hour:
                for line in d_hour:
                    output.write(line)

    with open(OUTPUT_FILE_PATH+'tweets/'+day+'.csv') as t_file:
        tweets = t_file.read()
        clean_tweets = re.sub('[^A-Za-z0-9#@_]+', ' ', tweets.lower())
        tweet_bow = [word.encode("utf-8") for word in clean_tweets.split() if word not in cachedStopWords]

    mg = MisraGries(MISRA_COUNT)
    mg.process(tweet_bow)
    misra_count = open(OUTPUT_FILE_PATH+'misra.csv', 'a')
    for key, count in mg.a.iteritems():
        misra_count.write(day+',all,'+key+','+str(count)+'\n')
    return

def misra_hour(hour):
     #combine files
    with open(OUTPUT_FILE_PATH+'tweets/'+hour+'.csv', 'w') as output:
        for d in DAYS:
            with open(TWEETS_FILE_PATH+d+'_'+hour+'.csv',) as d_hour:
                for line in d_hour:
                    output.write(line)

    with open(OUTPUT_FILE_PATH+'tweets/'+hour+'.csv') as t_file:
        tweets = t_file.read()
        clean_tweets = re.sub('[^A-Za-z0-9#@_]+', ' ', tweets.lower())
        tweet_bow = [word.encode("utf-8") for word in clean_tweets.split() if word not in cachedStopWords]

    mg = MisraGries(MISRA_COUNT)
    mg.process(tweet_bow)
    misra_count = open(OUTPUT_FILE_PATH+'misra.csv', 'a')
    for key, count in mg.a.iteritems():
        misra_count.write('all,'+hour+','+key+','+str(count)+'\n')
    return