import sys
from flask import Flask, render_template, request
from watson_developer_cloud import ToneAnalyzerV3, LanguageTranslatorV2, VisualRecognitionV3

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

@app.route('/translate', methods=['GET'])
def get_translate():
    return render_template('translate.html', tones=[])

@app.route('/translate', methods=['POST'])
def post_translate():
    u = 'c2b1bcd1-7ffe-4299-b7e0-061313b808c9'
    p = 'N7XheyFtb4qs'
    text = request.values['text']
    t = LanguageTranslatorV2(username=u, password=p)
    o = t.translate(text=text, source='en', target='es')
    return render_template('translate.html', o=o, text=text)

# ---------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #

@app.route('/visual', methods=['GET'])
def get_visual():
    return render_template('visual.html', klasses=[])

@app.route('/visual', methods=['POST'])
def post_visual():
    k = '70b9662c2397b6513d9c084ea9217c4c6f80e9a2'
    v = '2016-05-19'
    url = request.values['url']
    vis = VisualRecognitionV3(api_key=k, version=v)
    o = vis.classify(images_url=url)
    klasses = o['images'][0]['classifiers'][0]['classes']
    return render_template('visual.html', url=url, klasses=klasses)

# ---------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #

app.run(host='0.0.0.0', port=3333, debug=True)

# DEBUGGING
# from IPython import embed; embed()
# print('my dictionary', request.values)
