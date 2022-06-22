import face_recognition
import os
import numpy as np

path = 'source'

# Load pictures from folder and learn how to recognise them.
encodings = {} # {'Name': encoding}
if os.path.isdir(path):
    print("Loading known face image(s)")

    for file in os.listdir(path):
        # One person per image
        name = file.rpartition('.')[0]
        image = face_recognition.load_image_file(os.path.join(path, file))
        encoding = face_recognition.face_encodings(image)[0]
        encodings[name] = encoding

    print('Images encoded.')
else:
    raise FileNotFoundError('Source directory does not exist. Check path.')

# While the pickle module used in this function poses security flaws, this doesn't really matter.
# The main thing is that no precision is lost, while the conversion to list for JSON might.
np.save(os.path.join(path, 'encodings.npy'), encodings)