from nltk.tokenize import TweetTokenizer
import re
from string import punctuation
from nltk.corpus import stopwords
from nltk.stem.lancaster import LancasterStemmer

'''This script is a helper script used to clean TwitterData'''


'''
Tokenize_Tweet method is a method that is casting TweetTokenizer package to tokenize tweets
Takes a string tweet sentence
removes all users name and links
splits the sentence into a list of words and punctuation
returns the list
'''
def tokenize_tweet(tweet):
    tknzr = TweetTokenizer(reduce_len=True,strip_handles=True)
    return tknzr.tokenize(tweet)

'''
Helper method to remove URLs using regular expressions.
It is aware of http/https.
Takes a string tweet sentence
return string tweet without URLs
'''
def remove_urls(tweet):
    return re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', '', tweet, flags=re.MULTILINE)

'''
remove_stop_words_and_punctuation method.
Takes a list of splitted tweet words.
Removes the punctuation as specified in String class.
Removes all words contains digits through isAlpha method.
remove all stop words defined in NLTK.CORPUS stopwords.
Returns a new list of clean tweets.

NOTE: it is better to use this method on the output of (tokenize_tweet) method
'''
def remove_stop_words_and_punctuation(tweet):
    translator = str.maketrans('', '', punctuation)
    english_stopwords = stopwords.words('english')
    return [word.translate(translator) for word in tweet
            if word.isalpha()
            and word.lower() not in english_stopwords
            and word.translate(translator) != '']

'''
stemming method.
Takes a list of splitted tweet words.
st.stem(word): a process for reducing derived words to their stem, or root form.
E.g. ‘developed’, ‘development’, ‘developing’ are reduced to the stem ‘develop’.
returns a new list of stemmed tweet
'''
def stemming(tweet):
    st = LancasterStemmer()
    return [st.stem(word) for word in tweet]

