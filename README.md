# Twitterstream Sentiment-Analysis with Kafka, Spark & Elasticsearch
Reading the Twitterstream from the Twitter-API with Kafka and stream them into an Spark-Cluster to process it

# Things you need

* Installed [Apache Kafka](https://kafka.apache.org/)
* Installed [Apache Spark](https://spark.apache.org/)
* Installed [Elasticsearch & Kibana](https://www.elastic.co/de/) (If you want to)

Twitter Modules
* Tweepy (And your own pair of API Keys from Twitter)
* Kafka-Python
* Pyspark
* Elasticsearch 
* NLTK with VADER

# Base Architecture

Let's dive into the Base Architecture to get an overview of the tools. It's not that complicated.

</br><img src="TwitterstreamArch.jpg" width="800" height=auto />

At the beginning of our journey we have the Twitterusers tweeting some posts with some hashtags. Roumors says there are ~6000 per second.
Twitter offers an API to query them in past for some days or to read the livestream. 

With a Kafka Producer written in Python (use Java or Scala if you want to) we listen the stream and after some cleaning we send the relevant part auf the tweet to our Topic in the Kafkaserver. 

While the Tweets getting send to the topic on the other side of the Kafkaqueue waits the Spark-Consumer. The Spark-Streaming libary has some KafkaUtils to collect the messages from the Kafkaserver and return them into Spark RDDs to process them.

Inside the Spark-Consumer we let the NLTK Vader package doing the Sentiment-Magic and add that result to the data of the tweet.

In the end of a Consumingloop we can send the data to a Elasticsearch-Instance to build some fancy Dashboards to show the result of our tweets and proof that the Tweets are beeing processed in realtime.


# Step 1 - Read the stream

To swim with the twitterstream we need some tools:

* your personal API-Token you can get from Twitter to call the API
* the Python module Tweepy to access the Stream from Python 
* Kafka-Python module to send the tweets to the Kafkaserver

You can find the code here [twitterstreamproducer.py](/code/twitterstreamproducer.py)
