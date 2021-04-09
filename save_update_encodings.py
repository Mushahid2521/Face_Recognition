import face_recognition
import os
import pickle
import argparse

def save_update_encoding(known_path, encoding_file, verbose=True):
    # If there is already an encoding we update it, else we initialize it and save it
    if os.path.exists(encoding_file):
        encoding_dict = pickle.loads(open(encoding_file, "rb").read())
    else:
        encoding_dict = {}

    # get all the files in the known folder
    files = os.listdir(known_path)

    # Save the current person list to remove the previously known persons, which are not present now
    current_persons_list = set()
    print("......Encoding the Persons.......\n") if verbose else None
    for file in files:
        file_path = os.path.join(known_path, file)
        # check if its a image or not
        if not file_path.lower().endswith((".png", ".jpg", ".jpeg")):
            print(f"{file} is not an Image, Skipping it") if verbose else None
            continue

        # Check if the image can be read
        try:
            image = face_recognition.load_image_file(file_path)
        except:
            print(f"{file} is not a valid Image, Skipping it") if verbose else None
            continue

        person_name = file.split(".")[0] # taking name as without the extension
        print(f"Encoding {person_name}") if verbose else None
        # Check if the person has already in the database
        if person_name in encoding_dict.keys():
            print("{} is already in the Database".format(person_name)) if verbose else None
            current_persons_list.add(person_name)
            continue

        # Get the face locations
        face_locations = face_recognition.face_locations(image)

        # If no face found
        if len(face_locations)<1:
            print(f"{file} doesn't contain a face.") if verbose else None
            continue

        # Check if multiple faces are found, if found we will skip it because we don't know who is whom
        if len(face_locations)>1:
            print(f"{file} contains multiple faces. Not Encoding it.") if verbose else None
            continue

        current_persons_list.add(person_name)
        # Get the encoding
        encoding = face_recognition.face_encodings(image, face_locations)[0]
        encoding_dict[person_name] = encoding

    # Get the persons not in current known persons directory
    removed_persons = [person for person in encoding_dict.keys() if person not in current_persons_list]
    for person in removed_persons:
        print(f"{person} is removed from the encoding") if verbose else None
        del encoding_dict[person]

    with open(encoding_file, "wb") as file:
        file.write(pickle.dumps(encoding_dict))

    print(f"\nSaved Successfully in {encoding_file}") if verbose else None
    print(".....................\n") if verbose else None



if __name__=="__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--directory", default="known",
                    help="path to the known folder directory")
    ap.add_argument("-e", "--encoding", default=os.path.join(os.getcwd(), "encodings.pickle"),
                    help="path to encoding file, default is encodings.pickle")


    args = vars(ap.parse_args())
    save_update_encoding(args["directory"], args["encoding"])
