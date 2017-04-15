import pullTweets
import time
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

pullTweets.main()
@sched.scheduled_job('interval', minutes=5)
def timed_job():
    print time.strftime('%Y-%m-%d %H:%M:%S',  time.localtime(time.time())) +' : Job started'
    pullTweets.main()
    print time.strftime('%Y-%m-%d %H:%M:%S',  time.localtime(time.time())) +' : Job Ended'

# @sched.scheduled_job('cron', day_of_week='*', hour='*', minute=1, second=10)
# def scheduled_job():
#     #pullTweets.main()
#     print('This job is run every weekday at 10am.')

#sched.configure(options_from_ini_file)
sched.start()