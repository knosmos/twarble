import requests
import random

def pick(words):
    # Picks the most obnoxious word out of the list of words.
    # Remove any words that are multiple words to avoid confusion
    words = [word for word in words if word.count(' ')==0]
    return random.choice(sorted(words[:30],key=len,reverse=True)[:3])

def loadNoTranslate():
    global noTranslate
    with open('notranslate.txt','r') as fIn:
        noTranslate = set(fIn.read().split('\n'))

loadNoTranslate()

def translate(word,absurdity=0.7):
    global noTranslate
    # Is it a number?
    try:
        if int(word.replace(',','')):
            return word
    except:
        pass
    # To maintain semblance of cohesiveness, some words are not translated
    if random.random() > absurdity: return word
    # I don't want to deal with contractions
    if "'" in word:return word
    # Copy original formatting
    capitalized = word[0].isupper()
    allcaps = word.isupper()
    #if capitalized and not allcaps: return word # Ensure names are not changed
    word = word.lower()
    punctuation = ''
    if word[-1] in ['!','.',',','?',';']:
        punctuation = word[-1]
        word = word[:-1]
    if word in noTranslate:
        if capitalized: word = word.capitalize()
        if allcaps: word = word.upper()
        return word+punctuation
    # Send request to API
    r = requests.get('http://api.datamuse.com/words?ml='+word)
    words = [w['word'] for w in r.json()]
    if len(words) == 0:
        # No synonyms
        if capitalized: word = word.capitalize()
        if allcaps: word = word.upper()
        return word+punctuation
    res = pick(words)
    # Add original formatting
    if capitalized: res = res.capitalize()
    if allcaps: res = res.upper()
    res += punctuation
    return res

def fixGrammar(words):
    # Ensure that "a" precedes a consonant and "and" precedes a vowel
    vowels = ['a','e','i','o','u']
    for w in range(len(words)-1):
        if words[w] == 'an' and words[w+1][0] not in vowels:
            words[w] = 'a'
        if words[w] == 'a' and words[w+1][0] in vowels:
            words[w] = 'an'
    return words

def synonymize(text):
    # Parses text and replaces each word with its worst synonym
    res = list(map(translate,text.split()))
    res = fixGrammar(res)
    return ' '.join(res)

#print(synonymize("I WON THIS ELECTION, BY A LOT!"))