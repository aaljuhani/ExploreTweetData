import csv
from config import TWEETS_FILE_PATH
from config import OUTPUT_FILE_PATH
from config import DAYS
from config import HOURS

from countTweets import countTweets
from misra import misra
from misra import misra_day
from misra import misra_hour

class ComputeData():

    def countTweets(self,d,h):
        countTweets(d,h)
        return

    def run_misra(self,d,h):
        if d == 'all':
            misra_hour(h)
        elif h == "all":
            misra_day(d)
        else:
            misra(d,h)
        return

    def run_mincount(self,d,h):
        return

    def write_file_headers(self):
        # headers for tweets count
        with open(OUTPUT_FILE_PATH+'tweetcounts.csv', 'w') as outcsv:
            writer = csv.writer(outcsv)
            writer.writerow(["day", "time", "count"])

        with open(OUTPUT_FILE_PATH+'misra.csv', 'w') as outcsv:
            writer = csv.writer(outcsv)
            writer.writerow(["day", "time", "word","count"])
        return


def main():
    compute_data = ComputeData()
    compute_data.write_file_headers()

    for d in DAYS:
        for h in HOURS:
            print d,h
            compute_data.countTweets(d,h)
            compute_data.run_misra(d,h)
            compute_data.run_mincount(d,h)

    # run for all days
    for d in DAYS:
        compute_data.run_misra(d,'all')
    #run for all hours
    for h in HOURS:
        compute_data.run_misra('all',h)

    return

main()