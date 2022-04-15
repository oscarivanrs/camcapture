#REL 2022.020.1010
from CamCapture import CaptureImage
import configparser

def init():
    global cTP
    cTP = "TAKEPHOTO"
    global cREADY
    cREADY = "READY"
    global cIMREADY
    cIMREADY = "YES"
    global cLISTBESTMATCH
    cLISTBESTMATCH = "LISTBESTMATCH"
    global cDIRBESTMACTH
    cDIRBESTMACTH = "DIRBESTMATCH"
    global cCOMPAREIMG
    cCOMPAREIMG = "COMPAREIMG"
    global cADDTEXT
    cADDTEXT = "ADDTEXT"
    global cSETEXT
    cSETEXT = "SETEXT"
    global cERR
    cERR = "KO"
    global cSUCCESS
    cSUCCESS = "OK"
    global cIMG1
    cIMG1 = "IMG1"
    global cIMG2
    cIMG2 = "IMG2"
    global cNOMATCH
    cNOMATCH = "HOPS"
    global lblERR
    lblERR = "ERROR"
    global pFNAME
    pFNAME = "FNAME"
    global pEAN
    pEAN = "EAN"
    global pQTY
    pQTY = "QTY"
    global pPATH
    pPATH = "PATH"
    global pEXT
    pEXT = "EXT"
    global pIMGSEP
    pIMGSEP = "IMGSEP"
    global pSOURCE
    pSOURCE = "SOURCE"
    global pFILESLIST
    pFILESLIST = "FILES"
    global pDIRECTORY
    pDIRECTORY = "DIR"
    global pTEXT
    pTEXT = "TEXT"
    global paramsSEP
    paramsSEP = "|"
    global valASSIGN
    valASSIGN = "="
    global config
    global imgLibrary
    global defPath
    global defImgSep
    config = configparser.ConfigParser()
    config.read('config.ini')
    imgLibrary = config.get("DEFAULT","imagesLibrary")
    defPath = config.get("DEFAULT","imagesavedir")
    defImgSep = config.get("DEFAULT","imageseparator")

def initCamManager():
    if 'camManager' in globals():
        return
    print("initCamManager()")
    global camManager
    camManager = CaptureImage.CaptureImage(config.get("DEFAULT","cam_port"))
    camManager.setImagePrefix(config.get("DEFAULT","imagesprefix"))
