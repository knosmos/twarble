from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from synonymizer import synonymize
import twitter
import random
import os, datetime

app = Flask(__name__)

# Set up chatroom database
app.config['SECRET_KEY'] = 'you-will-never-guess'

db = SQLAlchemy(app)
migrate = Migrate(app,db)
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or \
    'sqlite:///' + os.path.join(basedir, 'app2.db')

SQLALCHEMY_TRACK_MODIFICATIONS = False

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
        t = twitter.get_tweets(handle,1)
        if len(t)>0:
            tweet = t[0]
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

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(140), index=True, unique=False)
    original = db.Column(db.String(140), index=True, unique=False)
    timestamp = db.Column(db.String(64), index=True, unique=False)
    def __repr__(self):
        return '<Post {}>'.format(self.content)

def add_post(content,timestamp):
    global db
    original = content
    content = synonymize(content)
    print(content)
    post = Post(content=content,original=original,timestamp=timestamp)
    db.session.add(post)
    db.session.commit()

def get_posts():
    posts = Post.query.all()
    return posts[::-1]

@app.route('/chat',methods=['GET','POST'])
def chat():
    posts = get_posts()
    if request.method == 'POST':
        new_post = request.form['text']
        if new_post == '':
            return redirect(url_for('chat'))
        timestamp = datetime.date.today().strftime("%m/%d/%Y")
        add_post(new_post,timestamp)
        return redirect(url_for('chat'))
    return render_template('chatroom.html',posts=posts)

@app.route('/chat/del')
def delete():
    db.create_all()
    posts = Post.query.all()
    for p in posts:
        db.session.delete(p)
    db.session.commit()
    db.create_all()
    return redirect(url_for('index'))

if __name__ == '__main__':
    db.create_all()
    app.run('0.0.0.0')