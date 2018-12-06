from flask import Flask
from flask import render_template
from flask import send_file
from flask import jsonify
import requests
import random
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')
@app.route("/templates/")
def get_image():
    included_extensions = ['jpg', 'jpeg', 'gif', 'bmp', 'png']
    file_names = [f for f in os.listdir('.') if any(f.endswith(ext) for ext in included_extensions)]
    print random.choice(file_names)
    return jsonify(random.choice(file_names))
@app.route("/templates/<filename>")
def give_image(filename=None):
    return send_file(filename)
@app.route("/static/css")
def give_style():
    return send_file('static/style.css')
@app.route("/get_weather")
def get_weather():
    weather = requests.get() #weather api url goes here
    return jsonify(weather.json())
@app.route("/get_logo")
def get_logo():
    return send_file('static/logo.jpg')
@app.route("/get_storage")
def get_storage():
    storage = os.statvfs('.')
    free_storage_float = storage.f_frsize * storage.f_bavail / 1073741824
    free_storage = str(round(free_storage_float, 2))
    return jsonify(free_storage)
