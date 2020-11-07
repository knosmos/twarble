from flask import Flask, request, render_template
from synonymizer import synonymize
import twitter
import random

app = Flask(__name__)

# Get handles for frontpage
with open('maintwitterhandles.txt','r') as fIn:
    mainhandles = fIn.read().split()

@app.route('/', methods = ['GET','POST'])
def index():
    if request.method == 'POST':
        handle = request.form['handle']
        tweets = twitter.get_tweets(handle,5)
        for tweet in tweets:
            tweet.text = synonymize(tweet.text)
        return render_template('index.html',messages=tweets)
    # Fetch five random handles from the list
    handles = random.sample(mainhandles,5)
    tweets = []
    for handle in handles:
        tweet = twitter.get_tweets(handle,1)[0]
        tweet.text = synonymize(tweet.text)
        tweets.append(tweet)
    return render_template('index.html',messages=tweets)

@app.route('/about', methods = ['GET'])
def about(): return render_template('about.html')

@app.route('/synonymizer', methods = ['GET','POST'])
def synonym():
    if request.method == 'POST':
        text = request.form['text']
        return render_template('synonymizer.html',translation=synonymize(text),text=text)
    return render_template('synonymizer.html')

if __name__ == '__main__':
    app.run('0.0.0.0')