# Face Recognition
This repository contains the code for Face Recognition project where the user can input an image to check if the person in the image is present in the Known faces in the known facses folder.    

## Usage   
There are two main files.  
```recognize_person.py``` which recognize the face passed as input. Additionally it takes the known face directory and encoding file as input.  
```save_update_encodings.py``` which encode the known faces so that the recognition step is faster. it takes the known face directory. By default it assumes that a `known` folder is present which contains the known faces.   

