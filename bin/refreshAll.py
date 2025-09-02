import os
from PySide2.QtCore import*
from PySide2.QtWidgets import*
from PySide2.QtGui import *
import sys
from pages import*


class Refresh(ToolboxPages):
    
    def __init__(self,toolbox):
        super().__init__() 
        self.toolboxPages = ToolboxPages()

    def refresh (self, toolbox,num):
        if num == 0:
            toolbox.deleteLater()
            toolbox = QToolBox()
            toolbox = self.toolboxPages.setAssetToolbox(toolbox)
            return toolbox
        elif num == 1:
            toolbox.deleteLater()
            toolbox = QToolBox()
            toolbox = self.toolboxPages.setShotToolbox(toolbox)
            return toolbox