# DCSA
Distributed computing and storage architecture project

Copyright ©VUB - Distributed computing and storage architecture course 2017.

**Authors:** 
- **Ahmed K. A Abdullah @github/antemooo.**
- **Rencong Tang @github/rencongtang.**


An example to deploy end-to-end big data harvesting. 

The data will be processed later in Hadoop cluster through a simple Map-Reduce program to count the 10 maximum words in a chunk of tweets and hashtags.

**The example is written and tested with Python 3.5**

--------------------------------------------------------------------------------------------

-----------------------------
## To setup the dependencies: 
-----------------------------

`pip3 install -r requirements.txt`

OR

`pip install -r requirements.txt`

--------------------------------------------------------------------------------------------

----------
## main.py
----------

A full example is established.

Only **api_key, api_secret, access_token_key and access_token_secret** must be assigned.

A well-explained example of how to obtain these keys can be found [here](http://docs.inboundnow.com/guide/create-twitter-application/).

**To run the code:**

`python3 main.py`

The script will produce 3 .txt files:

- Tweetoutput.txt: contains the raw tweets as gathered from Twitter.

- CleanTweets.txt: contains tweets without links, users, punctuation and English-stopwords

- Hashtagoutput.txt: contains per-line hashtags collected out of the tweets

-------------------
## TwitterStream.py
-------------------

A class contains the basic method needed to connect to Twitter's stream API.

The main class should be initialised with:

- **API key**.

- **API secret**.

- **Access token key**.

- **Acess token secret**.

A well-explained example of how to obtain these keys can be found [here](http://docs.inboundnow.com/guide/create-twitter-application/).

--------------------
###### fetchsamples:
--------------------
The main method to collect data from the API.

The method takes: 
- an URL with a specified filter. 
- the number of tweets to collect.
- an optional list of parameters.

**The filter can be either specified directly on the URL** e.g. `https://stream.twitter.com/1.1/statuses/filter.json?track=twitter`, or in the list of the parameters.

Another example is:

`url = "https://stream.twitter.com/1.1/statuses/filter.json?locations=-122.995004,32.323198,-67.799695,49.893813 & language=en"`

This one yield tweets from a specific location in the US and only tweets in English.

For further information check Twitter developers documentation [here](https://developer.twitter.com/en/docs/tweets/filter-realtime/api-reference/post-statuses-filter.html).

--------------------
###### clean_tweets:
--------------------
A method to clean the collected tweets.

It uses methods from **TweetsCleaner** script.

The method takes:

- **(optionally)** tweets input file.

- **(optionally)** text output file. 

**NOTE:** 
      If no input or output files specified.
      The method will open the file from the class that is created in FetchSamples method.
      It will also make a new output file called CleanTweets.txt.
      Then it will store the data in a list and return a list as output.

--------------------
## TweetsCleaner.py
--------------------

A simple script that contains different method to extract only useful data from tweets.

Some of these methods are wrappers for other methods from the [NLTK](http://www.nltk.org) toolkit. 

The script itself is well documented and each method has a comment explaining the functionality.

-----------------
## map_reduce.py
-----------------

A simple Map-Reduce implementation to count the maximum 10 used words in a file.

The **MRMostUsedWord** inherits **MRjob**

The code is well documented in the script.

The script can be modified for any other functionality.

For more information check the comments inside the script or [MRjob](https://pythonhosted.org/mrjob/index.html) documentation.

**To run locally:**

Input_File_Name : should be .txt, .csv, etc.

`python3 map_reduce.py "Input_File_Name"`

**To run on Hadoop:**

Input_File_Name & Output_File_Name : should be .txt, .csv, etc.

Hadoop_Dir: should be a directory in the HDFS

Other_Dir: a specified directory from the user to dump the output file. (this could be ignored)

`python3 map_reduce.py -r hadoop "Input_File_Name"`

`python3 map_reduce.py -r hadoop "Input_File_Name" —output-dir "Hadoop_Dir" > "Other_Dir"/"Output_File_Name"`







