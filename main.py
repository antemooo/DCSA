from TwitterStream import TwitterStream
api_key = "Put the api key here"
api_secret = "Put the api secret here"
access_token_key = "Put the token key here"
access_token_secret = "Put the token secret here"

url = "https://stream.twitter.com/1.1/statuses/filter.json?locations=-122.995004,32.323198,-67.799695,49.893813 & language=en"

mytweet = TwitterStream(api_key=api_key,
                        api_secret=api_secret,
                        access_token_key=access_token_key,
                        access_token_secret=access_token_secret,
                        debug = 0,
                        http_method = "GET")

mytweet.fetchsamples(url = url, numberoftweets = 25000)

output = mytweet.clean_tweets()