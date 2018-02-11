from requests_oauthlib import OAuth1
import json
import sys
import requests
import secret_data # file that contains OAuth credentials
import nltk # uncomment line after you install nltk
from nltk.probability import FreqDist

## SI 206 - HW
## COMMENT WITH:
## Your section day/time:
## Any names of people you worked with on this assignment:

#usage should be python3 hw5_twitter.py <username> <num_tweets>
username = sys.argv[1]
num_tweets = sys.argv[2]

consumer_key = secret_data.CONSUMER_KEY
consumer_secret = secret_data.CONSUMER_SECRET
access_token = secret_data.ACCESS_KEY
access_secret = secret_data.ACCESS_SECRET

#Code for OAuth starts
url = 'https://api.twitter.com/1.1/account/verify_credentials.json'
auth = OAuth1(consumer_key, consumer_secret, access_token, access_secret)
requests.get(url, auth=auth)
#Code for OAuth ends


#Write your code below:
#Code for Part 3:Caching
#Finish parts 1 and 2 and then come back to this


CACHE_FNAME = 'twitter_cache.json '
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()


except:
    CACHE_DICTION = {}


def params_unique_combination(baseurl, params):
    alphabetized_keys = sorted(params.keys())
    res = []
    for k in alphabetized_keys:
        res.append("{}-{}".format(k, params[k]))
    return baseurl + "_".join(res)


def make_request_using_cache(baseurl, params):
    unique_ident = params_unique_combination(baseurl,params)

    if unique_ident in CACHE_DICTION:
        print("Getting cached data...")
        return CACHE_DICTION[unique_ident]

    else:
        print("Making a request for new data...")
        resp = requests.get(baseurl,params,auth=auth)
        CACHE_DICTION[unique_ident] = json.loads(resp.text)
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close()
        newfile=open('tweet.json','w')
        newfile.write(dumped_json_cache)
        newfile.close()

        return CACHE_DICTION[unique_ident]



#Code for Part 1:Get Tweets
def get_tweets():
    baseurl='https://api.twitter.com/1.1/statuses/user_timeline.json'
    params={}
    params['count']=num_tweets
    params['screen_name']=username
    # r = requests.get(baseurl, params=params,auth=auth)
    return make_request_using_cache(baseurl, params)


# print(rtext)
# json.loads(r.text)



#Code for Part 2:Analyze Tweets
rtext=get_tweets()
token=""
for dict in rtext:
    token+=dict['text']
     # token +=str(dict['text'])

# print(token)
tokens=nltk.word_tokenize(token)


# # # Step 4: Ignore stop words (1) ignore any words that do not start with an alphabetic character [a-zA-Z], (2) ignore 'http', 'https', and 'RT' (these show up a lot in Twitter)
alpha=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x'
,'y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W'
,'X','Y','Z']
ignore=['http', 'https','RT']
newlist=[]
for item in tokens:
      # for string in item:
          if item[0] in alpha and item not in ignore:
                                newlist.append(item)
# print(newlist)

# #
# #PART2
fdist = FreqDist()
for word in newlist:
#       for word in lst:
          fdist[word]+=1
# #
# # # Step 4: Print the 5 most frequently used words using the frequency distribution you just created.
print(fdist.most_common(5))

# extra1
# Twitter Boggle: Take two twitter accounts and analyze their tweets to find words they have in common and words that are unique to each account. Show the 5 most frequent different (unique) words for each account and the 5 most frequent common words (shared by both).

if __name__ == "__main__":
    if not consumer_key or not consumer_secret:
        print("You need to fill in client_key and client_secret in the secret_data.py file.")
        exit()
    if not access_token or not access_secret:
        print("You need to fill in this API's specific OAuth URLs in this file.")
        exit()
