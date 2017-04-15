from config import TWEETS_FILE_PATH
from config import OUTPUT_FILE_PATH
import csv

'''
In this code we want to count how many tweets for hour per day
'''
def countTweets(day,time):
    num_lines = sum(1 for line in open(TWEETS_FILE_PATH+day+'_'+time+'.csv'))
    print num_lines
    #write result in tweet_count file
    t_count = open(OUTPUT_FILE_PATH+'tweetcounts.csv', 'a')
    t_count.write(day+','+time+','+str(num_lines)+'\n')
    return
