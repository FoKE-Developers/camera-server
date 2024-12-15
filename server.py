#!/bin/python

from flask import Flask, Response, render_template, send_file, request
import camera

app = Flask(__name__)
camera.reset()

def generate_stream(video):
    while True:
        frame = video.get_frame()
        if frame:
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        else:
            return b'--frame--\r\n\r\n'

@app.route('/preview', methods=["GET"])
def preview():
    try:
        video = camera.MjpegVideo(request.args.get('timeout'))
    except IOError as err:
        return Response(str(err), 503, mimetype='text/plain')
    except Warning as out:
        return Response(str(out), 504, mimetype='text/plain')

    return Response(generate_stream(video),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/capture', methods=["GET"])
def capture():
    try:
        return Response(camera.capture_image(), mimetype='image/jpeg')
    except IOError as err:
        return Response(str(err), 503, mimetype='text/plain')

@app.route('/capture/latest', methods=["GET"])
def latest_capture():
    try:
        return send_file(camera.LATEST_IMAGE, mimetype='image/jpeg')
    except IOError as err:
        return Response(str(err), 503, mimetype='text/plain')

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
    app.run(host='0.0.0.0', port=8080)

