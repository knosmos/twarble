import tweepy, requests

consumer_key = "xxxxx" 
consumer_secret = "xxxxx"
access_key = "xxxxx"
access_secret = "xxxxx"

# auth to consumer key and consumer secret 
auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
auth.set_access_token(access_key, access_secret) 
api = tweepy.API(auth)

class message:
    def __init__(self,name,handle,profile,text,url):
        self.name = name
        self.handle = handle
        self.profile = profile
        self.text = text
        self.url = url
        r = requests.get('https://publish.twitter.com/oembed?url=https://twitter.com/twitter/statuses/'+str(url))
        self.realTweet = r.json()['html']

def removeLinks(input):
    if "http" in input:
        newTweet = input.split()
        for i in newTweet:
            if "http" in i:
                newTweet.remove(i)
        newTweet = " ".join(newTweet)
        return newTweet
    return input

# Function to extract tweets 
def get_tweets(username, number_of_tweets, useLinkRemoval=True):
        global api

        username = username.replace('@','')
        tweets = api.user_timeline(screen_name=username, count=number_of_tweets) 
        
        tweetStrings = []
        tweets_for_csv = [tweet.text for tweet in tweets] # CSV file created
        for j in tweets_for_csv: 
            if (useLinkRemoval):
                temp = removeLinks(j)
            tweetStrings.append(temp)
        
        tweetURLs = []
        tweets_for_URL = [tweet.id for tweet in tweets]
        for j in tweets_for_URL:
            tweetURLs.append(j)
        
        replaces = {'&lt;':'<','&gt;':'>','&amp;':'&'}
        for tweet in tweetStrings:
            for i,j in replaces.items():
                tweet=tweet.replace(i,j)

        user = api.get_user(username)

        temp = user.name
        pfpURL = user.profile_image_url_https

        return [message(temp,username,pfpURL,tweetStrings[t],tweetURLs[t]) for t in range(len(tweetStrings))]

#get_tweets("realDonaldTrump", 5)
