import sys
from flask import Flask, render_template, request
from watson_developer_cloud import ToneAnalyzerV3

app = Flask(__name__)

# ---------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #

@app.route('/', methods=['GET'])
def home():
    return "<h1>hello html</h1>"

# ---------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #

@app.route('/version', methods=['GET'])
def version():
    return sys.version

# ---------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #

@app.route('/add/<int:a>/<int:b>', methods=['GET'])
def add(a, b):
    return str(a + b)

# ---------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #

@app.route('/pow', methods=['GET'])
def get_pow():
    return render_template('pow.html')

@app.route('/pow', methods=['POST'])
def post_pow():
    b = int(request.values['base'])
    e = int(request.values['exp'])
    r = b ** e
    return render_template('pow.html', r=r)

# ---------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #

@app.route('/tone', methods=['GET'])
def get_tone():
    return render_template('tone.html', tones=[])

@app.route('/tone', methods=['POST'])
def post_tone():
    u = '5b091126-a4af-4353-99d0-cbd004157df9'
    p = '1OBplj7RTAfq'
    v = '2016-05-19'
    text = request.values['text']
    t = ToneAnalyzerV3(username=u, password=p, version=v)
    d = t.tone(text)
    for tone in d['document_tone']['tone_categories']:
        if tone['category_id'] == 'emotion_tone':
            tones = tone['tones']
    return render_template('tone.html', tones=tones)

# ---------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #

app.run(host='0.0.0.0', port=3333, debug=True)

# DEBUGGING
# from IPython import embed; embed()
# print('my dictionary', request.values)
