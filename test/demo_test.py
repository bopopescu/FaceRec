import unittest
import tempfile
import os
import shutil

import cv2
import tensorflow as tf
import numpy as np

from src.main.FaceRec.FaceRec import FaceRec

from src.main.FaceRec.align_custom import AlignCustom
from src.main.FaceRec.face_feature import FaceFeature
from src.main.FaceRec.mtcnn_detect import MTCNNDetect
from src.main.FaceRec.tf_graph import FaceRecGraph

class TestingClass(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.facerec = FaceRec();

    #test for FaceRec module integration
    def testModuleIntegration(self):
        FRGraph = FaceRecGraph();
        MTCNNGraph = FaceRecGraph();
        self.aligner = AlignCustom();
        self.extract_feature = FaceFeature(FRGraph)
        self.face_detect = MTCNNDetect(MTCNNGraph, scale_factor=2);  # scale_factor, rescales image for faster detection

        self.facerec.aligner=self.aligner;
        self.facerec.extract_feature=self.extract_feature;
        self.facerec.face_detect=self.face_detect;


    def testRecognizeSelf(self):
        #open test data image
        img = cv2.imread('C:\\Users\\birsa\\FaceRec\\FaceRec\\test\\Capture.JPG',cv2.IMREAD_COLOR);

        # recog_data[0][0] - name of the recognized person
        # recog_data[0][1] - precision
        recog_data = self.facerec.camera_recog(img)

        recognizedPerson = recog_data[0][0]
        precision = float(recog_data[0][1])

        assert recognizedPerson == 'Birsan Vlad'
        assert precision >= 80.0

    def __init__(self, *args, **kwargs):
        super(TestingClass, self).__init__(*args, **kwargs)
