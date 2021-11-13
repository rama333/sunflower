from flask import Flask, jsonify, request
from flask_cors import CORS
from os.path import join, dirname, realpath
from werkzeug.utils import secure_filename
import cv2
import numpy as np
import json

UPLOADS_PATH = join(dirname(realpath(__file__)), 'static\\img')

app = Flask(name)
CORS(app)
@app.route("/api/sunflower", methods=['POST'])
def sunflower():
    if request.files['image'].filename != '':
        image = request.files['image']
        image.save(os.path.join(UPLOADS_PATH, secure_filename(image.filename)))

        img = cv2.imread(os.path.join(UPLOADS_PATH, secure_filename(image.filename)), 0)
        cimg = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

        circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 5,
                                   param1=118, param2=8, minRadius=0, maxRadius=7)

        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            cv2.circle(cimg, (i[0], i[1]), i[2], (0, 255, 0), 1)
            cv2.circle(cimg, (i[0], i[1]), 2, (0, 0, 255), 1)

        return jsonify({
            "count_seeds": circles.shape
        })
    else:
        return jsonify({
            "error": "bad request / not image"
        })

if name == 'main':
    app.run()
    print("Server listening on port 5000")




