import os
from PySide2.QtCore import*
from PySide2.QtWidgets import*
from PySide2.QtGui import *
import sys
import shutil
import maya.cmds as cmds
import data
import re


class FileManagment():
    def __init__(self):
        super().__init__()
        self.address = data.Main_Path
        self.publishWindow = None
        self.importWindow = None

    def mayaScene(self, path, project, name):
        templateMaya = data.Ressource_Path + "/Templates/mayaTemplate.ma"

        Editliste = os.listdir(path)
        fileCheckState = cmds.file(q=True, modified = True)
        maya_or_houdini = {
            'modeling' : True,
            'rigging' : True,
            'lookdev' : False,
            'groom' : False,
            'cfx' : True,
            'layout' : True,
            'anim' : True,
            'light' : False,
            'fx' : False,
            'rendu' : False,

        }
        if maya_or_houdini.get(name):

            if Editliste == [] :
                userChoice = self.createDialog()
                if userChoice:
                    name_mapping = {
                        'modeling': 'mod',
                        'rigging': 'rig',
                        'lookdev': 'lkd'
                    }
                    name = name_mapping.get(name, name)
    
                    new_name = project +'_'+ name +'_E_v001.ma'
                    new_path = path + '/' + new_name
                    shutil.copy(templateMaya, new_path)  
    
                    if fileCheckState :
                        userChoice2 = self.saveDialog()
                        if userChoice2 == 'save':
                            cmds.file(s = True)
                            cmds.file(new_path, o=True)
                            self.setProject(new_path)
    
                        elif userChoice2 == 'discard':
                            cmds.file(new=True, force=True) 
                            cmds.file(new_path, open=True)
                            self.setProject(new_path)
    
                        elif userChoice2 == "cancel":
                            return
                    else:
                        cmds.file(new_path, o=True)
                        self.setProject(new_path)
    
                elif not userChoice:
                    return
            elif not Editliste == []:
                if Editliste[0] == ".mayaSwatches":
                    openScene = Editliste[1]
                else :
                    openScene = Editliste[0]
                filePath = path + '/' + openScene
                if fileCheckState:
                    userChoice2 = self.saveDialog()
                    if userChoice2 == 'save':
                        cmds.file(s = True)
                        cmds.file(filePath, o=True)
                        self.setProject(filePath)
    
                    elif userChoice2 == 'discard':
                        cmds.file(new=True, force=True) 
                        cmds.file(filePath, open=True)
                        self.setProject(filePath)
    
                    elif userChoice2 == "cancel":
                        return
                else:
                    cmds.file(filePath, o=True)
                    self.setProject(filePath)
        else :
            dlg = QMessageBox(self)
            dlg.setWindowTitle('Not Here')
            dlg.setText('Go to houdini!')
            dlg.setStandardButtons(QMessageBox.Ok)
            dlg.setIcon(QMessageBox.Warning)
            button = dlg.exec()
            if button == QMessageBox.Ok:
                pass

    def importAsset(self, path):
        def show_dialog(title, text, buttons=None, icon=None, custom_buttons=None):
            dlg = QMessageBox(self)
            dlg.setWindowTitle(title)
            dlg.setText(text)
            if icon:
                dlg.setIcon(icon)
            if custom_buttons:
                button_map = {}
                for label in custom_buttons:
                    button = dlg.addButton(label, QMessageBox.ActionRole)
                    button_map[label] = button
                dlg.exec()
                for label, button in button_map.items():
                    if dlg.clickedButton() == button:
                        return label
            elif buttons:
                dlg.setStandardButtons(buttons)
                return dlg.exec()
    
        def get_first_file(directory):
            files = os.listdir(directory) if os.path.exists(directory) else []
            return os.path.join(directory, files[0]) if files else None
    
        def handle_import(file_path, as_reference):
            if as_reference:
                cmds.file(file_path, r=True, mergeNamespacesOnClash=True, namespace=":")
            else:
                cmds.file(file_path, i=True, usingNamespaces=False)
    
        ma_publish_path = path.replace('edit', 'publish')
        file_name = extract_assetFileName(path)
        scene_type = path.split('/')[-1]
        usd_publish_path = os.path.join(data.Main_Path, r'04_asset\publish_output', file_name, scene_type)
    
        ma_file = get_first_file(ma_publish_path)
        usd_file = get_first_file(usd_publish_path)
        edit_file = get_first_file(path)
    
        if not ma_file and not usd_file:
            if edit_file:
                if show_dialog('Import?', 'Publish not found, do you want to import last edit?',
                               QMessageBox.Yes | QMessageBox.No, QMessageBox.Warning) == QMessageBox.Yes:
                    handle_import(edit_file, as_reference=False)
            else:
                print('No files found in the path:', path)
            return
    
        if not usd_file and not ma_file and edit_file:
            if show_dialog('Import?', 'USD Publish not found, do you want to import last edit?',
                           QMessageBox.Yes | QMessageBox.No, QMessageBox.Warning) == QMessageBox.Yes:
                handle_import(edit_file, as_reference=False)
            return
    
        if ma_file and usd_file:
            choice = show_dialog('Choice', '.ma or .usd', icon=QMessageBox.Question, custom_buttons=["ma", "usd"])
            selected_file = ma_file if choice == "ma" else usd_file
        else:
            selected_file = ma_file or usd_file
    
        if selected_file == ma_file:
            as_reference = show_dialog('Import Publish', 'Import reference?',
                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.Question) == QMessageBox.Yes
            handle_import(ma_file, as_reference=as_reference)
        else:
            handle_import(usd_file, as_reference=False)
    

    def createDialog(self):
        dlg =QMessageBox(self)
        dlg.setWindowTitle('Create')
        dlg.setText("la scene n'existe pas, voulez vous la créer?")
        dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        dlg.setIcon(QMessageBox.Question)
        button = dlg.exec()
        if button == QMessageBox.Yes:
            return True
        elif button == QMessageBox.No:
            return False

    def saveDialog(self):
        dlg =QMessageBox(self)
        dlg.setWindowTitle('Save')
        dlg.setText("Sauvegarder la scene avant de quitter ?")
        dlg.setStandardButtons(QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
        dlg.setIcon(QMessageBox.Question)
        button = dlg.exec()
        if button == QMessageBox.Save:
            return 'save'
        elif button == QMessageBox.Discard:
            return 'discard'
        elif button == QMessageBox.Cancel:
            return 'cancel'


    def setProject(self, path):
        current_directory = os.path.dirname(path)
        while current_directory:
            workspace_mel_path = os.path.join(current_directory, "workspace.mel")
        
            # Vérifier si le fichier workspace.mel existe dans ce répertoire
            if os.path.exists(workspace_mel_path):
                break  # Sortir de la boucle si trouvé   
    
            # Remonter d'un niveau dans les répertoires
            parent_directory = os.path.dirname(current_directory)
    
            # Si on est remonté jusqu'à la racine du système de fichiers, on arrête la boucle
            if parent_directory == current_directory:
                print("Arrivé à la racine du système, aucun workspace.mel trouvé.")
                break
        
            current_directory = parent_directory

        cmds.workspace(current_directory, openWorkspace=True)

    def padding(self, num, padding):
        lenNum = len(str(num))
        nbrZero = padding - lenNum
        stringNum = '0'*nbrZero + str(num)
        return stringNum


    def indent(self):
        filePath = cmds.file(q=True, sn=True)
        sceneName = os.path.basename(filePath)
        sceneName = sceneName.split('.')[0]
        # os.path.splitext(sceneName)[0]
        print('indent: ', sceneName)

        if 'edit'in filePath:
            inc = sceneName.split('_')[-1].split('v')[-1]
            incNew = str(int(inc) + 1)
            incNew = self.padding(incNew, 3)
            incNew = 'v' + incNew
            inc = 'v' + inc
            newName = sceneName.replace(inc, incNew)
            print('nouveau nom: ', newName)


            backupPath = os.path.dirname(filePath)
            backupPath = backupPath.replace('edit','backup')

            customPath = os.path.join(os.path.dirname(filePath), newName)
            print('nouveau file: ', customPath)
            cmds.file(rename = customPath)
            cmds.file(s=True, f=True, type='mayaAscii')

            print("MOVE FROM", filePath, " TO ", backupPath)

            shutil.move(filePath, backupPath)


        elif 'backup' in filePath:
            backupPath = os.path.dirname(filePath)
            editPath = backupPath.replace('backup', 'edit')
            editScene = os.listdir(editPath)[0]
            
            inc = editScene.split('_')[-1].split('v')[-1].split('.')[0]
            
            incNew = str(int(inc) + 1)
            
            incNew = self.padding(incNew, 3)
            sceneName = editScene.split('.')[0]
            incNew = 'v' + incNew
            inc = 'v' + inc
            newName = sceneName.replace(inc, incNew)
            
            customPath = os.path.join(editPath, newName)

            cmds.file(rename = customPath)
            cmds.file(s=True, f=True, type='mayaAscii')

            oldScene = os.path.join(editPath, editScene)
            shutil.move(oldScene, backupPath)

        elif 'publish' in filePath:
            cmds.error("T'es dans le publish tête de noeud")


    def openBackup(self, path):
        if 'backup' in path:
            cmds.error("already in backup")

        elif 'edit': 
            backupPath = path.replace('edit', 'backup')
            dialog = QFileDialog(None, "selectionner un backup", backupPath)
            dialog.setFileMode(QFileDialog.ExistingFile)

            selected_file = ''

            if dialog.exec_():
                filenames = dialog.selectedFiles()
                fileCheckState = cmds.file(q=True, modified = True)
                if fileCheckState:
                    userChoice = self.saveDialog()
                    if userChoice == 'save':
                        cmds.file(s=True)
                        cmds.file(filenames, o = True)
                        self.setProject(filenames)

                    elif userChoice == 'discard':
                        cmds.file(new=True, force=True)
                        cmds.file(filenames, open=True)
                        self.setProject(filenames)

                    elif userChoice2 == "cancel":
                        return
                else : 
                    cmds.file(filenames, o=True)
                    self.setProject(filenames)



    def publish(self):
        if self.publishWindow is None:
            self.publishWindow = PublishWindow()
        self.publishWindow.show()
        
    def fbxPublish(self):
        path = cmds.file(q = True, sn = True)
        name = path.split('/')[-1].split('.')[0].replace('_P','_Smooth')
        version = path.split('_')[-1]
        path = path.replace(version,'')
        name = path.split('/')[-1].split('.')[0].replace('_E_','_Smooth')

        path = cmds.workspace(fn=True)
        path = path.replace('maya', 'substancePainter')
        path += '/fbx/' + name

        cmds.file(path, force=True, exportSelected = True, type= 'FBX export')
        


class PublishWindow(QWidget):
    def __init__(self):
        super().__init__()


        self.setWindowTitle("Publish")
        self.resize(300, 100)

        self.mainLayout = QVBoxLayout()

        #check box

        self.checkLayout = QHBoxLayout()
        self.USDBox = QRadioButton('USD')
        self.maBox = QRadioButton('.ma')
        

        self.checkLayout.addWidget(self.USDBox)
        self.checkLayout.addWidget(self.maBox)
        

        self.boxsWidget = QWidget()
        self.boxsWidget.setLayout(self.checkLayout)

        self.mainLayout.addWidget(self.boxsWidget)

        #buttons

        self.buttonLayout = QHBoxLayout()
        self.exportButton = QPushButton('Export')
        self.cancelButton = QPushButton('Cancel')

        self.buttonLayout.addWidget(self.exportButton)
        self.buttonLayout.addWidget(self.cancelButton)

        self.buttonsWidget = QWidget()
        self.buttonsWidget.setLayout(self.buttonLayout)


        self.exportButton.clicked.connect(self.export)
        self.cancelButton.clicked.connect(self.cancel)

        self.mainLayout.addWidget(self.buttonsWidget)


        self.setLayout(self.mainLayout)

    def export(self):


        if cmds.ls(sl=True) ==[]:
            cmds.framelessDialog (title='Error', message='Nothing selected in the outliner',button=['OK'], primary=['OK'])
            cmds.error('nothing selected in the outliner')
            self.close()
        else: 
            if self.USDBox.isChecked():
                fileName = cmds.file(q=True, sn=True).split('/')[-1].split('_E_')[0]
                type = fileName.split('_')[-1]
                name = extract_assetFileName(cmds.file(q=True,sn=True))
                name_mapping = {
                        'mod': 'modeling',
                        'rig': 'rigging',
                        'lkd': 'lookdev'
                    }
                type = name_mapping.get(type,type)
                path = os.path.join(data.Main_Path, r'04_asset\publish_output', name, type)
                if not os.path.exists(path):
                    os.makedirs(path)
                if os.listdir(path) == []:
                    fileName += '_P'
                    path = os.path.join(path, fileName +'.usd')
                    option = optionUSD()
                    cmds.file( 
                    path, force=True, exportSelected=True, preserveReferences=False, type='USD Export',
                    options=f"{option}"
                    )
                    self.close()
                else :
                    fileName += '_P'
                    path = os.path.join(path, fileName +'.usd')
                    option = optionUSD()
                    os.remove(path)
                    cmds.file(
                    path, force=True, exportSelected=True, preserveReferences=False, type='USD Export',
                    options=f"{option}"
                    )
                    self.close()
                    
            elif self.maBox.isChecked():
                path = cmds.file(q=True, sn=True)
                version = path.split('_')[-1]
                path = path.replace(version,'')
                path = path.replace('_E_','_P')
                path = path.replace('edit', 'publish')
        
                cmds.file(path, force=True, exportSelected = True, shader=True, type = 'mayaAscii')
                self.close()
            
            else:
                cmds.framelessDialog (title='Error', message='Nothing selected',button=['OK'], primary=['OK'])
                self.close()



    def cancel(self):
        self.close()



def optionUSD():
    path = cmds.file(q=True, sn=True).lower()
    frame_in = cmds.playbackOptions(q=True, min = True)
    frame_out = cmds.playbackOptions(q=True, max = True)
    if "04_asset" in path :
        USDoption =( 
            ";exportUVs=1; exportSkels=none; exportBlendShapes=0; exportDisplayColor=0; exportColorSets=1;"
            "exportComponentTags=1; defaultMeshScheme=catmullClark; animation=0; eulerFilter=0;"
            "staticSingleSample=0;startTime=0;endTime=30;frameStride=1;frameSample=0.0;defaultUSDFormat=usdc;"
            "rootPrimType=xform;convertMaterialsTo=[];"
            "exportRelativeTextures=automatic;exportInstances=1;exportVisibility=1;"
            "mergeTransformAndShape=1;stripNamespaces=1;worldspace=0;excludeExportTypes=[Cameras,Lights]"
        )
    elif "05_shot" in path :
        USDoption = ( 
            f";exportUVs=1;exportSkels=none;exportSkin=none;exportBlendShapes=0;exportDisplayColor=0;exportColorSets=1;"
            f"exportComponentTags=1;defaultMeshScheme=catmullClark;animation=1;eulerFilter=1;staticSingleSample=0;"
            f"startTime={frame_in};endTime={frame_out};frameStride=1;frameSample=0.0;defaultUSDFormat=usdc;rootPrim=;rootPrimType=scope;"
            f"shadingMode=useRegistry;convertMaterialsTo=[];exportRelativeTextures=automatic;exportInstances=0;"
            f"exportVisibility=0;mergeTransformAndShape=0;stripNamespaces=1;worldspace=0;excludeExportTypes=[Cameras,Lights]"
        )
    return USDoption



def extract_assetFileName(path):
    normalized_path = path.replace('/', '\\')
    # Utilisation d'une expression régulière pour capturer le "targetx"
    match = re.search(r'\\([^\\]+)\\maya\\', normalized_path)
    if match:
        return match.group(1)  # Retourne la capture du groupe
    return None  # Retourne None si aucun match n'est trouvé