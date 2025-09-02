import maya.cmds as cmds

def create_offset_groups(suffix="_offset", keep_parent=True):
    selection = cmds.ls(selection=True)

    if not selection:
        cmds.warning("Aucun objet sélectionné.")
        return

    cmds.undoInfo(openChunk=True)

    try:
        for obj in selection:
            parent = cmds.listRelatives(obj, parent=True)
            offset_grp = cmds.group(empty=True, name=f"{obj}{suffix}")

            constraint = cmds.parentConstraint(obj, offset_grp)
            scale_constraint = cmds.scaleConstraint(obj, offset_grp)
            cmds.delete(constraint, scale_constraint)

            if keep_parent and parent:
                cmds.parent(offset_grp, parent[0])

            cmds.parent(obj, offset_grp)

        print("Offset groups créés avec succès.")

    except Exception as e:
        cmds.warning(f"Erreur pendant la création des offset groups : {e}")

    finally:
        cmds.undoInfo(closeChunk=True)


create_offset_groups(suffix="_DRV_GRP", keep_parent=True)

