from flask import Flask, request, render_template
from synonymizer import synonymize
import twitter

app = Flask(__name__)
@app.route('/', methods = ['GET','POST'])
def index():
    if request.method == 'POST':
        handle = request.form['handle']
        tweets = twitter.get_tweets(handle,5)
        for tweet in tweets:
            tweet.text = synonymize(tweet.text)
        return render_template('index.html',messages=tweets)
    # Fetch five random handles from the list
    return render_template('index.html',messages=[])

@app.route('/about', methods = ['GET'])
def about(): return render_template('about.html')

@app.route('/synonymizer', methods = ['GET','POST'])
def synonym():
    if request.method == 'POST':
        text = request.form['text']
        return render_template('synonymize.html',translation=synonymize(text))
    return render_template('synonymize.html')

if __name__ == '__main__':
    app.run('0.0.0.0')