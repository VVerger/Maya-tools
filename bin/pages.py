import os
from PySide2.QtCore import*
from PySide2.QtWidgets import*
from PySide2.QtGui import *
import sys
from fileManagment import* 
import data

class ToolboxPages(QWidget, FileManagment):
    def __init__(self):
        super().__init__()
        
        self.single_click_timer = QTimer(self)
        self.single_click_timer.setSingleShot(True)
        self.single_click_timer.timeout.connect(self.on_single_click)
        self._btnPath = None
        self._project = None
        self._name = None

    def setAssetToolbox(self,Toolbox):
        address = data.Main_Path
        characterPath = address + '/04_asset/character'
        propsPath = address + '/04_asset/props'
        decorPath = address + '/04_asset/set'

        CList = os.listdir(characterPath)
        PList = os.listdir(propsPath)
        SList = os.listdir(decorPath)

        
        #character
        CWidget = self.createButtonAsset(CList, characterPath)
        
        Toolbox.addItem(CWidget, 'Characters')

        #props
        PWidget = self.createButtonAsset(PList, propsPath)

        Toolbox.addItem(PWidget, 'Props')

        #set
        for i in SList:
            AssetPath = decorPath + '/' + i
            AssetList = os.listdir(AssetPath)
            SWidget = self.createButtonAsset(AssetList, AssetPath)
            Toolbox.addItem(SWidget, i)

        return Toolbox

    def setShotToolbox(self, Toolbox):

        address = data.Main_Path
        seqPath = address + '/05_Shot'
        seqList = os.listdir(seqPath)
        for i in seqList:
            if i == 'Thumbs.db':
                pass
            else:
                shotPath = seqPath + '/' + i
                shotList = os.listdir(shotPath)
                shotWidget = self.createButtonShot(shotList, shotPath)
                Toolbox.addItem(shotWidget, i)

        return Toolbox

    def createButtonAsset(self, liste, path):
        mainwidget = QWidget()
        mainlayout = QVBoxLayout()
    
        liste = [path for path in liste if 'setDress' not in path]

        #file for frame
        fileLayout = QHBoxLayout()
        fileWidget = QWidget()
        firstButton = QPushButton('')
        iconPathFile = data.Ressource_Path + "/icon/blue_folder.png"
        iconPathBalckFile = data.Ressource_Path + "/icon/blue_folder_shade.png"
        FButtonicon = QIcon (iconPathFile)
        icon = QIcon (iconPathFile)
        firstButton.setIcon(icon)
        firstButton.setIconSize(QPixmap(iconPathFile).size())
        firstButton.setFixedSize(QPixmap(iconPathFile).size())
        firstButton.setStyleSheet("border: none; background: transparent;")
        firstButton.clicked.connect(lambda btnPath = path , x= 'null' : self.openfile(btnPath, x))
        firstButton.enterEvent = lambda event, button = firstButton, path = iconPathBalckFile: button.setIcon(QIcon(iconPathBalckFile))
        firstButton.leaveEvent = lambda event, button = firstButton, path = iconPathFile: button.setIcon(QIcon(iconPathFile))
        fileLayout.addWidget(firstButton)

        fileLayout.insertStretch(-1)
        fileWidget.setLayout(fileLayout)
        mainlayout.addWidget(fileWidget)


        for i in liste :
            label = QLabel(i) 
            layoutBase = QHBoxLayout()
            
            fileButton = QPushButton('')
            fileButton.setIcon(icon)
            fileButton.setIconSize(QPixmap(iconPathFile).size())
            fileButton.setFixedSize(QPixmap(iconPathFile).size())
            fileButton.setStyleSheet("border: none; background: transparent;")
            fileButtonPath = path + '/' + i + '/maya/scenes'
            fileButton.clicked.connect(lambda btnPath = fileButtonPath , x= 'null' : self.openfile(btnPath, x))
            fileButton.enterEvent = lambda event, button = fileButton, path = iconPathBalckFile: button.setIcon(QIcon(iconPathBalckFile))
            fileButton.leaveEvent = lambda event, button = fileButton, path = iconPathFile: button.setIcon(QIcon(iconPathFile))  
            layoutBase.addWidget(label)
            layoutBase.addWidget(fileButton)
            
            button_names = ['modeling', 'rigging', 'lookdev', 'groom', 'cfx']
            for idx, name in enumerate(button_names):
                EditPath = path + '/' + i + '/maya/scenes/edit/' + name
                button = QPushButton(name) 
                button.mousePressEvent = lambda event, btnPath = EditPath , button = button, project = i, name = name: self.handleMousePress(event, btnPath, button, project, name)
                
                color_top = self.generate_gradient_color(idx, 5)    
                color_bottom = self.generate_gradient_color(idx + 1, 5)  
                button.setStyleSheet(
                    f"QPushButton {{"
                    f"border : 1px solid black;"
                    f"background-color: qlineargradient(x1: 0, y1: 1, x2: 0, y2: 0, stop: 0 {color_bottom}, stop: 1 {color_top});"
                    f"min-height: 20px;"
                    f"}}"
                    f"QPushButton:hover {{"
                    f"   background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #430303, stop: 1 #8e6b6b);"
                    f"}}"
                )
                
                layoutBase.addWidget(button)
        
            wigdetBase = QWidget()
            wigdetBase.setLayout(layoutBase)
            mainlayout.addWidget(wigdetBase)
        
        mainlayout.insertStretch(-1)
        mainwidget.setLayout(mainlayout)
        return mainwidget


    def createButtonShot (self, liste, path):
        mainWidget = QWidget()
        mainlayout = QVBoxLayout()

        #file for frame
        fileLayout = QHBoxLayout()
        fileWidget = QWidget()
        seqButton = QPushButton('')
        iconPathFile = data.Ressource_Path + "/icon/blue_folder.png"
        iconPathBalckFile = data.Ressource_Path + "/icon/blue_folder_shade.png"
        FButtonicon = QIcon(iconPathFile)
        icon = QIcon (iconPathFile)
        seqButton.setIcon(icon)
        seqButton.setIconSize(QPixmap(iconPathFile).size())
        seqButton.setFixedSize(QPixmap(iconPathFile).size())
        seqButton.setStyleSheet("border: none; background: transparent;")
        seqButton.clicked.connect(lambda btnPath = path , x= 'null' : self.openfile(btnPath, x))
        seqButton.enterEvent = lambda event, button = seqButton, path = iconPathBalckFile: button.setIcon(QIcon(iconPathBalckFile))
        seqButton.leaveEvent = lambda event, button = seqButton, path = iconPathFile: button.setIcon(QIcon(iconPathFile))
        
        fileLayout.addWidget(seqButton)
        fileLayout.insertStretch(-1)
        fileWidget.setLayout(fileLayout)
        mainlayout.addWidget(fileWidget)

        for i in liste:
            label = QLabel(i)
            layoutBase = QHBoxLayout()
            fileButton = QPushButton('')
            fileButton.setIcon(icon)
            fileButton.setIconSize(QPixmap(iconPathFile).size())
            fileButton.setFixedSize(QPixmap(iconPathFile).size())
            fileButton.setStyleSheet("border: none; background: transparent;")
            fileButtonPath = path + '/' + i + '/maya/scenes'
            fileButton.clicked.connect(lambda btnPath = fileButtonPath , x= 'null' : self.openfile(btnPath, x))
            fileButton.enterEvent = lambda event, button = fileButton, path = iconPathBalckFile: button.setIcon(QIcon(iconPathBalckFile))
            fileButton.leaveEvent = lambda event, button = fileButton, path = iconPathFile: button.setIcon(QIcon(iconPathFile))  
            layoutBase.addWidget(label)
            layoutBase.addWidget(fileButton)

            button_names = ['layout', 'anim', 'light', 'fx', 'rendu']
            for idx, name in enumerate(button_names):
                EditPath = fileButtonPath + '/edit/' + name
                button = QPushButton(name) 
                button.mousePressEvent = lambda event, btnPath = EditPath , button = button, project = i, name = name: self.handleMousePress(event, btnPath, button, project, name)
               
                color_top = self.generate_gradient_color(idx, 5)    
                color_bottom = self.generate_gradient_color(idx + 1, 5)  
                button.setStyleSheet(
                    f"QPushButton {{"
                    f"border : 1px solid black;"
                    f"background-color: qlineargradient(x1: 0, y1: 1, x2: 0, y2: 0, stop: 0 {color_bottom}, stop: 1 {color_top});"
                    f"min-height: 20px;"
                    f"}}"
                    f"QPushButton:hover {{"
                    f"   background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #430303, stop: 1 #8e6b6b);"
                    f"}}"
                )

                layoutBase.addWidget(button)

            wigdetBase = QWidget()
            wigdetBase.setLayout(layoutBase)
            mainlayout.addWidget(wigdetBase)

        mainlayout.insertStretch(-1)
        mainWidget.setLayout(mainlayout)
        return mainWidget

    def openfile(self, path, x):
        os.startfile(path)


        
    def backupfile(self, path):
        FileManagment.openBackup(self, path)
        
            
    def handleMousePress(self, event, btnPath, button, project, name):
        self._btnPath = btnPath
        self._project = project
        self._name = name

        if event.button() == Qt.MiddleButton:
            self.middleButton(btnPath)

        elif event.type() == QEvent.MouseButtonDblClick and event.button() == Qt.LeftButton:  
            self.single_click_timer.stop()
            self.backupfile(btnPath)

        elif event.button() == Qt.LeftButton:
            self.single_click_timer.start(250) 

        else:
            QPushButton.mousePressEvent(button, event)


    def middleButton(self,btnPath):
        FileManagment.importAsset(self, btnPath)

    def on_single_click(self):
        # Méthode appelée pour le clic simple une fois le timer expiré
        FileManagment.mayaScene(self, self._btnPath, self._project, self._name)



    def generate_gradient_color(self, step, total_steps):
        """Génère une couleur en fonction du step, du vert pâle au vert foncé"""
        start_color = (92, 121, 98)  # Vert foncé (#5c7962)
        end_color = (11, 57, 21)    # Vert presque noir (#0b3915)
        
        # Calculer la différence entre les composantes de couleur
        r = start_color[0] + (end_color[0] - start_color[0]) * step // total_steps
        g = start_color[1] + (end_color[1] - start_color[1]) * step // total_steps
        b = start_color[2] + (end_color[2] - start_color[2]) * step // total_steps
    
        # Retourner la couleur en format hexadécimal
        return f"#{r:02x}{g:02x}{b:02x}"