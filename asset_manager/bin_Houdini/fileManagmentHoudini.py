import os
from PySide2.QtCore import*
from PySide2.QtWidgets import*
from PySide2.QtGui import *
import sys
import shutil
import data
import hou
import re


class FileManagment():
    def __init__(self):
        super().__init__()
        self.address = data.Main_Path
        self.publishWindow = None

        hou.putenv('HIP', data.Main_Path.replace('\\','/'))
        #current_hip = hou.getenv('HIP')
        #print(f"Current $HIP: {current_hip}")

    def houdiniScene(self, path, project, name):
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
        if not maya_or_houdini.get(name):
            
            pathList  = os.listdir(path)

            if pathList == []:
                user_choice = self.createDialog()
                name_mapping = {
                    'lookdev': 'lkd',
                    'light' : 'lgt'
                }
                name = name_mapping.get(name, name)

                if user_choice:
                    if name == 'lkd':
                        Template = os.path.join(data.Ressource_Path,'Templates/houdini_Templates/houdiniLookdev_Template.hipnc')
                        finalPath = os.path.join(path, project + "_lkd_E_v001.hipnc")
                    elif name == 'groom':
                        Template = os.path.join(data.Ressource_Path,'Templates/houdini_Templates/houdiniGroom_Template.hipnc')
                        finalPath = os.path.join(path, project + "_groom_E_v001.hipnc")
                    elif name == 'lgt':
                        Template = os.path.join(data.Ressource_Path,'Templates/houdini_Templates/houdiniLight_Template.hipnc')
                        finalPath = os.path.join(path, project + "_lgt_E_v001.hipnc")
                    elif name == 'fx':
                        Template = os.path.join(data.Ressource_Path,'Templates/houdini_Templates/houdiniFX_Template.hipnc')
                        finalPath = os.path.join(path, project + "_FX_E_v001.hipnc")
                    elif name == 'rendu':
                        Template = os.path.join(data.Ressource_Path,'Templates/houdini_Templates/houdiniRendu_Template.hipnc')
                        finalPath = os.path.join(path, project + "_rendu_E_v001.hipnc")


                    shutil.copy(Template, finalPath)

                    finalPath = finalPath.replace('\\','/')
        
                    hou.hipFile.load(finalPath, suppress_save_prompt=False, ignore_load_warnings=False)

                else:
                    return

            elif not pathList == []:
                finalPath = path + '/'+ pathList[0]
                finalPath = finalPath.replace('\\','/')

                hou.hipFile.load(finalPath, suppress_save_prompt=False, ignore_load_warnings=False)

        else :
            dlg = QMessageBox(self)
            dlg.setWindowTitle('Not Here')
            dlg.setText('Go to Maya!')
            dlg.setStandardButtons(QMessageBox.Ok)
            dlg.setIcon(QMessageBox.Warning)
            button = dlg.exec()
            if button == QMessageBox.Ok:
                pass


    def importAsset(self, path):

        publishInput_path = os.path.join(data.Main_Path , r'04_asset\publish_input')
        if os.path.exists(path):
            assetPublishListe = os.listdir(path)
            item_with_setDress = next((item for item in assetPublishListe if 'setDress' in item), None)
    
            if item_with_setDress:
                publishInput_path = os.path.join(publishInput_path, item_with_setDress)
    
                if os.path.exists(publishInput_path):
                    publishList = os.listdir(publishInput_path)
                    if publishList == []:
                        print ('no publish')
                        return
                    publishItem = [x for x in publishList if not '.usdc' in x][0]
                    publishItem_Path = os.path.join(publishInput_path, publishItem)
                    publishItem_Path = publishItem_Path.replace('\\','/')
                    stage = hou.node('/stage')
                    name = publishItem.split('.usd')[0]
                    refNode = stage.createNode('reference', name)
                    refNode.parm("filepath1").set(publishItem_Path)
                    refNode.setName(name, unique_name=True)
                else:
                    print('publish file not found')
                    return
        else:
            fileName = extract_assetFileName(path)
            scene_type = path.split('/')[-1]
            publishInput_path =os.path.join(publishInput_path, fileName, scene_type)
            
            if os.path.exists(publishInput_path):
                publishList = os.listdir(publishInput_path)
                if publishList == []:
                    print('no publish')
                    return
                publishItem = [x for x in publishList if not '.usdc' in x][0]
                publishItem_Path = os.path.join(publishInput_path, publishItem)
                publishItem_Path = publishItem_Path.replace('\\','/')
                stage = hou.node('/stage')
                name = publishItem.split('.usd')[0]
                refNode = stage.createNode('reference', name)
                refNode.parm("filepath1").set(publishItem_Path)
                refNode.setName(name, unique_name=True)
            else:
                print('publish file not found')
                return



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


    def create_setDress(self, path):
        setName = path.split('/')[-1]
        name = 'setDress_' + setName
        setDress_Template = data.Ressource_Path + '/Templates/houdini_Templates/setDress_Template'
        path_setDress = path +'/'+ name

        fileCheckState = hou.hipFile.hasUnsavedChanges()


        if os.path.exists(path_setDress):           
            setDress_scene = os.path.normpath(os.path.join(path_setDress, 'houdini', 'edit'))
            sceneName = os.listdir(setDress_scene)[0]

            newName = os.path.join(setDress_scene, sceneName)
            newName = newName.replace('\\','/')
            hou.hipFile.load(newName,suppress_save_prompt=False, ignore_load_warnings=False)


        else :
            user_choice = self.createDialog()


            if user_choice:

                shutil.copytree(setDress_Template, path_setDress)
                       
                setDress_scene = os.path.normpath(os.path.join(path_setDress, 'houdini','edit'))
                newName = setDress_scene + "\\" + name +"_E_v001.hipnc"   
                os.rename(setDress_scene + '\\houdini_setDress.hipnc', newName)


                newName = newName.replace('\\','/')
                

                if fileCheckState:
                    user_choice2 = self.saveDialog()


                    if user_choice2 == "save":
                        hou.hipFile.save(file_name=None, save_to_recent_files=True)
                        hou.hipFile.load(newName, suppress_save_prompt=False, ignore_load_warnings=False)
                        

                    elif user_choice2 == "discard":
                        hou.hipFile.load(newName, suppress_save_prompt = True, ignore_load_warnings =False)
                        

                    elif user_choice2 == "cancel":
                        return

                else :
                    hou.hipFile.load(newName,suppress_save_prompt = True, ignore_load_warnings =False)
                    

            elif not user_choice:
                return    

    def setProject(self, path):
        pass

    def padding(self, num, padding):
        lenNum = len(str(num))
        nbrZero = padding - lenNum
        stringNum = '0'*nbrZero + str(num)
        return stringNum


    def indent(self):
        filePath = hou.hipFile.path()
        sceneName = hou.getenv("HIPNAME")

        if 'edit' in filePath:
            inc = sceneName.split('_')[-1].split('v')[-1]
            incNew = str(int(inc) + 1)
            incNew = self.padding(incNew, 3)
            incNew = 'v' + incNew
            inc = 'v' + inc
            newName = sceneName.replace(inc, incNew)
            print('nouveau nom: ', newName)

            backupPath = os.path.dirname(filePath)
            backupPath = backupPath.replace('edit','backup')

            newPathName = os.path.join(os.path.dirname(filePath), newName + '.hipnc')
            print('nouveau file: ', newPathName)

            hou.hipFile.save()
            hou.hipFile.save(newPathName)
            print("MOVE FROM", filePath, " TO ", backupPath)
            
            shutil.move(filePath, backupPath)

        elif 'backup' in filePath:
            backupPath = os.path.dirname(filePath)
            editPath = backupPath.replace('backup','edit')
            editSceneName = os.listdir(editPath)[0]
            editFullScene = os.path.join(editPath, editSceneName)


            inc = editSceneName.split('_')[-1].split('v')[-1].split('.')[0]
            incNew = str(int(inc) + 1)
            incNew = self.padding(incNew, 3)
            inc = sceneName.split('_')[-1].split('v')[-1]
            incNew = 'v' + incNew
            inc = 'v' + inc
            newName = sceneName.replace(inc, incNew)

            customPath = os.path.join(editPath, newName + '.hipnc')

            hou.hipFile.save(customPath)
            shutil.move(editFullScene , backupPath)



    def openBackup(self, path):
        if 'backup' in path:
            print("already in backup")
            return
        elif 'edit':
            backupPath = path.replace('edit', 'backup')
            dialog = QFileDialog(None, "selectionner un backup", backupPath)
            dialog.setFileMode(QFileDialog.ExistingFile)

            selected_file = ''
            if dialog.exec_():
                filenames = dialog.selectedFiles()[0]
                hou.hipFile.load(filenames,suppress_save_prompt = True, ignore_load_warnings =False)




    def publish(self):
        pass


def extract_assetFileName(path):
    normalized_path = path.replace('/', '\\')
    if 'houdini' in path:
    # Utilisation d'u   ne expression régulière pour capturer le "targetx"
        match = re.search(r'\\([^\\]+)\\houdini\\', normalized_path)
        if match:
            return match.group(1)  # Retourne la capture du groupe
        return None  # Retourne None si aucun match n'est trouvé
    elif 'maya' in path:
        match = re.search(r'\\([^\\]+)\\maya\\', normalized_path)
        if match:
            return match.group(1)  # Retourne la capture du groupe
        return None  # Retourne None si aucun match n'est trouvé



'''


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
        pass

    def cancel(self):
        self.close()

'''