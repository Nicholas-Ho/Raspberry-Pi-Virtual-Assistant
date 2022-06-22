import face_recognition
import picamera
import numpy as np

# Load encodings. allow_pickle=True is a security flaw, but is not relevant.
source = 'source/encodings.npy'
base_encodings = np.load(source, allow_pickle=True).item()

print(base_encodings)

# Get a reference to the Raspberry Pi camera.
# If this fails, make sure you have a camera connected to the RPi and that you
# enabled your camera in raspi-config and rebooted first.
camera = picamera.PiCamera()
camera.resolution = (320, 240)
output = np.empty((240, 320, 3), dtype=np.uint8)

# Initialize some variables
face_locations = []
face_encodings = []

while True:
    print("Capturing image.")
    # Grab a single frame of video from the RPi camera as a numpy array
    camera.capture(output, format="rgb")

    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(output)
    print("Found {} faces in image.".format(len(face_locations)))
    face_encodings = face_recognition.face_encodings(output, face_locations)

    # Loop over each face found in the frame to see if it's someone we know.
    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        match = face_recognition.compare_faces(base_encodings.values(), face_encoding)
        name = "<Unknown Person>"

        if any(match):
            name = base_encodings.keys()[np.where(match)[0]]

        print("I see someone named {}!".format(name))