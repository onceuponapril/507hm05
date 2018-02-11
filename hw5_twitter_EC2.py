from requests_oauthlib import OAuth1
import json
import sys
import requests
import secret_data # file that contains OAuth credentials

userid= sys.argv[1]

consumer_key = secret_data.CONSUMER_KEY
consumer_secret = secret_data.CONSUMER_SECRET
access_token = secret_data.ACCESS_KEY
access_secret = secret_data.ACCESS_SECRET

#Code for OAuth starts
url = 'https://api.twitter.com/1.1/account/verify_credentials.json'
auth = OAuth1(consumer_key, consumer_secret, access_token, access_secret)
requests.get(url, auth=auth)

CACHE_FNAME = 'twitter_cache_EC2.json '
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
        CACHE_DICTION[unique_ident]['cache_timestamp'] = datetime.now().timestamp()
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close()
        newfile=open('tweet.json','w')
        newfile.write(dumped_json_cache)
        newfile.close()

        return CACHE_DICTION[unique_ident]

def get_tweets():
    baseurl='https://api.twitter.com/1.1/statuses/user_timeline.json'
    params={}
    params['user_id']=userid
    return make_request_using_cache(baseurl, params)




MAX_STALENESS = 30
def is_fresh(cache_entry):
    now = datetime.now().timestamp()
    staleness = now - cache_entry['cache_timestamp']
    return staleness > MAX_STALENESS

if __name__ == "__main__":
    if not consumer_key or not consumer_secret:
        print("You need to fill in client_key and client_secret in the secret_data.py file.")
        exit()
    if not access_token or not access_secret:
        print("You need to fill in this API's specific OAuth URLs in this file.")
        exit()
