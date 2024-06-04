import os
import cv2
import numpy as np
import pickle
from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
from flask_cors import CORS


# Load the trained model, scaler and label encoder
with open('classifier-SVM.pkl', 'rb') as f:
    classifier = pickle.load(f)

with open('scaler2.pkl', 'rb') as f:
    scaler = pickle.load(f)
 
with open('label_encoder2.pkl', 'rb') as f:
    label_encoder = pickle.load(f)

# Define constants
img_height = 64
img_width = 64
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Create Flask app
app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Check if file is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Preprocess image
def preprocess_image(image_path, img_height, img_width):
    img = cv2.imread(image_path)
    img = cv2.resize(img, (img_height, img_width))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    img = img.reshape(1, -1)  # Flatten image
    return img

@app.route('/image', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        # If user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Preprocess the image
            preprocessed_image = preprocess_image(filepath, img_height, img_width)
            preprocessed_image = scaler.transform(preprocessed_image)
            
            # Predict the class of the image
            predicted_class_index = classifier.predict(preprocessed_image)[0]
            predicted_class = label_encoder.inverse_transform([predicted_class_index])[0]
            
            response_data = {
                            "filename": filename,
                            "is_malware": predicted_class
                        }
                        
            return jsonify(response_data)
    return render_template('index.html')
@app.route('/result')
def result():
    return render_template('result.html')

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
