import maya.cmds as cmd

class Tool():
    def __init__(self):
        self.obj = cmd.ls(typ="transform")

    def search (self, name):
        sel = cmd.ls('*{}*'.format(name), dag = 1)
        listMesh = []
        for obj in sel :
            type = cmd.objectType(obj)
            if type == 'mesh' and cmd.getAttr("{obj}.visibility") == True:
                listMesh.append(obj)
        return listMesh


    def ghost(self, preframe, postframe, step, objs):
        for o in objs:
            cmd.select(o)
            cmd.ghosting( action='ghost', preFrames = int(preframe), postFrames = int(postframe), ghostsStep = int(step) )
    
    def unghost(self,objs):
        for obj in objs :
            cmd.setAttr("{}.ghosting".format(obj), 0)
        
