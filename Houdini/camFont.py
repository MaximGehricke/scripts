#camFont
#places font in front of the camera
#icon = OBJ_camera

import hou

def getCurCam(camtypes=["cam","cm_abc_camera::1.0"]):
    #grabs the current camera based on (in order) selection, active viewport cam, or manual selection
    
    sel = hou.selectedNodes()[0] if hou.selectedNodes() else None
    sv = hou.ui.paneTabOfType(hou.paneTabType.SceneViewer)
    vp = sv.curViewport() if sv else None
    
    for camtype in camtypes:
        cam = sel if sel and sel.type().name() == camtype else None
        if not cam:
            cam = vp.camera() if vp else None
        if not cam:
            cam = hou.node(hou.ui.selectNode(initial_node=hou.node("obj/"),title="Choose Camera"))
        
        vp.setCamera(cam)
        return cam

def createFont():
    node = hou.node("/obj").createNode("geo", "font_geo")
    font = node.createNode("font")
    parent_pos = font.position()
    
    #align
    trf = node.createNode("xform","align")
    trf.parm("tx").setExpression("-bbox(0,D_XSIZE)/2", hou.exprLanguage.Hscript)
    trf.setInput(0, font)
    trf.setPosition((parent_pos[0], parent_pos[1] - 1))
    
    #material
    mat = node.createNode("material", "SHD_white")
    mat.parm("shop_materialpath1").set("/shop/white")
    mat.setInput(0, trf)
    mat.setPosition((parent_pos[0], parent_pos[1] - 2))
    
    #output
    out = node.createNode('output')
    out.setPosition((parent_pos[0], parent_pos[1] - 3))
    out.setUserData("nodeshape", "null")
    out.setColor(hou.Color((0.29,0.565,0.886)))
    out.setName(node.name()+"_OUT",1)
    out.setInput(0, mat)
    out.setDisplayFlag(1)
    out.setRenderFlag(1)
    
    font.setSelected(1)
    
    return font
    
def placeFont(font,cam,scale = 2):
    font = font.parent()
    font.setInput(0, cam)
    
    nearClip = cam.parm("near").eval()
    resx = cam.parm("resx").eval()
    resy = cam.parm("resy").eval()
    focal = cam.parm("focal").eval()
    aspect = cam.parm("aspect").eval()
        
    font.parmTuple("t").set(((nearClip/2)/(focal/50),(-nearClip/2)*resy/resx/(focal/50)/aspect, -nearClip*1.1))
    font.parmTuple("s").set((aspect,1,1))
    font.parm("scale").set((nearClip/2*scale/focal)*1.7/(resx/resy))
    parent_pos = cam.position()
    font.setPosition((parent_pos[0], parent_pos[1] - 1))
    font.setName(str(cam.name())+"_font", unique_name=True)
    
def createWhiteMaterial():
    #creates a flat white arnold or mantra shader in /shop/ (if shader named "white" doesn't exist yet)
    if not hou.node("/shop/white"):
        if hou.nodeType("Driver/arnold") is not None:
            vopnet = hou.node("/shop").createNode("arnold_vopnet","white")
            flat = vopnet.createNode("arnold::flat", "flat")
            out = hou.node(str(vopnet.path())+"/OUT_material")
            
            out.setInput(0, flat)
            parent_pos = out.position()
            flat.setPosition((parent_pos[0]-3, parent_pos[1]))
        else:
            vopnet = hou.node("/shop").createNode("v_constant","white")


cam = getCurCam()
font = createFont()
placeFont(font,cam)
createWhiteMaterial()
#hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor).setCurrentNode(font)
