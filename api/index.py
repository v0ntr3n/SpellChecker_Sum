from flask import Flask, render_template_string
from flask import Flask, render_template, request, redirect, session
from api.spellcheck.spellchecker import spellChecker
from api.sumarize.summarize import summarize
from json import dumps
app = Flask(__name__)

@app.route('/')
def home():
    return render_template_string(open('Web.html', 'r').read())

@app.route('/sumarize', methods=['POST'])
def handle_post():
    text = request.args['text']
    res = summarize(text)
    return dumps({'response': res})

@app.route('/mistake', methods=['POST'])
def handle_post():
    text : str = request.args['text']
    misspelled = spellChecker.unknown(['something', 'is', 'hapenning', 'here'])
    for word in misspelled:
        # Get the one `most likely` answer
        print(spellChecker.correction(word))

    res = summarize(text)
    return dumps({'response': res})