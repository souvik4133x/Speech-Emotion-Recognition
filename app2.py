from flask import Flask, render_template, request, redirect
import keras
import numpy as np
import librosa
from sklearn.preprocessing import LabelEncoder
import os
from flask_cors import CORS
app = Flask(__name__)
CORS(app) 
class livePredictions:

    def __init__(self, path, file):
        self.path = path
        self.file = file

    def load_model(self):
        self.loaded_model = keras.models.load_model(self.path)
        return self.loaded_model.summary()

    def makepredictions(self):
        lb = LabelEncoder()
        arr = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']
        enc = lb.fit(arr)
        data, sampling_rate = librosa.load(self.file)
        mfccs = np.mean(librosa.feature.mfcc(y=data, sr=sampling_rate, n_mfcc=40).T, axis=0)
        x = np.expand_dims(mfccs, axis=1)
        x = np.expand_dims(x, axis=0)
        predictions = self.loaded_model.predict(x)
        
        # Get the index of the class with the highest probability
        predicted_class_index = np.argmax(predictions, axis=1)
        
        # Get the corresponding class label
        predicted_class = enc.inverse_transform(predicted_class_index)
        
        print("Prediction is", predicted_class[0])
        return predicted_class[0]
        

# Initialize the livePredictions class with the path to your model
model_path = 'C:/Users/souvi/OneDrive/Desktop/Speech Emotion Python flask/Emotion_Voice_Detection_Model.h5'

@app.route("/", methods=["GET","POST"])
def index():
    transcript = ""  # Initialize transcript with an empty string
    
    if request.method == "POST":
        print("FORM DATA RECEIVED")

        if "file" not in request.files:
            return redirect(request.url)

        file = request.files["file"]
        if file.filename == "":
            return redirect(request.url)
        
        try:
            # Save the uploaded file to a temporary location
            file_path = os.path.join("uploads", file.filename)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            file.save(file_path)

            # Initialize the predictor instance with the file path
            pred = livePredictions(model_path, file=file_path)

            # Load the model and make predictions
            pred.load_model()
            transcript = pred.makepredictions()
            print("Transcript:", transcript)  # Debug print

            # Optionally, delete the file after processing to save space
            os.remove(file_path)

        except Exception as e:
            print(f"Error processing file: {e}")
            transcript = f"Error in processing the uploaded file: {e}"

    return render_template('index.html', transcript=transcript)

if __name__ == "__main__":
    app.run(debug=True, threaded=True)
