#REL 2022.020.1010
from ImgDiff import mom
import glv
import threading
import configparser

def buildErrMesg(err):
    print(err)
    return glv.cERR+glv.paramsSEP+glv.lblERR+glv.valASSIGN+err

def getDetails(inputmsg,cmd):
    return inputmsg[len(cmd)+1:].split(glv.paramsSEP)

def checkCommandMatch(inputmsg,command):
    if len(inputmsg) >= len(command) and inputmsg[0:len(command)] == command:
        return True
    return False

def elaboraInput(inputmsg):
    if checkCommandMatch(inputmsg,glv.cREADY):
        return glv.cIMREADY
    elif checkCommandMatch(inputmsg,glv.cTP):
        details = getDetails(inputmsg,glv.cTP)
        filename = ""
        eancode = ""
        quantity = "1"
        path = glv.defPath[:]
        imgsep = glv.defImgSep[:]
        ext = ""
        for detail in details:
            if glv.valASSIGN in detail:
                dett = detail.split(glv.valASSIGN)
                if dett[0] == glv.pFNAME:
                    filename = dett[1]
                elif dett[0] == glv.pEAN:
                    eancode = dett[1]
                elif dett[0] == glv.pQTY:
                    quantity = dett[1]
                elif dett[0] == glv.pEXT:
                     ext = dett[1]
                elif dett[0] == glv.pPATH:
                     path = dett[1]
                elif dett[0] == glv.pIMGSEP:
                     imgsep = dett[1]
                else:
                    print("Detail \""+detail+"\" unrecognized")
            else:
                print("Ivalid details \""+detail+"\"")
        if len(filename) == 0:
            filename = eancode
        if len(filename) > 0:
            glv.initCamManager()
            glv.camManager.setImageSaveDir(path)
            if len(ext) > 0:
                glv.camManager.setImageExt(ext)
            if len(imgsep) > 0:
                glv.camManager.setImageSep(imgsep)
            image_path = glv.camManager.cattura(eancode, filename)
            print("Immagine salvata:", path+"/"+image_path)
            return image_path
        else:
            return buildErrMesg("Missing info to rename the file")
    elif checkCommandMatch(inputmsg,glv.cDIRBESTMACTH):
        details = getDetails(inputmsg,glv.cDIRBESTMACTH)
        sourceimg = ""
        searchdir = ""
        for detail in details:
            if glv.valASSIGN in detail:
                dett = detail.split(glv.valASSIGN)
                if dett[0] == glv.pSOURCE:
                    sourceimg = dett[1]
                elif dett[0] == glv.pDIRECTORY:
                    searchdir = dett[1]
                else:
                    print("Detail \""+detail+"\" unrecognized")
            else:
                return buildErrMesg("Ivalid details \""+detail+"\"")
        if len(sourceimg) > 0:
            if len(searchdir) > 0:
                try:
                    return str(mom.dir_best_match(sourceimg,searchdir))
                except ValueError as err:
                    return buildErrMesg(str(err))
            else:
                return buildErrMesg("Empty param "+glv.pDIRECTORY+"=\""+searchdir+"\"")
        else:
            return buildErrMesg("Empty param "+glv.pSOURCE+"=\""+sourceimg+"\"")
    elif checkCommandMatch(inputmsg,glv.cLISTBESTMATCH):
        details = getDetails(inputmsg,glv.cLISTBESTMATCH)
        sourceimg = ""
        fileslist = ""
        for detail in details:
            if glv.valASSIGN in detail:
                dett = detail.split(glv.valASSIGN)
                if dett[0] == glv.pSOURCE:
                    sourceimg = dett[1]
                elif dett[0] == glv.pFILESLIST:
                    fileslist = dett[1]
                else:
                    print("Detail \""+detail+"\" unrecognized")
            else:
                return buildErrMesg("Ivalid details \""+detail+"\"")
        if len(sourceimg) > 0:
            if len(fileslist) > 0:
                try:
                    return str(mom.list_best_match(sourceimg,fileslist))
                except ValueError as err:
                    return buildErrMesg(str(err))
            else:
                return buildErrMesg("Empty param "+glv.pFILESLIST+"=\""+fileslist+"\"")
        else:
            return buildErrMesg("Empty param "+glv.pSOURCE+"=\""+sourceimg+"\"")
    elif checkCommandMatch(inputmsg,glv.cCOMPAREIMG):
        details = getDetails(inputmsg,glv.cCOMPAREIMG)
        img1 = ""
        img2 = ""
        for detail in details:
            if glv.valASSIGN in detail:
                dett = detail.split(glv.valASSIGN)
                if dett[0] == glv.cIMG1:
                    img1 = dett[1]
                elif dett[0] == glv.cIMG2:
                    img2 = dett[1]
                else:
                    print("Detail \""+detail+"\" unrecognized")
            else:
                return buildErrMesg("Ivalid details \""+detail+"\"")
        if len(img1) > 0:
            if len(img2) > 0:
                try:
                    return str(mom.orb_compare(img1,img2))
                except ValueError as err:
                    return buildErrMesg(str(err))
            else:
                return buildErrMesg("Empty param "+glv.cIMG1+"=\""+img1+"\"")
        else:
            return buildErrMesg("Empty param "+glv.cIMG2+"=\""+img2+"\"")
    elif checkCommandMatch(inputmsg,glv.cADDTEXT):
        details = getDetails(inputmsg,glv.cADDTEXT)
        sourceimg = ""
        imgtext = ""
        for detail in details:
            if glv.valASSIGN in detail:
                dett = detail.split(glv.valASSIGN)
                if dett[0] == glv.pSOURCE:
                    sourceimg = dett[1]
                elif dett[0] == glv.pTEXT:
                    imgtext = dett[1]
                else:
                    print("Detail \""+detail+"\" unrecognized")
            else:
                return buildErrMesg("Ivalid details \""+detail+"\"")
        if len(sourceimg) > 0:
            if len(imgtext) > 0:
                try:
                    mom.write_text_image(sourceimg,imgtext)
                    return glv.cSUCCESS
                except ValueError as err:
                    return buildErrMesg(str(err))
            else:
                return buildErrMesg("Empty param "+glv.pTEXT+"=\""+imgtext+"\"")
        else:
            return buildErrMesg("Empty param "+glv.pSOURCE+"=\""+sourceimg+"\"")
    elif checkCommandMatch(inputmsg,glv.cSETEXT):
        details = getDetails(inputmsg,glv.cSETEXT)
        ext = ""
        for detail in details:
            if glv.valASSIGN in detail:
                dett = detail.split(glv.valASSIGN)
                if dett[0] == glv.pEXT:
                    ext = dett[1]
                else:
                    print("Detail \""+detail+"\" unrecognized")
            else:
                return buildErrMesg("Ivalid details \""+detail+"\"")
        if len(ext) > 0:
            try:
                mom.set_extensions(ext)
                return glv.cSUCCESS
            except ValueError as err:
                return buildErrMesg(str(err))
        else:
            return buildErrMesg("Empty param "+glv.pEXT)
    else:
        return buildErrMesg("Unrecognized message")
