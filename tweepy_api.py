import tweepy
import json

# Twitter API Credentials (Replace with your keys)
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAOLgzAEAAAAAy3slyQQtp2ZIsrJ84zPfBh1634g%3Do4Th8VNBLdiN7IWnbJFFYWvnNNRpgdIj3TbzQWOeuweiot2c3J"

# Authenticate with Twitter API
client = tweepy.Client(bearer_token=BEARER_TOKEN)

# Search Query for Wildfires in California
query = "California wildfire OR #CAwildfires OR #CaliforniaFires -is:retweet"

# Fetch recent tweets (max 10 tweets)
tweets = client.search_recent_tweets(query=query, tweet_fields=["created_at", "text", "author_id"], max_results=1)

# Display the fetched tweets
for tweet in tweets.data:
    print(f"User ID: {tweet.author_id}\nTime: {tweet.created_at}\nTweet: {tweet.text}\n{'-'*50}")
