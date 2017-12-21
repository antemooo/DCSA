import oauth2 as oauth
import urllib.request as urllib
import json
'''
api_key = "<Enter api key>"
api_secret = "<Enter api secret>"
access_token_key = "<Enter your access token key here>"
access_token_secret = "<Enter your access token secret here>"
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
      self.tweets = open('Tweetoutput.txt', 'a')
      self.hashtag = open('Hashtagoutput.txt', 'a')


  '''
  Construct, sign, and open a twitter request
  using the hard-coded credentials above.
  '''

  def twitterreq(self,url, method , parameters):
    req = oauth.Request.from_consumer_and_token(self._oauth_consumer,
                                                token=self._oauth_token,
                                                http_method=self._http_method,
                                                http_url=url,
                                                parameters=parameters)

    req.sign_request(self._signature_method_hmac_sha1, self._oauth_consumer, self._oauth_token)

    headers = req.to_header()

    if self._http_method == "POST":
      encoded_post_data = req.to_postdata()
    else:
      encoded_post_data = None
      url = req.to_url()

    opener = urllib.OpenerDirector()
    opener.add_handler(self._http_handler)
    opener.add_handler(self._https_handler)

    response = opener.open(url, encoded_post_data)

    return response


  def fetchsamples(self,url,numberoftweets,parameters = [],):
      count = 0
      response = self.twitterreq(url, "GET", parameters)
      for line in response:
          tempJSON = (line.strip()).decode(encoding='utf-8')
          data = json.loads(tempJSON)
          try:
              self.tweets.write(data['text']+";"+"\n")
              print("tweet {0}".format(count))
              for hashtag in (data["entities"]["hashtags"]):
                  if len(hashtag['text']) > 0:
                      self.hashtag.write(hashtag['text'])
                      self.hashtag.write(";" + "\n")
              count+=1
          except:
              pass
          if count >= numberoftweets:
              break
      return count
