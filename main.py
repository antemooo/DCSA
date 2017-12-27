from DCSA.goodies.TweetCollect.twitterstream import TwitterStream
mytweet = TwitterStream(api_key="ODdfd2wlcHddZ2j85sWwjYC4T",
                        api_secret="JqwVeggPEiccVfBdqKMo6Z32ULnYn1oofCfAZT9gSBPfVzv4BH",
                        access_token_key="943584485433585666-tYTBJJECOwGAqMUnFW4v4xJ9unVhHz2",
                        access_token_secret="vtObMVSeO98Twtqcgbq22zd1uxjwPnkHwXhOkNN4nD72N",
                        debug = 0,
                        http_method = "GET")
# mytweet.fetchsamples(url = "https://stream.twitter.com/1.1/statuses/filter.json"
#                            "?locations=-122.995004,32.323198,-67.799695,49.893813 & language=en",
#                      numberoftweets = 5000)


output = mytweet.clean_tweets()
print(output)
file = open("output_tweet.txt",'a')
for tweet in output:
    if len(tweet) > 0 :
        file.write(" ".join(tweet) + '\n')
