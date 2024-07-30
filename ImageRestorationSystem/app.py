from flask import Flask, request, jsonify, send_file, render_template, send_from_directory
from werkzeug.utils import secure_filename
import os
import numpy as np
from keras.models import load_model
from PIL import Image

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['OUTPUT_FOLDER'] = 'uploads/output_images'

model = load_model(os.path.join(app.config['UPLOAD_FOLDER'], 'autoencoder_model.h5'))

def preprocess_image(image_path):
    image = Image.open(image_path).convert('L')
    image = image.resize((28, 28))
    image = np.array(image) / 255.0
    image = image.reshape(1, 28, 28, 1)
    return image

def save_image(image_array, output_path, size=(224, 224)):
    image_array = image_array.reshape(28, 28) * 255.0
    image = Image.fromarray(image_array).convert('L')
    image = image.resize(size, Image.NEAREST)  # Resize to a larger size
    image.save(output_path)



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/file-upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify(status="error", message="No file part")
    
    file = request.files['file']
    if file.filename == '':
        return jsonify(status="error", message="No selected file")
    
    if file:
        filename = secure_filename(file.filename)
        original_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(original_path)

        image = preprocess_image(original_path)

        output = model.predict(image)

        output_filename = 'output_' + filename
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
        save_image(output, output_path)

        return jsonify(
            status="success",
            original_image='/uploads/' + filename,
            output_image='/uploads/output_images/' + output_filename
        )

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/uploads/output_images/<filename>')
def output_file(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename)

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    if not os.path.exists(app.config['OUTPUT_FOLDER']):
        os.makedirs(app.config['OUTPUT_FOLDER'])
    app.run(debug=True)
