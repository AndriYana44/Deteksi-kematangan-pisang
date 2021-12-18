import os
import numpy
from flask import Flask, render_template, request, flash, redirect, url_for
from flask.sessions import NullSession
from werkzeug.utils import secure_filename
from PIL import Image

UPLOAD_FOLDER = './static/image_upload/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_image(image_path):
    image = Image.open(image_path, "r")
    width, height = image.size
    pixel_values = list(image.getdata())
    channels = 3
    pixel_values = numpy.array(pixel_values).reshape((width, height, channels))
    return pixel_values

def getAverage(item):
    red = 0
    green = 0
    blue = 0
    lenData = 0
    for item1 in item:
        for item2 in item1:
            red += item2[0]
            green += item2[1]
            blue += item2[2]
            lenData += 1
        lenData += 1
    return [round(red/lenData), round(green/lenData), round(blue/lenData)]

@app.route('/', methods=['GET', 'POST'])
def home():
    flash_success = None
    result = None
    filename = None
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash_success = "Uploaded"

            image = get_image(UPLOAD_FOLDER + filename)
            rgb = getAverage(image)

            # cek kematangan berdasarkan warna RGB
            if (rgb[0] - rgb[1]) < 30 and (rgb[0] - rgb[1]) > 11 and rgb[2] > 50 and rgb[2] < rgb[0] and rgb[2] < rgb[1]:
                result = 'sangat matang'
            elif (rgb[0] - rgb[1]) < 12 and (rgb[0] - rgb[1]) > 0  and rgb[2] > 50 and rgb[2] < rgb[0] and rgb[2] < rgb[1]:
                result = 'matang'
            elif (rgb[0] - rgb[1]) < 0 and (rgb[0] - rgb[1]) > -24 and rgb[2] > 50 and rgb[2] < rgb[0] and rgb[2] < rgb[1]:
                result = 'mentah'
            else :
                result = 'tidak terdeteksi'

    return render_template('index.html', flash_success=flash_success, result=result, filename=filename)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8000, debug=True)