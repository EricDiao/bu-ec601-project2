import sys
import os
import json
import requests
import logging

from google.cloud import language_v1


def _main(fname, lang):
    with open(fname) as f:
        content = f.read()

    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(
        content=content, type_=language_v1.Document.Type.PLAIN_TEXT)

    r = client.analyze_sentiment(
        request={'document': document})

    sentiment = r.document_sentiment
    print("Overall Sentiment: {}, {}".format(
        sentiment.score, sentiment.magnitude))

    senteces = r.sentences
    for s in senteces:
        print("="*80)
        print("Sentence:", s.text.content)
        print("Sentiment: {}, {}".format(
            s.sentiment.score, s.sentiment.magnitude))


if __name__ == "__main__":
    fname = sys.argv[1]
    _main(fname, lang="en")
