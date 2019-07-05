from flask import Flask, request, Response, url_for, redirect, render_template, json, send_from_directory
from werkzeug import secure_filename

import os
import os.path

TIME_DELAY = 5

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads/'

app.config['ALLOWED_EXTENSIONS'] = set(['jpg', 'jpeg'])

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/upload', methods=['POST', 'GET'])
def upload():
    global TIME_DELAY
    TIME_DELAY = str(request.form['timeDelay'])
    
    fileDir = os.path.dirname(os.path.realpath(__file__))
    DIR = os.path.join(fileDir, 'uploads')
    os.system('rm ' + DIR + '/*.jpg')
    print DIR
    
    uploaded_files = request.files.getlist("file[]")
    print uploaded_files
    filenames = []
    i = 0
    for file in uploaded_files:
        if file and allowed_file(file.filename):
            filename = str(i) + '.jpg'
            i += 1
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print os.path.join(app.config['UPLOAD_FOLDER'], filename)
            filenames.append(filename)
            print filenames
    return '<html><head><h3>Successfully uploaded</h3></head></html'

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/upload/check', methods = ['POST'])
def check():
    fileDir = os.path.dirname(os.path.realpath(__file__))
    DIR = os.path.join(fileDir, 'uploads')
    count = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
    return json.dumps({'count':count, 'delay':TIME_DELAY})

if __name__ == '__main__':
    app.run(threaded = True, debug = True, host = '0.0.0.0', port = 5001)