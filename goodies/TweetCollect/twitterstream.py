import oauth2 as oauth
import urllib.request as urllib
import json
import re
from string import punctuation
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer

'''
api_key = "<Enter api key>"
api_secret = "<Enter api secret>"
access_token_key = "<Enter your access token key here>"
access_token_secret = "<Enter your access token secret here>"
HTTP_method is GET by default, otherwise the method should be specified.
'''

class TwitterStream:
  def __init__(self,api_key,api_secret,access_token_key,access_token_secret,debug = 0,http_method = "GET"):
      self._api_key = api_key
      self._api_secret = api_secret
      self._access_token_key = access_token_key
      self._access_token_secret = access_token_secret
      self._debug = debug
      self._oauth_token = oauth.Token(key= self._access_token_key, secret=self._access_token_secret)
      self._oauth_consumer = oauth.Consumer(key=self._api_key, secret=self._api_secret)
      self._signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()
      self._http_method = http_method
      self._http_handler = urllib.HTTPHandler(debuglevel=self._debug)
      self._https_handler = urllib.HTTPSHandler(debuglevel=self._debug)
      # files initialize to None in the beginning. However fetchsamples will initialize them.
      self.tweets = None
      self.hashtag = None


  '''
  Construct, sign, and open a twitter request 
  using the class-given credentials above.
  '''

  def twitterreq(self,url, parameters, method = None):
    #if the method not specified use the GET method as default
    if method == None:
          method = self._http_method
    req = oauth.Request.from_consumer_and_token(self._oauth_consumer,
                                                token=self._oauth_token,
                                                http_method=method,
                                                http_url=url,
                                                parameters=parameters)

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

    response = opener.open(url, encoded_post_data)

    return response


#FetchSamples is connecting to Twitter Stream API and fetching Tweets & HashTags
#Url with flitering symbols should be specified
#numberoftweets is the number of tweets wanted before terminating
  def fetchsamples(self,url,numberoftweets,parameters = []):
      self.tweets = open('Tweetoutput1.txt', 'a')
      self.hashtag = open('Hashtagoutput1.txt', 'a')
      count = 0
      response = self.twitterreq(url, parameters)
      for line in response:
          #Convert from Byte_List to JSON format
          tempJSON = (line.strip()).decode(encoding='utf-8')
          data = json.loads(tempJSON)
          try:
              self.tweets.write(data['text']+";"+"\n")
              hashtagsLength = 0
              #looping on each hashtag object in the JSON file and store the text into a newline
              for hashtag in (data["entities"]["hashtags"]):
                  if len(hashtag['text']) > 0:
                      hashtagsLength += len(hashtag['text'])
                      self.hashtag.write(hashtag['text'] + ",")
              if hashtagsLength > 0:
                  self.hashtag.write(";" + "\n")
                  hashtagsLength = 0
              print("tweet {0}".format(count))
              count+=1
          except:
              pass
          if count >= numberoftweets:
              break
      return count

  def clean_tweets(self):
      result = []
      tweets = open("Tweetoutput1.txt", 'r')
      for tweet in tweets:
          tweet_token = tokenize_tweet(tweet)
          content = remove_stop_words_and_punctuation(tweet_token)
          result.append(content)
      return result




def tokenize_tweet(tweet):
    tknzr = TweetTokenizer(reduce_len=True,strip_handles=True)
    return tknzr.tokenize(tweet)


def remove_urls(tweet):
    return re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', '', tweet, flags=re.MULTILINE)

def remove_stop_words_and_punctuation(tweet):
    translator = str.maketrans('', '', punctuation)
    english_stopwords = stopwords.words('english')
    return [word.translate(translator) for word in tweet
            if word.isalpha()
            and word.lower() not in english_stopwords
            and word.translate(translator) != '']