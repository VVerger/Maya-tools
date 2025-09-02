from PySide2.QtCore import*
from PySide2.QtWidgets import*
from PySide2.QtGui import*
import sys
import os
import shutil
from refreshAll import *
from ui import*
import data

class Add():
    def __init__(self):
        super(). __init__()
        
        self.mainpath = data.Main_Path
        self.newAssetWindow = None
        self.newShotWindow = None

    def addAssetWindow(self, refresh_callback):
        if self.newAssetWindow is None:
            self.newAssetWindow = AssetWindow()
            self.newAssetWindow.signal_action.connect(refresh_callback)
        self.newAssetWindow.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.newAssetWindow.show()

    def addShotWindow(self, refresh_callback):
        if self.newShotWindow is None:
            self.newShotWindow = ShotWindow()
            self.newShotWindow.signal_action.connect(refresh_callback)
        self.newShotWindow.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.newShotWindow.show()


    def addTextureWindow(self):
        print(2)


class AssetWindow(QWidget):
    signal_action = Signal()

    def __init__(self):
        super().__init__()
        self.templatePath = data.Ressource_Path + '/Templates/assetTemplates'
        self.assetPath = data.Main_Path + '/04_asset/'
        self.characterPath = self.assetPath + 'character'
        self.propsPath = self.assetPath + 'props'
        self.decorPath = self.assetPath + 'set'

        CList = os.listdir(self.characterPath)
        PList = os.listdir(self.propsPath)
        SList = os.listdir(self.decorPath)


        self.setWindowTitle("Add Asset")
        self.resize(500,300)
        
        

        self.mainlayout = QVBoxLayout()
        
        
        
        ##list01
        self.VLayout01 = QVBoxLayout()
        
        self.frameListeW = QListWidget()
        
        
        self.frameListeW.addItem('character')
        self.frameListeW.addItem('props')
        self.frameListeW.addItems(SList)
        self.frameListeW.setCurrentRow(0)
        self.frameListeW.itemClicked.connect(self.frameclicked)


        self.frameQLine = QLineEdit()
        self.frameQLine.setMaxLength(15)
        self.frameQLine.setPlaceholderText("Enter a new set name")


        self.frameButton =  QPushButton('Add Set')
        self.frameButton.clicked.connect(self.frameButtonClicked)

        self.VLayout01.addWidget(self.frameListeW)
        self.VLayout01.addWidget(self.frameQLine)
        self.VLayout01.addWidget(self.frameButton)

        self.VLayout01Widget = QWidget()
        self.VLayout01Widget.setLayout(self.VLayout01)

        ##list02
        self.VLayout02 = QVBoxLayout()
        
        self.assetListeW = QListWidget()
        charaList = os.listdir(self.characterPath)
        self.assetListeW.addItems(charaList)


        self.assetQLine = QLineEdit()
        self.assetQLine.setMaxLength(15)
        self.assetQLine.setPlaceholderText('Enter a new project name')


        self.assetButton = QPushButton('Add Project')
        self.assetButton.clicked.connect(self.assetButtonClicked)


        self.VLayout02.addWidget(self.assetListeW)
        self.VLayout02.addWidget(self.assetQLine)
        self.VLayout02.addWidget(self.assetButton)

        self.VLayout02Widget = QWidget()
        self.VLayout02Widget.setLayout(self.VLayout02)

        self.HLayout = QHBoxLayout()
        self.HLayout.addWidget(self.VLayout01Widget)
        self.HLayout.addWidget(self.VLayout02Widget)
        self.HLayoutWidget = QWidget()
        self.HLayoutWidget.setLayout(self.HLayout)


        self.mainlayout.addWidget(self.HLayoutWidget)
        self.setLayout(self.mainlayout)


        


    def frameclicked(self):
        current_row = self.frameListeW.currentRow()
        current_item = self.frameListeW.currentItem()

        if current_row == 0:
            newPath = self.characterPath

        elif current_row == 1:
            newPath = self.propsPath

        else:
            name = current_item.text()
            newPath = self.decorPath + '/' +name
            
        
        newlist = os.listdir(newPath)
        self.assetListeW.clear()
        self.assetListeW.addItems(newlist)
  


    def frameButtonClicked (self):
        frameName = self.frameQLine.text()
        newPath =  self.decorPath + '/' + frameName
        if not frameName :
            button = QMessageBox.critical(
            self,
            "Error",
            "Ecrit un nom idiot!",
            buttons=QMessageBox.Ok,
            defaultButton=QMessageBox.Ok,
            )
        else:
            if not os.path.exists(newPath):
                os.makedirs(newPath)
                self.frameListeW.addItem(frameName)
                self.frameQLine.clear()
                self.signal_action.emit()

            else:
                button = QMessageBox.critical(
                self,
                "Error",
                "Le fichier existe deja idiot!",
                buttons=QMessageBox.Ok,
                defaultButton=QMessageBox.Ok,
                )



    def assetButtonClicked (self):
        assetName = self.assetQLine.text()
        current_row = self.frameListeW.currentRow()
        current_item = self.frameListeW.currentItem()
        if not assetName : 
            button = QMessageBox.critical(
            self,
            "Error",
            "Ecrit un nom idiot!",
            buttons=QMessageBox.Ok,
            defaultButton=QMessageBox.Ok,
            )
        else:
            if current_row == 0:
                path = self.characterPath +'/' + assetName
                
                if not os.path.exists(path):
                    shutil.copytree(self.templatePath, path)
                    self.assetListeW.addItem(assetName)
                    self.assetQLine.clear()
                    self.signal_action.emit()
                else:
                    button = QMessageBox.critical(
                    self,
                    "Error",
                    "Le fichier existe deja idiot!",
                    buttons=QMessageBox.Ok,
                    defaultButton=QMessageBox.Ok,
                    )


            elif current_row == 1:
                path = self.propsPath + '/' + assetName
                if not os.path.exists(path):
                    shutil.copytree(self.templatePath, path)
                    self.assetListeW.addItem(assetName)
                    self.assetQLine.clear()
                    self.signal_action.emit()
                else:
                    button = QMessageBox.critical(
                    self,
                    "Error",
                    "Le fichier existe deja idiot!",
                    buttons=QMessageBox.Ok,
                    defaultButton=QMessageBox.Ok,
                    )
            else:
                name = current_item.text()
                path = self.decorPath + '/' + name + '/' + assetName
                if not os.path.exists(path):
                    shutil.copytree(self.templatePath, path)
                    self.assetListeW.addItem(assetName)
                    self.assetQLine.clear()
                    self.signal_action.emit()
                else:
                    button = QMessageBox.critical(
                    self,
                    "Error",
                    "Le fichier existe deja idiot!",
                    buttons=QMessageBox.Ok,
                    defaultButton=QMessageBox.Ok,
                    )



class ShotWindow(QWidget):
    signal_action = Signal()

    def __init__(self):
        super().__init__()
        self.templatePath = data.Ressource_Path + '/Templates/shotTemplates'
        self.shotPath = data.Main_Path + '/05_shot'

        self.seqList = os.listdir(self.shotPath)

        self.setWindowTitle("Add Shot")
        self.resize(500,300)

        self.mainlayout = QHBoxLayout()

        #left
        self.leftLayout = QVBoxLayout()

        self.seqLabel = QLabel('Sequences')

        self.seqListWidget = QListWidget()
        self.seqListWidget.addItems(self.seqList)
        self.seqListWidget.itemClicked.connect(self.seqClicked)

        

        self.seqLineE = QLineEdit()
        self.seqLineE.setMaxLength(15)
        self.seqLineE.setPlaceholderText("Enter a new seq name")

        self.seqButton =QPushButton('Add Sequence')
        self.seqButton.clicked.connect(self.seqButtonClicked)

        self.leftLayout.addWidget(self.seqLabel)
        self.leftLayout.addWidget(self.seqListWidget)        
        self.leftLayout.addWidget(self.seqLineE)
        self.leftLayout.addWidget(self.seqButton)

        self.leftWidget = QWidget()
        self.leftWidget.setLayout(self.leftLayout)

        self.mainlayout.addWidget(self.leftWidget)

        #right
        self.rightLayout = QVBoxLayout()

        self.shotLabel= QLabel('Shot')

        self.shotListWidget = QListWidget()
        if not self.seqListWidget.currentRow() is None:
            currentSeq = self.seqListWidget.item(0).text()
            tempPath = self.shotPath + '/' + currentSeq
            self.shotListWidget.addItems(os.listdir(tempPath))

        self.shotLineE = QLineEdit()
        self.shotLineE.setMaxLength(15)
        self.shotLineE.setPlaceholderText("Enter a new shot name")

        self.shotButton = QPushButton('Add Shot')
        self.shotButton.clicked.connect(self.shotButtonClicked)

        self.rightLayout.addWidget(self.shotLabel)
        self.rightLayout.addWidget(self.shotListWidget)
        self.rightLayout.addWidget(self.shotLineE)
        self.rightLayout.addWidget(self.shotButton)

        self.rightWidget = QWidget()
        self.rightWidget.setLayout(self.rightLayout)
        
        self.mainlayout.addWidget(self.rightWidget)
        self.setLayout(self.mainlayout)

       
        

    def seqClicked(self):
        name = self.seqListWidget.currentItem().text()
        path = self.shotPath + '/' + name
        newListe = os.listdir(path)
        self.shotLineE.setText(name+'_sh')       
        self.shotListWidget.clear()
        self.shotListWidget.addItems(newListe)


    def seqButtonClicked(self):
        seqName = self.seqLineE.text()
        newPath = self.shotPath +'/'+ seqName
        if not seqName:
            button = QMessageBox.critical(
            self,
            "Error",
            "Ecrit un nom idiot!",
            buttons=QMessageBox.Ok,
            defaultButton=QMessageBox.Ok,
            )

        else:
            if not os.path.exists(newPath):
                os.makedirs(newPath)
                self.seqListWidget.addItem(seqName)
                self.seqLineE.clear()
                self.signal_action.emit()

            else:
                button = QMessageBox.critical(
                self,
                "Error",
                "Le fichier existe deja idiot!",
                buttons=QMessageBox.Ok,
                defaultButton=QMessageBox.Ok,
                )


    def shotButtonClicked(self):
        shot = self.shotLineE.text()
        seq = self.seqListWidget.currentItem().text()
        path = self.shotPath +'/'+seq+'/'+shot
        if not os.path.exists(path):
            shutil.copytree(self.templatePath, path)
            self.shotListWidget.addItem(shot)
            
            num = shot.split('_sh')[-1]
            nextNum = int(num)+10
            nextNum = self.shotpadding(nextNum, 4)
            nextShot = shot.replace(num, nextNum)
            self.shotLineE.setText(nextShot)

            self.signal_action.emit()

        else:
            button = QMessageBox.critical(
            self,
            "Error",
            "Le fichier existe deja idiot!",
            buttons=QMessageBox.Ok,
            defaultButton=QMessageBox.Ok,
            )

    def shotpadding(self, num, padding):
        lenNum = len(str(num))
        nbrZero = padding - lenNum
        stringNum = '0'*nbrZero + str(num)
        return stringNum