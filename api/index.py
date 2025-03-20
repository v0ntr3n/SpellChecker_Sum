from flask import Flask, render_template_string
from flask import Flask, request
from api.spellcheck.spellchecker import spellChecker
from api.spellcheck.utils import prepare_text_for_spell_check, correct_original_text
from api.sumarize.summarize import summarize
from json import dumps, loads
app = Flask(__name__)

@app.route('/')
def home():
    return render_template_string(open('Web.html', 'r').read())

@app.route('/sumarize', methods=['POST'])
def handle_post():
    data = loads(request.data.decode('utf-8'))
    text = data['text']
    res = summarize(text)
    return dumps({'summary': res})

@app.route('/mistake', methods=['POST'])
def handle_post2():
    data = loads(request.data.decode('utf-8'))
    text = data['text'].strip()

    prepared_words, word_mapping = prepare_text_for_spell_check(text)
    misspelled = spellChecker.unknown(prepared_words)
    response, correction_mapping = correct_original_text(text, misspelled, word_mapping, spellChecker.correction)
    return dumps({'response': response, 'corections' : correction_mapping})


app.run(debug=True)
