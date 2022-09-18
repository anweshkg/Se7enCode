from traceback import print_tb
import face_recognition
import cv2
import os 
import numpy as np
import json  
import sys
if ('.txt' in sys.argv[1]):
    with open(sys.argv[1],'r',encoding='utf-8') as f:
        fid=f.read()
else:
    fid=sys.argv[1]

def logger(string):
    with open("logs.txt",'a',encoding="utf-8") as f:
        f.write(str(string))

def face_distance(face_encodings, face_to_compare):
    if len(face_encodings) == 0:
        return np.empty((0))

    return np.linalg.norm(face_encodings - face_to_compare, axis=1)

def compare_faces(known_face_encodings, face_encoding_to_check, tolerance=0.6):
    return list(face_distance(known_face_encodings, face_encoding_to_check) <= tolerance)

def compute_match(match_value,c):
    if bool(match_value[0]):
        global count
        count+=1
        if(count>=10):
            # result=True
            return True

    else:
        return False


def face_verify_fromDB(face_encodelistDB,vid_path):
    sourcefolder=vid_path
    face_encodingdb=np.asarray(face_encodelistDB, dtype=np.float32)

    known_faces = [face_encodingdb]

    
    video_file = os.path.join('files', vid_path)

    input_movie = cv2.VideoCapture(video_file)
    face_locations = []
    face_encodings = []
    # face_names = []
    frame_number = 0
    result=False
    count=0
    while_iter = 0 
    while True:
        while_iter+=1
        if (while_iter) > 7:
            return False
        print("Pass")
        sys.stdout.flush()
        logger("start\n")
        ret, frame = input_movie.read()
        frame_number += 1
        if not ret:
            print('Passing Break')
            break
        rgb_frame = frame[:, :, ::-1]

        face_locations = face_recognition.face_locations(rgb_frame)

        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)


        for time_run,face_encoding in enumerate(face_encodings):
            if (time_run) > 4:
                print("Pass Breaking Face")
                return False
            print("Pass 2")
            sys.stdout.flush()

            match = face_recognition.compare_faces(known_faces, face_encoding, tolerance=0.39)    
            if bool(match[0]):
                count+=1
                if(count>2):
                    result=True
                    input_movie.release()
                    cv2.destroyAllWindows()
                    sys.stdout.flush()

                    # return result
                    return result
    input_movie.release()
    cv2.destroyAllWindows()
    sys.stdout.flush()

    return result


#format : list,string to path


    
# if len(sys.argv) != 3:
#     sys.exit(0)
# ar = json.loads(fid)
# var = face_verify_fromDB(ar ,'file-1663403653122-899586894.mp4')
# print("False")
# # var = face_verify_fromDB(ar ,sys.argv[2])

