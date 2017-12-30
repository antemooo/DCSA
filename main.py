from TwitterStream import TwitterStream
api_key = "ODdfd2wlcHddZ2j85sWwjYC4T"
api_secret = "JqwVeggPEiccVfBdqKMo6Z32ULnYn1oofCfAZT9gSBPfVzv4BH"
access_token_key = "943584485433585666-tYTBJJECOwGAqMUnFW4v4xJ9unVhHz2"
access_token_secret = "vtObMVSeO98Twtqcgbq22zd1uxjwPnkHwXhOkNN4nD72N"

url = "https://stream.twitter.com/1.1/statuses/filter.json?locations=-122.995004,32.323198,-67.799695,49.893813 & language=en"

mytweet = TwitterStream(api_key=api_key,
                        api_secret=api_secret,
                        access_token_key=access_token_key,
                        access_token_secret=access_token_secret,
                        debug = 0,
                        http_method = "GET")

mytweet.fetchsamples(url = url, numberoftweets = 150)

output = mytweet.clean_tweets()