# hide_camera_view_menu.py
#
# Hides cameras for the sceneview camera and renderview camera dropdown menus.
# Given a selected camera in the obj context, create the soho_viewport_menu and 
# soho_renderview_menu params if needed and set them to false.
# script by Shawn Lipowski

import hou

def cameras_from_selection():

    cameras = []
    for node in hou.selectedNodes():
        if node.type().name() == 'cam' or node.type().name() == 'cm_abc_camera::1.0':
            cameras.append(node)

    return cameras

def append_toggle_hide(node, folder_name, toggle_name, toggle_label, toggle_default):

    ptg = node.parmTemplateGroup()
    folder = ptg.findFolder(folder_name)
       
    if ptg.find(toggle_name) is None:
        p = hou.ToggleParmTemplate (toggle_name, toggle_label, toggle_default)
        ptg.appendToFolder(folder, p)
        node.setParmTemplateGroup(ptg)
    else:
        node.parm(toggle_name).set(False)

def hide_cam_view_menu_on_selection():

    for cam in cameras_from_selection():
        append_toggle_hide(cam, 'Render', 'soho_viewport_menu', 'Show In Viewport Menu', False)
        append_toggle_hide(cam, 'Render', 'soho_renderview_menu', 'Show In Render View Menu', False)

hide_cam_view_menu_on_selection()
