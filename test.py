from flask import Flask, request, Response, url_for, redirect, render_template, json, send_from_directory

app = Flask(__name__)

@app.route('/')
def index():
    return "<HTML><head><h1>Hi</h1></head></HTML>"


if __name__ == '__main__':
    app.run(threaded = True, debug = True, host = '0.0.0.0', port = 5001)