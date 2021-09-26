import sys
import os
import json
import requests
import logging
import tweepy


def get_auth():
    '''
    Read the authenication credientals from the envrinment vriable.
    Exception will be raised if any of the given key dis not exists. 
    '''
    auth_data = {}
    auth_data['consumer_key'] = os.environ['TWITTER_CONSUMER_KEY']
    auth_data['consumer_secret'] = os.environ['TWITTER_CONSUMER_SECRET']
    auth_data['access_key'] = os.environ['TWITTER_ACCESS_KEY']
    auth_data['access_secret'] = os.environ['TWITTER_ACCESS_SECRET']
    return auth_data


def _main(handle: str):
    auth_data = get_auth()

    auth = tweepy.OAuthHandler(auth_data['consumer_key'], ['consumer_secret'])
    auth.set_access_token(auth_data['access_key'], ['access_secret'])
    api_client = tweepy.API(auth)

    all_tweets = [i._json for i in api_client.user_timeline(
        screen_name=handle, count=200)]

    with open("twitter-dump-{}.json".format(handle), mode="w") as f:
        json.dump(all_tweets, f)


def _test():
    pass


if __name__ == "__main__":
    handle = sys.argv[1]
    _main(handle)
