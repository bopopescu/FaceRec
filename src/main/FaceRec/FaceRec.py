'''
FaceRec program
'''

from src.main.FaceRec.align_custom import AlignCustom
from src.main.FaceRec.face_feature import FaceFeature
from src.main.FaceRec.mtcnn_detect import MTCNNDetect
from src.main.FaceRec.tf_graph import FaceRecGraph
import sys
import json
import numpy as np

TIMEOUT = 10 #10 seconds

class FaceRec(object):
    def __init__(self):
        FRGraph = FaceRecGraph();
        MTCNNGraph = FaceRecGraph();
        self.aligner = AlignCustom();
        self.extract_feature = FaceFeature(FRGraph)
        self.face_detect = MTCNNDetect(MTCNNGraph, scale_factor=2);  # scale_factor, rescales image for faster detection


    #     if(mode == "camera"):
    #         camera_recog()
    #     elif mode == "input":
    #         create_manual_data();

    '''
    Description:
    Images from Video Capture -> detect faces' regions -> crop those faces and align them 
        -> each cropped face is categorized in 3 types: Center, Left, Right 
        -> Extract 128D vectors( face features)
        -> Search for matching subjects in the dataset based on the types of face positions. 
        -> The preexisitng face 128D vector with the shortest distance to the 128D vector of the face on screen is most likely a match
        (Distance threshold is 0.6, percentage threshold is 70%)
        
    '''
    def camera_recog(self,frame):
        print("[INFO] camera sensor warming up...")

        rects, landmarks = self.face_detect.detect_face(frame,80);#min face size is set to 80x80
        aligns = []
        positions = []

        for (i, rect) in enumerate(rects):
            aligned_face, face_pos = self.aligner.align(160,frame,landmarks[:,i])
            if len(aligned_face) == 160 and len(aligned_face[0]) == 160:
                aligns.append(aligned_face)
                positions.append(face_pos)
            else:
                print("Align face failed") #log
        recog_data = [];
        if(len(aligns) > 0):
            features_arr = self.extract_feature.get_features(aligns)
            #recog_data - person's name,precision
            recog_data = self.findPeople(features_arr,positions)

        return recog_data

    '''
    facerec_128D.txt Data Structure:
    {
    "Person ID": {
        "Center": [[128D vector]],
        "Left": [[128D vector]],
        "Right": [[128D Vector]]
        }
    }
    This function basically does a simple linear search for 
    ^the 128D vector with the min distance to the 128D vector of the face on screen
    '''
    def findPeople(self,features_arr, positions, thres = 0.6, percent_thres = 70):
        '''
        :param features_arr: a list of 128d Features of all faces on screen
        :param positions: a list of face position types of all faces on screen
        :param thres: distance threshold
        :return: person name and percentage
        '''
        f = open('C:\\Users\\birsa\\FaceRec\\FaceRec\\src\\main\\FaceRec\\facerec_128D.txt','r')
        data_set = json.loads(f.read());
        returnRes = [];
        for (i,features_128D) in enumerate(features_arr):
            result = "Unknown";
            smallest = sys.maxsize
            for person in data_set.keys():
                person_data = data_set[person][positions[i]];
                for data in person_data:
                    distance = np.sqrt(np.sum(np.square(data-features_128D)))
                    if(distance < smallest):
                        smallest = distance;
                        result = person;
            percentage =  min(100, 100 * thres / smallest)
            if percentage <= percent_thres :
                result = "Unknown"
            returnRes.append((result,percentage))
        return returnRes

    '''
    Description:
    User input his/her name or ID -> Images from Video Capture -> detect the face -> crop the face and align it 
        -> face is then categorized in 3 types: Center, Left, Right 
        -> Extract 128D vectors( face features)
        -> Append each newly extracted face 128D vector to its corresponding position type (Center, Left, Right)
        -> Press Q to stop capturing
        -> Find the center ( the mean) of those 128D vectors in each category. ( np.mean(...) )
        -> Save
        
    '''
    def create_manual_data(self,frameList,userID):
        new_name = userID;
        f = open('C:\\Users\\birsa\\FaceRec\\FaceRec\\src\\main\\FaceRec\\facerec_128D.txt','r');
        r = f.read();
        f.close();
        data_set = json.loads(r);
        person_imgs = {"Left" : [], "Right": [], "Center": []};
        person_features = {"Left" : [], "Right": [], "Center": []};
        for frame in frameList:
            rects, landmarks = self.face_detect.detect_face(frame, 80);  # min face size is set to 80x80
            for (i, rect) in enumerate(rects):
                aligned_frame, pos = self.aligner.align(160,frame,landmarks[:,i]);
                if len(aligned_frame) == 160 and len(aligned_frame[0]) == 160:
                    person_imgs[pos].append(aligned_frame)

        for pos in person_imgs: #there r some exceptions here, but I'll just leave it as this to keep it simple
            if(len(person_imgs[pos])!=0):
                person_features[pos] = [np.mean(self.extract_feature.get_features(person_imgs[pos]),axis=0).tolist()]
        data_set[new_name] = person_features;
        f = open('C:\\Users\\birsa\\FaceRec\\FaceRec\\src\\main\\FaceRec\\facerec_128D.txt', 'w');
        f.write(json.dumps(data_set));
        f.close();
