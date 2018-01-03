import oauth2 as oauth
import urllib.request as urllib
import json
from TweetsCleaner import tokenize_tweet,remove_stop_words_and_punctuation
'''Following the best practices and code design guidelines. 
    It is advised to cast the code in the Object oriented way.
    Our Twitter Stream class is a simple class that is providing the basic functionality to gather data from Twitter's API
    The main class should be initialised with API key, API secret, Access token key and Acess token secret.
    The different methods will be explained individually
    The class returns Tweets and Hashtags by default'''

# To start the streamer directly:
#  - uncomment the following and enter the correct data
#  - uncoment the lines after if __name__ == '__main__':
'''
api_key = "<Enter api key>"
api_secret = "<Enter api secret>"
access_token_key = "<Enter your access token key here>"
access_token_secret = "<Enter your access token secret here>"
url = https://stream.twitter.com/1.1/statuses/filter.json
numberoftweets = 1000
# HTTP_method is GET by default, otherwise the method should be specified.
'''

class TwitterStream:
    def __init__(self,api_key,api_secret,access_token_key,access_token_secret,debug = 0,http_method = "GET"):
        self._api_key = api_key
        self._api_secret = api_secret
        self._access_token_key = access_token_key
        self._access_token_secret = access_token_secret
        self._debug = debug
        # Initialise te OAUTH token
        self._oauth_token = oauth.Token(key= self._access_token_key, secret=self._access_token_secret)
        # Initialise the OAUTH consumer
        self._oauth_consumer = oauth.Consumer(key=self._api_key, secret=self._api_secret)
        # Get the connection signature
        self._signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()
        # Initialise the HTTP handler
        self._http_method = http_method
        self._http_handler = urllib.HTTPHandler(debuglevel=self._debug)
        self._https_handler = urllib.HTTPSHandler(debuglevel=self._debug)
        # files initialize to None in the beginning. However fetchsamples will initialize them.
        self.tweets = None
        self.hashtags = None

    '''
       Construct, sign, and open a twitter request 
       using the class-given credentials above.
    '''
    def twitterreq(self,url, parameters, method = None):
        #if the method not specified use the GET method as default
        if method == None:
            method = self._http_method
        # Make OAUTH request for the prespecified data
        req = oauth.Request.from_consumer_and_token(self._oauth_consumer,
                                                    token=self._oauth_token,
                                                    http_method=method,
                                                    http_url=url,
                                                    parameters=parameters)
        # Account sign-in
        req.sign_request(self._signature_method_hmac_sha1, self._oauth_consumer, self._oauth_token)
        headers = req.to_header()
        if method == "POST":
            encoded_post_data = req.to_postdata()
        else:
            encoded_post_data = None
            url = req.to_url()
        opener = urllib.OpenerDirector()
        opener.add_handler(self._http_handler)
        opener.add_handler(self._https_handler)

        # Start collecting data through open stream socket
        response = opener.open(url, encoded_post_data)

        return response


        #FetchSamples is connecting to Twitter Stream API and fetching Tweets & HashTags
        #Url with filtering symbols should be specified
        #numberoftweets is the number of tweets wanted before terminating
    def fetchsamples(self,url,numberoftweets,parameters = []):
        self.tweets = open('Tweetoutput.txt', 'a')
        self.hashtags = open('Hashtagoutput.txt', 'a')
        count = 0
        response = self.twitterreq(url, parameters)
        #Convert each response line from Byte_List to JSON format
        for line in response:
            tempJSON = (line.strip()).decode(encoding='utf-8')
            data = json.loads(tempJSON)
            # Try catch block to avoid empty tweets and convertion rubbish
            try:
                # Write each tweet in tweets file
                if len(data['text']) > 0:
                    self.tweets.write(data['text'] + "\n")
                #looping on each hashtag object in the JSON file and store the hashtag text into a newline
                for hashtag in (data["entities"]["hashtags"]):
                    # Check if there is a hashtag to store
                    if len(hashtag['text']) > 0:
                        # Store each hashtag in a newline
                        self.hashtags.write(hashtag['text'] + "\n")
                print("tweet {0}".format(count))
                count+=1
            except:
                pass
            # If the number of the specified tweets is reached.
            # Close the files and stop collecting data.
            # The response socket will stop automatically.
            if count >= numberoftweets:
                self.tweets.close()
                self.hashtags.close()
                break
        return count

    '''
      This method is used to clean twitter data.
      It uses the TweetsCleaner script.
      The method takes:
      (optionally) tweets input file.
      (optionally) text output file. 
      NOTE: 
      If no input or output files specified.
      it will open the file from the class that is created in FetchSamples method.
      Then it will store the data in a list and return a list as output
      '''
    def clean_tweets(self,InputFileName = None, OutputFileName = None):
        # List to store the clean tweets
        result = []
        # If no input file specified, set the default
        if InputFileName == None:
            InputFileName = 'Tweetoutput.txt'
        # If no output file specified, set a new file
        if OutputFileName == None:
            OutputFileName = 'CleanTweets.txt'
        # Open both files, one to read, one to write
        input_tweets = open(InputFileName, 'r')
        output_tweets = open(OutputFileName, 'a')
        # Loop over all input tweets
        for tweet in input_tweets:
            # Tokenize tweets, returns a list
            tweet_token = tokenize_tweet(tweet)
            # remove stop word, punctuation and words with digits from the list
            content = remove_stop_words_and_punctuation(tweet_token)
            # Check if the tweet list still has words
            # Because some tweets for example are just links so they will be cleaned.
            if len(content) > 0:
                # append the clean tweet as a sublist of words in the result list
                result.append(content)
                # rejoin the list of words into a string and write it in the file
                output_tweets.write(" ".join(content) + "\n")
        input_tweets.close()
        output_tweets.close()
        return result


if __name__ == '__main__':
    '''
    mytweet = TwitterStream(api_key=api_key,
                            api_secret=api_secret,
                            access_token_key=access_token_key,
                            access_token_secret=access_token_secret,
                            debug = 0,
                            http_method = "GET")
    mytweet.fetchsamples(url = url, numberoftweets = numberoftweets)
    '''
