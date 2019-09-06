import os
import face_recognition
import cv2
from datetime import datetime
import csv

known_face_encodings = []
known_face_metadata = []

def registerKnownFaces():
    original = '//home//cm//dlib-19.17//Doorcam_Save_Faces//Face_Recognition:DCU_Insight//InsightCrawler'
    path = '//home//cm//dlib-19.17//Doorcam_Save_Faces//Face_Recognition:DCU_Insight//InsightCrawler//InsightFaces//full'

    with open("InsightInformation.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter = ',')
        line_count = 0
        
        next(csv_reader)
        face_label = []
        os.chdir(path)
        print("Directory Changed")
        counter = 1
        try:
            for row in csv_reader:

                first_name = row[0]
                last_name = row[1]
                position_name = row[2]
                filename = row[3]
                url = row[4]
                #print(first_name, last_name, filename)
                frame = face_recognition.load_image_file(filename)              # Smaller image
                #small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)       # Faster processing
            
                face_locations = face_recognition.face_locations(frame)   # Cropping
                face_encodings = face_recognition.face_encodings(frame, face_locations)
                print(counter)
                counter += 1
                #print(len(face_locations))
                if len(face_locations) == 0:
                    pass
                else:
                    top, right, bottom, left = face_locations[0]    # Assuming only 1 person per image
                    face_image = frame[top:bottom, left:right]
                    face_image = cv2.resize(face_image, (150, 150)) # Resizes image

                    register_new_face(face_encodings, first_name, last_name, position_name, face_image)
                
                line_count += 1
            print(f'Processed {line_count} People.')
            os.chdir(original)
            print("Returning to Original Directory")

        except IndexError:
            pass

    return known_face_encodings, known_face_metadata, face_label

def register_new_face(face_encoding, first_name, last_name, position, face_image):          #
    known_face_encodings.append(face_encoding)                                              #
    known_face_metadata.append({                                                            #
        "last_seen": datetime.now(),                                                        #
        "first_name": first_name,                                                           #
        "last_name": last_name,                                                             #
        "position": position,                                                               #
        "face_image": face_image,                                                           #
        "seen_frames": 1,
    })

	#Testing
if __name__ == "__main__":
	registerKnownFaces()
