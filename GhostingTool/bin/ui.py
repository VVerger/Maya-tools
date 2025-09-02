import maya.cmds as cmd
from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2 import QtUiTools, QtWidgets, QtCore
from bin.tool import Tool

class GhostingWindow (QMainWindow, Tool):
    def __init__(self):
        super().__init__()
        self.uiFile = "F:\\CODE\\module_python\\GhostingTool\\ressource\\Gosting_window.ui"
        
        loader = QtUiTools.QUiLoader()
        self.ui = loader.load(self.uiFile, parentWidget=self)
       
        self.SearchEdit = self.ui.findChild(QtWidgets.QLineEdit,"SearchEdit")
        self.PreframeEdit = self.ui.findChild(QtWidgets.QLineEdit,"PreframeEdit")
        self.PostframeEdit = self.ui.findChild(QtWidgets.QLineEdit,"PostframeEdit")
        self.StepEdit = self.ui.findChild(QtWidgets.QLineEdit,"StepEdit")

        self.ActivateButton = self.ui.findChild(QtWidgets.QPushButton,"ActivateButton")
        self.ActivateButton.clicked.connect(self.activate)
       
        self.DesactivateButton = self.ui.findChild(QtWidgets.QPushButton,"DesactivateButton")
        self.DesactivateButton.clicked.connect(self.desactivate)
        
        self.show()

    def activate(self):
        Tool.ghost(self.PreframeEdit.text(), self.PostframeEdit.text(), self.StepEdit.text(),Tool.search(self.SearchEdit.text))
        self.close()


    def desactivate(self):
        Tool.unghost(Tool.search(self.SearchEdit.text()))
        self.close()
    
        
        
        


