import json
import requests
import os
import http.client, urllib.parse
import logging

# send logs to cloudwatch
logger = logging.getLogger("handler_logger")
logger.setLevel(logging.DEBUG)

def news(event, context):
    # event = json.loads(event)
    lan = event['pathParameters']['lan']
    headlines = []
    print(lan)
    news_key = os.environ.get('API_SECRET_KEY')

    # retrieving the news

    conn = http.client.HTTPConnection('api.mediastack.com')

    params = urllib.parse.urlencode({
        'access_key': news_key,
        'categories': 'general',
        'sort': 'published_desc',
        'languages': lan,
        'limit': 10,
    })

    conn.request('GET', '/v1/news?{}'.format(params))

    res = conn.getresponse()
    news = res.read()

    news = (news.decode('utf-8'))
    news_json = json.loads(news)
    # print(news_json)
    # print(news_json['data'][0]['title'])
    num_articles = news_json['pagination']['count']

    for n in range(0, num_articles):
        headlines.append(news_json['data'][n]['title'])

    return {
        'statusCode': 200,

        'body': json.dumps(headlines)
    }
