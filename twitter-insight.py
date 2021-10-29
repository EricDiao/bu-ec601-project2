import sys
import os
import json
import requests
from pprint import pprint
import logging
import tweepy

from google.cloud import language_v1


def avg(x): return sum(x)/len(x)


def _twitter_get_auth():
    '''
    Read the authenication credientals from the envrinment vriable.
    Exception will be raised if any of the given key dis not exists.
    '''
    auth_data = {}
    auth_data['consumer_key'] = os.environ['TWITTER_CONSUMER_KEY']
    auth_data['consumer_secret'] = os.environ['TWITTER_CONSUMER_SECRET']
    auth_data['access_key'] = os.environ['TWITTER_ACCESS_KEY']
    auth_data['access_secret'] = os.environ['TWITTER_ACCESS_SECRET']
    auth_data['GOOGLE_APPLICATION_CREDENTIALS'] = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
    return auth_data


def _google_sentiment_range_from_score(score: float) -> str:
    if score < -0.25:
        return "NEGATIVE"
    elif score < 0.25:
        return "NEUTUAL"
    else:
        return "POSTIVE"


def _obtain_tweets_under_hashtag(hashtag: str, client: tweepy.API) -> list:
    ret = []
    for tweet in tweepy.Cursor(client.search_30_day, label="dev", query="#{}".format(hashtag)).items(limit=128):
        this_tweet = {
            "text": tweet.text,
            "time": tweet.created_at,
            "lang": tweet.lang
        }
        ret.append(this_tweet)
    return ret


def _run_sentiment_analysis(tweets: list):
    client = language_v1.LanguageServiceClient()

    for tweet in tweets:
        document = language_v1.Document(
            content=tweet['text'], type_=language_v1.Document.Type.PLAIN_TEXT)

        try:
            r = client.analyze_sentiment(
                request={'document': document})

            sentiment = r.document_sentiment
            tweet['sentiment'] = {
                "magnitude": sentiment.magnitude,
                "score": sentiment.score
            }
        except Exception as e:
            logging.error("Failed to analysis a tweet: {}".format(e))
            tweet['sentiment'] = {
                "magnitude": 0,
                "score": 0
            }

        # print(tweet['text'])
        # print("-"*80)
        # print("Overall Sentiment: {}, {}".format(
        #     sentiment.score, sentiment.magnitude))
        # print("="*80)


def _agg_analysis_result(tweets: list):
    scores = []
    magnitudes = []

    for tweet in tweets:
        scores.append(tweet['sentiment']['score'])
        magnitudes.append(tweet['sentiment']['magnitude'])

    avg_score = avg(scores)
    avg_magnitude = avg(magnitudes)

    print("Overall sentiment over the hashtag is {}, with score {}.".format(
        _google_sentiment_range_from_score(avg_score), avg_score))


def _main(hashtag: str):
    logging.warning(
        "Analysis latest Twitters under hashtag #{}.".format(hashtag))

    try:
        auth_data = _twitter_get_auth()
    except Exception as e:
        logging.error("Failed to gather authenication data: {}".format(e))
        exit(-1)

    try:
        auth = tweepy.OAuthHandler(
            auth_data['consumer_key'], auth_data['consumer_secret'])
        auth.set_access_token(
            auth_data['access_key'], auth_data['access_secret'])
        api_client = tweepy.API(auth)
    except Exception as e:
        logging.error("Failed to authenicate: {}".format(e))
        exit(-1)

    tweets = _obtain_tweets_under_hashtag(hashtag, api_client)
    logging.warning("{} tweets obtained.".format(len(tweets)))

    _run_sentiment_analysis(tweets)

    _agg_analysis_result(tweets)


def _show_usage():
    assert len(sys.argv) >= 1
    print("Usage:", file=sys.stderr)
    print("", file=sys.stderr)
    print("{} <hashtag>\n".format(sys.argv[0]), file=sys.stderr)
    print("Do remember to set the envrinment variables.", file=sys.stderr)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        hashtag = sys.argv[1]
    else:
        _show_usage()
        exit(-1)

    _main(hashtag)
