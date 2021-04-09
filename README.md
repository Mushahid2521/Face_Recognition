# Face Recognition
This repository contains the code for Face Recognition project where the user can input an image to check if the person in the image is present in the Known faces in the known facses folder.    

There are two main files.  
`recognize_person.py` which recognize the face passed as input. Additionally it takes the known face directory and encoding file as input. If only the known face directory is passed then it encodes those and saves into a pickle file. If both known and encoding files is present then it updates the encoding file.  

`save_update_encodings.py` which encode the known faces so that the recognition step is faster. Addionally it takes the known face directory. By default it assumes that a `known` folder is present which contains the known faces if the known face direcotry is not passsed. Thus file can be useful when the system is idle and it has many images to encode for being used in later query.   


This also supports mutiple faces present in the Image and tells from left which one is whom from the known faces. If a person is not present then it prints unknown face. Codes are commented with explanation of each steps. 

## Usage   
`virtualenv` is required to follow the steps. To install virtual environment. `sudo apt-get install python3-pip` and `pip3 install virtualenv` on the terminal. 
The code has been tested on Linux OS and Python3.8. 
```
git clone https://github.com/Mushahid2521/Face_Recognition.git
cd Face_Recognition
source env/bin/activate

python3 recognize_person.py -l known_1.jpg
python3 recognize_person.py -l unknown.jpg
python3 recognize_person.py -l multiple_faces.png
```

## Steps Followed
1. Face Recognition module is used to detect faces and get face encodings which uses dlib's state-of-the-art face recognition built with deep learning.
2. First face encodings are stored in a dictionary and saved using pickle module. 
3. Input image is taken which may contains multiple faces. Each face is matched with the existing encodings file. This allows faster query. Before that the knwon face folder is checked if it updated by adding or removing any person. If the person already in the encoding it skip its encoding operation. If a person is removed from the previous known folder, it also deletes the encoding of that person from the encoding file. 
4. For multiple faces persons are matched from left. If no person is found then it prints that message. 

**Drawback:** If there present different person with same name then it will consider both of them as same person as we are storing the encoding with name as key.  



