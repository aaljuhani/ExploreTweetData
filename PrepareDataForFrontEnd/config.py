__author__ = 'Asmaa'
TWEETS_FILE_PATH = '../TweetsAnalysis/tweets/'
OUTPUT_FILE_PATH = '../python-gae-quickstart/data/'
DAYS = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
HOURS = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','0']
MISRA_COUNT = 100
'''stop words list'''
file = open("../TweetsAnalysis/stopWords.txt", "r")
cachedStopWords = file.read()