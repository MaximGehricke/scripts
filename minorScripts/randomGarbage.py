#change speed on v project
import hou

nodes = hou.selectedNodes()
parmsToAffect = ["speed1x","speed1y","speed2x","speed2y","speed3x","speed3y","speed4x","speed4y","speed","flow_speed_mult","flow_speed_mult2"]

input = str(hou.ui.readInput("expression pls")[1])

for node in nodes:
    for parm in node.parms():
        for name in parmsToAffect:
            if parm.name()==name:
                print(parm.name())
                parmVal = parm.rawValue()
                parm.setExpression(str(parmVal)+input)



#SLManager

import hou
node = hou.node('/obj/sl_sequence_manager1')
desktop = hou.ui.curDesktop()
if node is not None:
    desktop = hou.ui.curDesktop()
    fp = desktop.createFloatingPane(hou.paneTabType.Parm)
    fp.setCurrentNode(node)




#setCam
#sets current SL camera 
#icon = OBJ_camera
#hotkey = F7

import hou

def get_viewport_cameras():
    desktop = hou.ui.curDesktop()
    scene_viewer = desktop.paneTabOfType(hou.paneTabType.SceneViewer)
    if not scene_viewer:
        return []

    camera_list = []
    for viewport in scene_viewer.viewports():
        camera = viewport.camera()
        if camera:
            camera_list.append((viewport, camera.path()))
    return camera_list

def set_camera_from_sql_current_shot():
    seq_manager_node = hou.node('/obj/sl_sequence_manager1')
    if not seq_manager_node:
        hou.ui.displayMessage("Node 'sl_sequence_manager1' not found.")
        return

    sql_current_shot_param = seq_manager_node.parm('SQL_Current_Shot')
    if not sql_current_shot_param:
        hou.ui.displayMessage("Parameter 'SQL_Current_Shot' not found.")
        return

    current_shot = sql_current_shot_param.eval()
    camera_path = f'/obj/{current_shot}_render'
    new_camera = hou.node(camera_path)

    if not new_camera:
        print(f"Camera '{camera_path}' does not exist.")
        return

    desktop = hou.ui.curDesktop()
    scene_viewer = desktop.paneTabOfType(hou.paneTabType.SceneViewer)
    if scene_viewer:
        first_viewport = scene_viewer.viewports()[3]
        first_viewport.setCamera(new_camera)
        print(f"Viewport camera set to: {camera_path}")

def switch_camera_name(cameras):
    for viewport, first_camera in cameras:
        new_camera_name = first_camera[:-7] if first_camera.endswith('_scaled') else first_camera + '_scaled'
        new_camera = hou.node(new_camera_name)
        if new_camera:
            viewport.setCamera(new_camera)
            print(f"Viewport camera changed to: {new_camera_name}")
        else:
            print(f"Camera '{new_camera_name}' does not exist.")

cameras = get_viewport_cameras()

if cameras:
    switch_camera_name(cameras)
else:
    set_camera_from_sql_current_shot()



import hou
node = "/obj/fx_balefire/OUT_balefireROD"

n = hou.node(node)
n.setTemplateFlag(1)


# Get a reference to the geometry viewer
pane = hou.ui.curDesktop().paneTabOfType(hou.paneTabType.SceneViewer)
# Get the display settings
settings = pane.curViewport().settings()
# Get the GeometryViewportDisplaySet for objects
tmplset = settings.displaySet(hou.displaySetType.TemplateModel)

tmplset.setShadedMode(hou.glShadingType.Smooth)
tmplset.useGhostedLook(0)
