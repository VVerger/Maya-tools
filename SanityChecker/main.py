## sanity checker 
# cam != [pers, top etc]
# pas de doublons de noms
# pas de [pCubex, spaceLocatorx, nurbesCirclex etc]
# moteur == renderman
# format != hd540
# subdivScheme

import maya.cmds as cmds
from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2 import QtUiTools, QtWidgets

class SanityChecker:
	"""docstring for SanityChecker"""
	def __init__(self):
		self.engine = "renderman"
		self.allObj = [obj.split('|')[-1] for obj in cmds.ls(et = ['mesh', 'transform'])]

	def checkScene(self):
		self.popupErrors = PopupErrors(self.getError())

	def getError(self):
		Errorlist = []
		Errorlist.append(self.checkCam())
		Errorlist.append(self.doubleName())
		Errorlist.append(self.checkObjName())
		Errorlist.append(self.checkEngine())
		Errorlist.append(self.checkFormat())
		Errorlist.append(self.checkcatmull())
		return Errorlist

	def checkCam(self):
		out = []
		cams = cmds.ls(type='camera')
		for cam in cams:
			renderable = cmds.getAttr(f'{cam}.renderable')
			if renderable:
				out.append(cam)
		currentCam = out[0]

		cameras = cmds.ls(type=('camera'))
		startup_cameras = [camera for camera in cameras if cmds.camera(cmds.listRelatives(camera, parent=True)[0], startupCamera=True, q=True)]
		if currentCam in startup_cameras:
			#cmds.warning("error camera")
			return 'Warning : error camera'
		else:
			return (f'{currentCam} is renderable')


	def doubleName(self):
		doublons=[]
		for obj in self.allObj:
			if self.allObj.count(obj) > 1:
				if not obj in doublons :
					doublons.append(obj)
		if doublons != []:
			#cmds.warning(f'double names:, {doublons}')
			#cmds.warning(f'double names: {", ".join(map(str, doublons))}')
			return (f'Warning : double names: {", ".join(map(str, doublons))}')
		else:
			return 'no duplicates names'


	def checkEngine(self):
		currentRender = cmds.getAttr("defaultRenderGlobals.currentRenderer")
		if not currentRender == self.engine:
			#cmds.warning("error engine")
			return 'Warning : error engine'
		else:
			return f'{self.engine} engine'


	def checkObjName (self):
		baseName = ['pCube', 'pSphere', 'pCylinder', 'pCone', 'pTorus', 'pPlane', 'pDisc', 'locator', 'nurbsCircle', 'square', 'cube', 'arrow']
		listName =[]
		for base in baseName:
			for obj in self.allObj:
				if base in obj :
					if not obj in listName:
						listName.append(obj)
		if listName != []:
			#cmds.warning(f'base named found : {", ".join(map(str,listName))}')
			return f'Warning : base named found : {", ".join(map(str,listName))}'
		else:
			return 'no base name'

	def checkFormat (self):
		h=cmds.getAttr("defaultResolution.height")
		if h == 540:
			#cmds.warning("format error")
			return 'Warning format = 540'
		else:
			return 'format is ok'
		

	def checkcatmull (self):
		Objects = cmds.ls(exactType = 'mesh')
		listNotSmoth = []
		for obj in Objects :
			smooth = cmds.getAttr(f"{obj}.rman_subdivScheme")
			if smooth != 1 : 
				listNotSmoth.append(obj)
		if listNotSmoth != []:
			#cmds.warning(f'Subdiv Scheme Off : {", ".join(map(str,listNotSmoth))}')
			return f'Warning : Subdiv Scheme Off : {", ".join(map(str,listNotSmoth))}'
		else:
			return 'subdivScheme On'



class PopupErrors(QMainWindow):
	def __init__(self,listerror):
		super().__init__()
		self.listError = listerror

		self.uiFile = "F:\\CODE\\module_python\\SanityChecker\\sanity_checker.ui"

		loader = QtUiTools.QUiLoader()
		self.ui = loader.load(self.uiFile, parentWidget = self)

		#Cam
		self.checkButton = self.ui.findChild(QtWidgets.QPushButton, "checkButton")
		self.repairButton = self.ui.findChild(QtWidgets.QPushButton, "repairButton")
		self.showtext = self.ui.findChild(QtWidgets.QTextBrowser, "showtext")
		self.camBox = self.ui.findChild(QtWidgets.QCheckBox, "camBox")
		self.formatbox = self.ui.findChild(QtWidgets.QCheckBox, "formatbox")
		self.engineBox = self.ui.findChild(QtWidgets.QCheckBox, "engineBox")
		self.duplicatesBox = self.ui.findChild(QtWidgets.QCheckBox, "duplicatesBox")
		self.basenamebox = self.ui.findChild(QtWidgets.QCheckBox, "basenamebox")
		self.catmullBox = self.ui.findChild(QtWidgets.QCheckBox, "catmullBox")
		self.checkButton.clicked.connect(self.check)
		self.repairButton.clicked.connect(self.repair)


		self.show()


	def check(self):
		checklist = []

		if self.formatbox.isChecked() :
			ErrorFormat = self.listError[4]
			checklist.append(ErrorFormat)

		if self.duplicatesBox.isChecked() :
			ErrorDup = self.listError[1]
			checklist.append(ErrorDup)

		if self.basenamebox.isChecked() :
			ErrorBase = self.listError[2]
			checklist.append(ErrorBase) 

		if self.catmullBox.isChecked() :
			ErrorCatmull = self.listError[5]
			checklist.append(ErrorCatmull)
		
		if self.engineBox.isChecked() :
			ErrorEngine = self.listError[3]
			checklist.append(ErrorEngine)

		if self.camBox.isChecked() :
			ErrorCam = self.listError[0]
			checklist.append(ErrorCam)


		message = '{}'.format("\n ".join(map(str,checklist)))
		self.showtext.setText(message)

	
	def repair(self):

		if self.engineBox.isChecked() :
			cmds.setAttr("defaultRenderGlobals.currentRenderer", "renderman", type="string")

		if self.formatbox.isChecked():
			pAx = maya.cmds.getAttr("defaultResolution.pixelAspect")
			pAr = maya.cmds.getAttr("defaultResolution.deviceAspectRatio")
			maya.cmds.setAttr("defaultResolution.aspectLock", 0)
			maya.cmds.setAttr("defaultResolution.width", 1920)
			maya.cmds.setAttr("defaultResolution.height", 1080)
			maya.cmds.setAttr("defaultResolution.pixelAspect", pAx)
			maya.cmds.setAttr("defaultResolution.deviceAspectRatio", pAr)

		if self.catmullBox.isChecked() :
			Objects = cmds.ls(exactType = 'mesh')
			
			for obj in Objects :
				smooth = cmds.getAttr(f"{obj}.rman_subdivScheme")
				water = cmds.getAttr(f"{obj}.rman_watertight")
				poly = cmds.getAttr(f"{obj}.rman_preventPolyCracks")
				if smooth != 1 : 
					cmds.setAttr(f"{obj}.rman_subdivScheme", 1)
				if water != 1 : 
					cmds.setAttr(f"{obj}.rman_watertight", 1)
				if poly != 1 : 
					cmds.setAttr(f"{obj}.rman_preventPolyCracks", 1)


		self.close()

sanityChecker = SanityChecker()
sanityChecker.checkScene()