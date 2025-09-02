import maya.cmds as cmds

def create_offset_groups(suffix="_offset", keep_parent=True):
    selection = cmds.ls(selection=True)

    if not selection:
        cmds.warning("Aucun objet sélectionné.")
        return

    # Démarre un undo chunk
    cmds.undoInfo(openChunk=True)

    try:
        for obj in selection:
            # Récupère le parent de l'objet (s'il y en a un)
            parent = cmds.listRelatives(obj, parent=True)

            # Crée le groupe offset
            offset_grp = cmds.group(empty=True, name=f"{obj}{suffix}")

            # Aligne le groupe en position, rotation et scale sur l'objet
            constraint = cmds.parentConstraint(obj, offset_grp)
            scale_constraint = cmds.scaleConstraint(obj, offset_grp)
            cmds.delete(constraint, scale_constraint)

            # Replace le groupe dans la hiérarchie d'origine
            if keep_parent and parent:
                cmds.parent(offset_grp, parent[0])

            # Reparent l'objet sous son groupe offset
            cmds.parent(obj, offset_grp)

        print("Offset groups créés avec succès.")

    except Exception as e:
        cmds.warning(f"Erreur pendant la création des offset groups : {e}")

    finally:
        # Ferme le undo chunk
        cmds.undoInfo(closeChunk=True)

# Exemple d'exécution
create_offset_groups(suffix="_DRV_GRP", keep_parent=True)
