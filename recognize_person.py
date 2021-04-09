import face_recognition
import os
import pickle
import argparse
from save_update_encodings import save_update_encoding

def recognize_this(location, known_encodings):
    # Lets support unknown directory also
    if os.path.isdir(location):
        files = os.listdir(location)
        image_files = []
        for file in files:
            if file.lower().endswith((".png", ".jpg", ".jpeg")):
                image_files.append(os.path.join(location, file))
    else:
        if location.lower().endswith((".png", ".jpg", ".jpeg")):
            image_files = [location]
        else:
            return

    for file in image_files:
        print(f"Recognizing face/s in {file}")
        try:
            image = face_recognition.load_image_file(file)
        except:
            print(f"{file} is not a valid image")
            continue

        face_locations = face_recognition.face_locations(image)
        # If no face found in the image
        if len(face_locations)<1:
            print(f"No face found in {file}")
            continue

        # Sort to recognize the faces from the Left
        face_locations.sort(key= lambda x:x[3])
        encodings = face_recognition.face_encodings(image, face_locations)

        # If multiple faces found on the Image
        if len(encodings)>1:
            print(f"Multiple faces found in {file}. From Left....")

        for encoding in encodings:
            found = False
            for name, known_encoding in known_encodings.items():
                result = face_recognition.compare_faces([known_encoding], encoding)[0]
                if result:
                    print(f"Found {name}")
                    found = True
                    break

            if not found:
                print("Unknown Face")

        print()


if __name__=="__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-l", "--location", required=True,
                    help="path to the unknown folder or image")
    ap.add_argument("-e", "--encoding", required=False,
                    default=None,
                    help="path to encoding file, default is encodings.pickle")
    ap.add_argument("-kd", "--known_dir", required=False, default="known",
                    help="Directory to match the query image")
    args = vars(ap.parse_args())

    if args["encoding"]==None:
        # User didn't pass an encoding file, We create it from the known dir
        print("Updating the Encoding from Known Folder")
        save_update_encoding(args["known_dir"], "encodings.pickle", False)
        print("Saved/Updated the Encoding\n")
        encodings_ = pickle.loads(open(os.path.join(os.getcwd(), "encodings.pickle"), "rb").read())
    else:
        # User passed an encoding file. We use this
        encodings_ = pickle.loads(open(args["encoding"], "rb").read())

    recognize_this(args["location"], encodings_)

