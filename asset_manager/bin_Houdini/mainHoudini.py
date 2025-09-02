import sys
from PySide2 import QtCore, QtWidgets
from uiHoudini import AssetMainWindow  # Import de AssetMainWindow

def launcher():
    # Vérifie s'il existe déjà une instance de QApplication
    app = QtWidgets.QApplication.instance()
    
    # Si aucune instance n'existe, on en crée une
    if not app:
        app = QtWidgets.QApplication(sys.argv)

    def show_window():
        # Si aucune fenêtre n'existe, on en crée une nouvelle
        if AssetMainWindow.instance is None:
            window = AssetMainWindow()
            window.show()
        else:
            # Si la fenêtre existe déjà, on la ramène au premier plan
            AssetMainWindow.instance.raise_()
            AssetMainWindow.instance.activateWindow()

    # Utiliser QTimer pour différer l'exécution après la configuration de Houdini
    QtCore.QTimer.singleShot(0, show_window)


#import mainHoudini as mH
#mH.launcher()
