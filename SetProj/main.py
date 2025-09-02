from pathlib import Path
import maya.cmds as cmds

def find_upwards(start_path, target_file):
    
    path = Path(start_path).resolve()
    for parent in [path] + list(path.parents):
        if (parent / target_file).is_file():
            return parent
    return None

def set_project_from_current_file():
    
    current_file = cmds.file(q=True, sn=True)
    if not current_file:
        cmds.warning("Aucun fichier n'est ouvert.")
        return
    
    workspace_dir = find_upwards(Path(current_file).parent, "workspace.mel")
    
    if workspace_dir:
        try:
            cmds.workspace(str(workspace_dir), openWorkspace=True)
            print(f"Projet défini sur : {workspace_dir}")
        except Exception as e:
            cmds.warning(f"Impossible de définir le projet : {e}")
    else:
        cmds.warning("workspace.mel introuvable en remontant les dossiers.")

# Lance directement
set_project_from_current_file()

