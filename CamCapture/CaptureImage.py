import os
from datetime import datetime
import cv2 # importing OpenCV library
import ManOfTheMessage

class CaptureImage:
    def __new__(cls, cam_port):
        istanza = super().__new__(cls)
        return istanza
    
    def __init__(self, cam_port):
        print("CaptureImage Rel: 2022.021.1022")
        self.cam = cv2.VideoCapture()
        self.__camsports = []

        #Testing ports
        camsports = cam_port.split(";")
        for camport in camsports:
            print("Cheking port "+camport)
            if self.cam.open(int(camport)):
                self.cam.release()
                self.__camsports.append(["USB",camport])
                print("Port "+camport+" OK")
            else:
                print("Port "+camport+" KO")
        self.__imgext = "png"
        self.__imgsep = ";"

    def cattura(self, eancode, filename):
        if not os.path.isdir(self.__savedir):
            return ManOfTheMessage.buildErrMesg("Folder {"+self.__savedir+"} does not exist")
        if len(self.__camsports) == 0:
            return ManOfTheMessage.buildErrMesg("NO CAMERAS")
        names = ""
        if len(filename) == 0 or filename == eancode:
            now = datetime.now().strftime("%Y%m%d%H%M%S%f")
            filename = self.__imgprefix+"_"+now+"_"+eancode+"_"
        camid = 0
        while camid < len(self.__camsports):
            print("read cam "+str(self.__camsports[camid][0])+" "+str(self.__camsports[camid][1]))
            self.opencam(self.__camsports[camid])
            result, image = self.cam.read()
            if result:
                names = names + self.saveondisk(eancode, image, filename+str(camid)) + self.__imgsep
            else:
                print("Errore")
            self.closecam()
            camid = camid + 1
        if len(names) > 0:
            return names[:-1]
        else:
            return ManOfTheMessage.buildErrMesg("No image generated")

    def opencam(self, camid):
        self.cam.open(int(camid[1]))
        self.cam.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        self.cam.set(cv2.CAP_PROP_FPS, 1)
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    def closecam(self):
        self.cam.release()

    def saveondisk(self, eancode, image, filename):
        filename = filename+"."+self.__imgext
        path = self.__savedir+"/"+filename
        cv2.imwrite(path, image)
        return filename

    def setImageSaveDir(self, directory):
        self.__savedir = directory

    def setImagePrefix(self, prefix):
        self.__imgprefix = prefix

    def setImageExt(self, ext):
        self.__imgext = ext

    def setImageSep(self, sep):
        self.__imgsep = sep
