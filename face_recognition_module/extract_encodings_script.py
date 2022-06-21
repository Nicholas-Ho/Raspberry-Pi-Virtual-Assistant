import face_recognition
import os
import json

path = 'source'

# Load pictures from folder and learn how to recognise them.
encodings = {} # {'Name': encoding}
if os.path.isfile(path):
    print("Loading known face image(s)")

    for file in os.listdir(path):
        # One person per image
        name = file.rpartition('.')[0]
        image = face_recognition.load_image_file(file)
        encoding = face_recognition.face_encodings(image)[0]
        encodings[name] = encoding

    print('Images encoded.')
else:
    raise FileNotFoundError('Source directory does not exist. Check path.')

with open('encodings.json', 'w') as output:
    json.dump(encodings, output)