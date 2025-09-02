from ui import AssetMainWindow
from PySide2.QtWidgets import QApplication
import maya.utils
import sys

def launcher():
    # Assurez-vous qu'il existe une instance unique de QApplication
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
    
    def show_window():
        # Créer une nouvelle instance de la fenêtre, si elle n'existe pas déjà
        if AssetMainWindow.instance is None:
            window = AssetMainWindow()
            window.show()
        else:
            # Si l'instance existe, ramenez-la au premier plan
            AssetMainWindow.instance.raise_()
            AssetMainWindow.instance.activateWindow()
    
    # Utilisez executeDeferred pour afficher la fenêtre correctement dans Maya
    maya.utils.executeDeferred(show_window)
