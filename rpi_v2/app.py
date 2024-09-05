from flask import Flask, render_template
import json

app = Flask(__name__)

def getURL():
    try:
        with open("../../config.json") as f:
            data = json.load(f)
        return data.get("urls").get("face_api")
    except:
        with open("config.json") as f:
            data = json.load(f)
    return data.get("urls").get("face_api")

@app.route('/')
def index():
    return render_template('index.html', api = getURL())

@app.route('/start',methods=['POST'])
def start():
    return render_template('index.html', api = getURL())

@app.route('/stop',methods=['POST'])
def stop():
    return render_template('stop.html')

if __name__=='__main__':
    app.run(debug=True, use_reloader=False, port=7000)