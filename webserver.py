import json
import random
import asyncio
import concurrent
import time
import os
from unipath import Path
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, abort
from flask_socketio import SocketIO, send, emit
from config import *

UPLOAD_FOLDER = 'static/img'
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = SECRET_KEY
socketio = SocketIO(app)

#
# URL Routing
#

# Index Page
@app.route('/')
def index():
    menu = [
        {"name": "Time Series" , "url": "/time" },
        {"name": "3D Surface" , "url": "/surface" },
        {"name": "Spotlight" , "url": "/spotlight" },
        {"name": "Trail" , "url": "/trail" },
        {"name": "Heatmap" , "url": "/heatmap" }
    ]
    return render_template('index.html', menu=menu)

# Time Series Page
@app.route('/time')
def timeseries():
    return render_template('timeseries.html')

# Surface plot
@app.route('/surface')
def surface():
    return render_template('surface.html')

# Spotlight plot
@app.route('/spotlight')
def spotlight():
    return render_template('spotlight.html')

# Trail plot
@app.route('/trail')
def trail():
    return render_template('trail.html')

# Trail plot
@app.route('/heatmap')
def heatmap():
    return render_template('heatmap.html')

# Default context vars for all templates
@app.context_processor
def inject_defaults():
    return { "table_width": TABLE_WIDTH, 'table_depth': TABLE_DEPTH }

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    saveRoot = os.path.join(os.path.dirname(os.path.realpath(__file__)), app.config['UPLOAD_FOLDER'])
    msg = ''
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            if "spotlight" in request.form:
                filename = "spotlight.jpg"
            elif "trail" in request.form:
                filename = "trail.jpg"
            else:
                abort(500)
            file.save(Path(saveRoot).child(filename))
            msg = 'Image uploaded: '+filename

    return render_template('settings.html', message=msg)

# Message receivers
#

# All messages with unknown event
@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)


# Test event
@socketio.on('new_serial_data')
def handle_json(json):
    send_json(json)
    print('received json: ' + str(json))

#
# Send Message
#

def send_json(jsondata):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    socketio.emit('update', { 'timestamp': timestamp, 'data': jsondata })

#
# Start App
#

if __name__ == '__main__':
    app.debug = True
    socketio.run(app, port=WEB_SERVER_PORT)





