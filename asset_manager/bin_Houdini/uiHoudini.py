from PySide2.QtCore import*
from PySide2.QtWidgets import*
from PySide2.QtGui import*
import sys
from pagesHoudini import*
from fileManagmentHoudini import*
from addHoudini  import*
from refreshAllHoudini import*
import data
import os 
import shutil

class AssetMainWindow(QMainWindow, Add, ToolboxPages, FileManagment):
    instance = None

    def __init__(self):
        if AssetMainWindow.instance is not None:
            # Si une instance existe déjà, la fermer avant de créer une nouvelle
            AssetMainWindow.instance.close()

        print("Initialisation de Main...")  # Message de débogage
        super().__init__()
        print("Main initialisé avec succès.")
        
        self.add = Add()
        self.toolboxPages = ToolboxPages()
        self.fileManagment = FileManagment()
        self.ressourcePath = data.Ressource_Path

        self.setWindowTitle("Asset Manager des singes")
        self.resize(1000,700)
        


        ##toolbarmain
        toolbarMain = QToolBar('Main Toolbar')
        toolbarMain.setIconSize(QSize(32, 32))
        toolbarMain.setMovable(False)

   
            #indentation button
        indentButton_action = QAction(QIcon(self.ressourcePath + "/icon/arrow-090.png"), "Indentation", self)
        indentButton_action.setStatusTip("Indent motherfucker")
        indentButton_action.triggered.connect(self.indentationBackup)
        toolbarMain.addAction(indentButton_action)
        
        toolbarMain.addSeparator()
        
            #publish button
        publishButton_action = QAction(QIcon(self.ressourcePath + "/icon/tick.png"), "Publish",self)
        publishButton_action.setStatusTip("Publish if you are sure")
        publishButton_action.triggered.connect(self.savePublish)
        toolbarMain.addAction(publishButton_action)

        toolbarMain.addSeparator()

            #publishfile button
        publishFile_action = QAction(QIcon(self.ressourcePath + "/icon/folder-horizontal_P.png"), "P_output", self)
        publishFile_action.setStatusTip("Open publish output file")
        publishFile_action.triggered.connect(self.p_outputFile)
        toolbarMain.addAction(publishFile_action)

        toolbarMain.addSeparator()

            #publish transfert file
        publishTrans_action = QAction(QIcon(self.ressourcePath + "/icon/folder-transfert.png"), "Transfert", self)
        publishTrans_action.setStatusTip("transfert publish_output into publish_input")
        publishTrans_action.triggered.connect(self.transfertPublish)
        toolbarMain.addAction(publishTrans_action)

        toolbarMain.addSeparator()


            #add button
        addButton_action = QAction(QIcon(self.ressourcePath + "/icon/plus.png"), "ADD", self)
        addButton_action.setStatusTip("add ce que tu veux ma couille")
        addButton_action.triggered.connect(self.addMore)
        toolbarMain.addAction(addButton_action)

        toolbarMain.addSeparator()

            #refreshButton
        refreshButton = QAction(QIcon(self.ressourcePath + "/icon/arrow-circle.png"), "refresh",self)
        refreshButton.setStatusTip("refresh si tu vois pas")
        refreshButton.triggered.connect(self.refreshUI)
        toolbarMain.addAction(refreshButton)

        ##tabs
        self.tabs = QTabWidget(self)
        self.tabs.setTabPosition(QTabWidget.North)
        self.tabs.setMovable(False)
        self.tabs.setDocumentMode(True)
        self.tabs.currentChanged.connect(self.tabindex)
        self.setCentralWidget(self.tabs)


        ##asset_ToolBox
        
        self.asset_ToolBox = QToolBox()
        self.asset_ToolBox = self.toolboxPages.setAssetToolbox(self.asset_ToolBox)   
        self.asset_MainLayout = QVBoxLayout()
        self.asset_MainLayout.addWidget(self.asset_ToolBox)
        self.assetWidget = QWidget()
        self.assetWidget.setLayout(self.asset_MainLayout)
        
        
        


        ##shot_Toolbox
        self.shot_ToolBox = QToolBox()
        self.shot_ToolBox = self.toolboxPages.setShotToolbox(self.shot_ToolBox)
        self.shot_MainLayout = QVBoxLayout()
        self.shot_MainLayout.addWidget(self.shot_ToolBox)
        self.shotWidget = QWidget()
        self.shotWidget.setLayout(self.shot_MainLayout)
        
       

        ##addTab
        self.tabs.addTab(self.assetWidget, 'Asset manager')
        self.tabs.addTab(self.shotWidget, 'Shot manager')
        texture_manager = QLabel("en travaux")
        self.tabs.addTab(texture_manager, 'Texture manager')
        

        


        self.addToolBar(toolbarMain)
        self.setStatusBar(QStatusBar(self))

        AssetMainWindow.instance = self
    
    def tabindex(self):
        return self.tabs.currentIndex()

    def indentationBackup(self):
        self.fileManagment.indent()
        

    def savePublish(self):
        self.fileManagment.publish()
        

    def addMore(self):

        if self.tabindex() == 0 :
            
            self.add.addAssetWindow(self.refreshUI)
        elif self.tabindex() == 1:
            
            self.add.addShotWindow(self.refreshUI) 
        elif self.tabindex() == 2:
            
            Add.addTextureWindow(self) 


    def refreshUI(self):           
        if self.tabindex() == 0:
            self.asset_ToolBox = Refresh.refresh(self, self.asset_ToolBox, 0)
            self.asset_MainLayout.addWidget(self.asset_ToolBox)

        elif self.tabindex()==1:
            self.shot_ToolBox = Refresh.refresh(self, self.shot_ToolBox, 1)
            self.shot_MainLayout.addWidget(self.shot_ToolBox)

        elif self.tabindex()==2:
            pass
    
    def closeEvent(self, event):
        """Réinitialise l'instance lorsqu'elle est fermée."""
        AssetMainWindow.instance = None
        event.accept()
    

    def p_outputFile (self):
        path = os.path.join(data.Main_Path, '04_asset/publish_output')
        os.startfile(path)


    def transfertPublish(self):
        output_folder = os.path.join(data.Main_Path, r'04_asset\publish_output')
        input_folder = os.path.join(data.Main_Path, r'04_asset\publish_input')
        
        for root, dirs, files in os.walk(output_folder):
            relative_path = os.path.relpath(root, output_folder)
            target_dir = os.path.join(input_folder, relative_path)

            if not os.path.exists(target_dir):
                os.makedirs(target_dir)

            for file_name in files:
                output_file = os.path.join(root, file_name)
                input_file = os.path.join(target_dir, file_name)

                try:
                    if os.path.exists(input_file):
                        output_mtime = os.path.getmtime(output_file)
                        input_mtime = os.path.getmtime(input_file)

                        if output_mtime > input_mtime:
                            print(f"Mise à jour de '{input_file}' (plus ancien).")
                            shutil.copy2(output_file, input_file)
                        else:
                            print(f"'{input_file}' est déjà à jour.")
                    else:
                        print(f"Copie de '{output_file}' vers '{input_file}'.")
                        shutil.copy2(output_file, input_file)
                except PermissionError as e:
                    print(f"Erreur d'accès au fichier '{output_file}' : {e}. Ignoré.")
                except Exception as e:
                    print(f"Erreur lors de la copie de '{output_file}' vers '{input_file}' : {e}. Ignoré.")