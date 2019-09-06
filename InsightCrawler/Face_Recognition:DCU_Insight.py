from registerKnownFaces_CSV2 import registerKnownFaces
from imutils.video import WebcamVideoStream
from datetime import datetime, timedelta
from imutils.video import FPS
import face_recognition
import numpy as np
import platform
import argparse
import imutils
import pickle
import cv2
import os

known_face_encodings = []
known_face_metadata = []

# Functions
#############################################################################################
def save_known_faces():                                                                     #
    with open("InsightKnownFaces.dat", "wb") as face_data_file:                             #
        face_data = [known_face_encodings, known_face_metadata]                             #
        pickle.dump(face_data, face_data_file)                                              #
        print("Known faces backed up to disk.")                                             #
                                                                                            #
def load_known_faces(known_face_encodings, known_face_metadata):                            #
    try:                                                                                    #
        with open("InsightKnownFaces.dat", "rb") as face_data_file:                         #
            known_face_encodings, known_face_metadata = pickle.load(face_data_file)         #
            print("Known faces loaded from disk.")                                          #
    except FileNotFoundError as e:                                                          #
        print("No previous face data found - starting with a blank known face list.")       #
        pass                                                                                #
    return known_face_encodings, known_face_metadata                                        #
                                                                                            #
def register_new_face(face_encoding, first_name, last_name, position, face_image):          #
    known_face_encodings.append(face_encoding)                                              #
    known_face_metadata.append({                                                            #
        "last_seen": datetime.now(),                                                        #
        "first_name": first_name,                                                           #
        "last_name": last_name,                                                             #
        "position": position,                                                               #
        "face_image": face_image,                                                           #
        "seen_frames": 1,                                                                   #
    })                                                                                      #
                                                                                            #
def lookup_known_face(face_encoding):                                                       #
    metadata = None                                                                         #
                                                                                            #
    if len(known_face_encodings) == 0:                          # No known faces            #
        return metadata                                                                     #
                                                                                            #
    i = 0                                                                                   #
    for known_face_encoding in known_face_encodings:                                        #
        face_distances = face_recognition.face_distance(known_face_encoding, face_encoding) #
        best_match_index = np.argmin(face_distances)                                        #
        if face_distances[best_match_index] < 0.58:                                         #
            metadata = known_face_metadata[i]                                               #   
            metadata["last_seen"] = datetime.now()                                          #
            metadata["seen_frames"] += 1                                                    #
                                                                                            #
        i+=1                                                    # Cycles through info       #
    return metadata                                                                         #
                                                                                            #
#############################################################################################

def main_loop():                                        # Main Loop
    process_frame = True
    window_name = "Facial Recognition"
    number_of_faces_since_save = 0
    screenshotCount = 0

    vs = WebcamVideoStream(src=0).start()
    fps = FPS().start()

    print ('After loading: ', len(known_face_encodings), "Faces Found") 

    while True:
        frame = vs.read()
        frame = imutils.resize(frame, width=1280)

        ori_frame = frame.copy()
        small_frame = cv2.resize(frame, (0, 0), fx=0.125, fy=0.125)   

        rgb_small_frame = small_frame[:, :, ::-1]
        if process_frame:
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_labels = []
            position_labels = []
            for face_location, face_encoding in zip(face_locations, face_encodings):
            
                metadata = lookup_known_face(face_encoding) # See if this face is in our list of 
                position_label = []                         # known faces.

                if metadata is not None:
                    face_label = metadata["first_name"]                
                    position_label = metadata["position"]
                    image = metadata["face_image"]
                else:
                    face_label = "New visitor"
                    position_label = "Unknown Position"

                    top, right, bottom, left = face_location
                    face_image = small_frame[top:bottom, left:right]
                    face_image = cv2.resize(face_image, (150, 150))

                    register_new_face(face_encodings, face_label, "Unknown", position_label, face_image)

                face_labels.append(face_label)
                position_labels.append(position_label)
        process_frame = not process_frame


        for (top, right, bottom, left), face_label, position_label in zip(face_locations, face_labels, position_labels):
            
            top *= 8                                    # Scale back up face locations since the 
            right *= 8                                  # frame we detected in was scaled to 1/8 
            bottom *= 8                                 # size.
            left *= 8

            cv2.rectangle(frame, (left - 10, top - 10), (right + 10, bottom + 10), (0, 0, 255), 2)
            cv2.rectangle(frame, (left - 10, bottom - 25), (right + 10, bottom + 10), (0, 0, 255), cv2.FILLED)
            cv2.putText(frame, face_label, (left - 2, bottom - 8), cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 1)
            cv2.putText(frame, position_label, (left, bottom + 5), cv2.FONT_HERSHEY_DUPLEX, 0.4, (255, 255, 255), 1)
            cv2.putText(frame, "Screenshot - s: Quit - q", (10, 10), cv2.FONT_HERSHEY_DUPLEX, 0.4, (0, 0, 0), 1)

# Key Handling
###################################################################################################                                                     
        cv2.imshow(window_name, frame)
        key = cv2.waitKey(1)
              
        if key & 0xFF == ord('q'):                  
            save_known_faces()
            fps.stop()
            vs.stop()
            break      
        elif key & 0xFF == ord('s'):	# Press s to take picture
            numPeople = 0
            locationList = []       	# Create a dictionary of lists
            peopleList = []         	# Lists contain information on people's names and 
            infoDict = {}           	# Their location on the frame
            cv2.rectangle(ori_frame, (0, 800), (1280, 1280), (0 ,0 ,0 ),cv2.FILLED)
            for (top, right, bottom, left), face_label in zip(face_locations, face_labels):
                

                cv2.putText(ori_frame, "From the Left: ", (0, 825), cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 1)

                peopleList.append(face_label)   # Fill the list with names
                locationList.append(face_locations[numPeople][3])   # Fill the list with 
                numPeople += 1      	# Iterate through the faces found in the frame                                                        # leftmost location
                infoDict["label"] = peopleList  # Insert the people list into the key "label"
                infoDict["location"] = locationList # Insert location list into the key "location"

            locationArray = np.array(locationList)  # Use bubble sort to move smallest (leftmost)
            lengthOfArray = len(locationArray) - 1  # location to the front to iterate through 
            for i in range(lengthOfArray):      # those first.
                for j in range(lengthOfArray - i):
                    if locationArray[j] > locationArray[j + 1]:
                        locationArray[j], locationArray[j + 1] = locationArray[j + 1], locationArray[j]

            peopleInFrameCounter = 0
            try:                                # Check if someone's in the frame.
                for x in np.nditer(locationArray):  # Iterate through all items in array
                    for item in range(len(infoDict["location"])):   # Iterate through locations
                        if infoDict["location"][item] == x:     # Check if location matches array,
                            x_label=(peopleInFrameCounter)*100  # which is ascending order.       
                            cv2.putText(ori_frame, infoDict["label"][item], (x_label + 175, 825), cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 1)
                            cv2.imwrite("Screenshot(" + str(screenshotCount + 1) + ")_" + ":" + ".jpg", ori_frame)
                            peopleInFrameCounter += 1   
            except ValueError:                  # If no one's in the frame, ignore it.
                pass

            screenshotCount += 1

# Cleanup
###################################################################################################
        if len(face_locations) > 0 and number_of_faces_since_save > 100:
            save_known_faces()                          
            number_of_faces_since_save = 0      # Saves known faces every so often
        else:
            number_of_faces_since_save += 1

        f = open("InsightKnownFaces.txt", "w")  # Saves known faces to a text file
        f.write(str(known_face_metadata))       
        f.close()                               
        
        fps.update()

    save_known_faces()
    fps.stop()
    print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
    print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
    cv2.destroyAllWindows()
    vs.stop()

if __name__ == "__main__":
    known_face_encodings, known_face_metadata, face_labels = registerKnownFaces()
    load_known_faces(known_face_encodings, known_face_metadata)
    main_loop()


