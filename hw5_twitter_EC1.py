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
# username = sys.argv[1]
# num_tweets = sys.argv[2]

consumer_key = secret_data.CONSUMER_KEY
consumer_secret = secret_data.CONSUMER_SECRET
access_token = secret_data.ACCESS_KEY
access_secret = secret_data.ACCESS_SECRET

#Code for OAuth starts
url = 'https://api.twitter.com/1.1/account/verify_credentials.json'
auth = OAuth1(consumer_key, consumer_secret, access_token, access_secret)
requests.get(url, auth=auth)
#Code for OAuth ends


# Extra one
def compare_tweets(username, num_tweets):
    baseurl='https://api.twitter.com/1.1/statuses/user_timeline.json'
    params={}
    params['count']=num_tweets
    params['screen_name']=username
    r = requests.get(baseurl, params=params,auth=auth)
    anatext=r.text

    jdump=json.dumps(anatext)
    opfile=open(username,'w')
    opfile.write(jdump)
    opfile.close()
    return anatext

textone=compare_tweets('realDonaldTrump',10)
texttwo=compare_tweets('HillaryClinton',10)

tokensone=nltk.word_tokenize(textone)
tokenstwo=nltk.word_tokenize(texttwo)

commonlst={}
uniquelst={}

for word in tokensone:
    if word in tokenstwo:
        if word in commonlst:

            commonlst[word]+=1
        else:
            commonlst[word]=1
    else:
        if word in uniquelst:
            uniquelst[word]+=1
        else:
            uniquelst[word]=1

for word in tokenstwo:
    if word not in tokensone:
        if word in uniquelst:
            uniquelst[word]+=1
        else:
            uniquelst[word]=1



fiveunique=sorted(uniquelst.items(),key=lambda x:x[1],reverse=True)[:5]
fivecommon=sorted(commonlst.items(),key=lambda x:x[1],reverse=True)[:5]

print(fiveunique)
print(fivecommon)




if __name__ == "__main__":
    if not consumer_key or not consumer_secret:
        print("You need to fill in client_key and client_secret in the secret_data.py file.")
        exit()
    if not access_token or not access_secret:
        print("You need to fill in this API's specific OAuth URLs in this file.")
        exit()
