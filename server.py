#!/bin/python

from flask import Flask, Response, render_template, request
import camera

app = Flask(__name__)

def generate_stream(timeout):
    mjpg = camera.MjpegStream(timeout)
    while True:
        frame = mjpg.get_frame()
        if frame:
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/preview', methods=["GET"])
def preview():
    return Response(generate_stream(request.args.get('timeout')),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/capture', methods=["GET"])
def capture():
    return Response(camera.capture_image(), mimetype='image/jpeg')

@app.route('/reset', methods=["GET"])
def reset():
    camera.reset()
    return Response('Camera has been reset.')

@app.route('/cmd', methods=["GET"])
def command():
    text = camera.command(request.args.get('arg'))
    return Response(text, mimetype='text/plain')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

