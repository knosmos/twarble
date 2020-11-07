import tweepy 

consumer_key = "C9lJMPJ6EI1WdQInKXajX99g9" 
consumer_secret = "jpatKMyLe3kqqCYLvxi0wlWB3iKoA8C5EinjerNfyKccd4rYSe"
access_key = "1325119105888882689-kMRUQHQsNyeNXT2HRxBWZhcnKW5AnM"
access_secret = "NofY4e7pWLfi0exO0sv1RrsiR2MjweCjYcWS8lwC5gQqV"

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