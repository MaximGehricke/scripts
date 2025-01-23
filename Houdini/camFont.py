#camFont
#places font in front of the camera
#icon = OBJ_camera

import hou

def getCurCam():
    #grabs the current camera based on (in order) selection, active viewport cam, or manual selection
    
    sel = hou.selectedNodes()[0] if hou.selectedNodes() else None
    sv = hou.ui.paneTabOfType(hou.paneTabType.SceneViewer)
    vp = sv.curViewport() if sv else None
    
    cam = sel if sel and sel.type().name() == "cam" else None
    if not cam:
        cam = vp.camera() if vp else None
    if not cam:
        cam = hou.node(hou.ui.selectNode(initial_node=hou.node("obj/"),title="Choose Camera"))
    
    #debug hou.ui.displayMessage(str(cam.path()))
    vp.setCamera(cam)
    return cam

def createFont():
    node = hou.node("/obj").createNode("geo", "font_geo")
    font = node.createNode("font")
    mat = node.createNode("material", "flat_white")
    mat.parm("shop_materialpath1").set("/shop/white")
    mat.setInput(0, font)
    parent_pos = font.position()
    mat.setPosition((parent_pos[0], parent_pos[1] - 1))
    return font
    
def placeFont(font,cam):
    font = font.parent()
    font.setInput(0, cam)
    font.parmTuple("t").set((0.04, -0.025, -0.1))
    font.parmTuple("s").set((0.003, 0.003, 0.003))
    parent_pos = cam.position()
    font.setPosition((parent_pos[0], parent_pos[1] - 1))
    font.setName(str(cam.name())+"_font", unique_name=True)
    

cam = getCurCam()
font = createFont()
placeFont(font,cam)
hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor).setCurrentNode(font)
