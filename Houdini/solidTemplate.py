#solidTemplate
#toggles current viewer template mode between solid and ghosted wireframe
#icon = opdef:/labs::Sop/export_uv_wireframe?IconSVG

import hou

# Get a reference to the geometry viewer
pane = hou.ui.curDesktop().paneTabOfType(hou.paneTabType.SceneViewer)
# Get the display settings
settings = pane.curViewport().settings()
# Get the GeometryViewportDisplaySet for objects
tmplset = settings.displaySet(hou.displaySetType.TemplateModel)



# toggle display modes
if tmplset.shadedMode() == hou.glShadingType.Smooth:
    tmplset.setShadedMode(hou.glShadingType.Wire)
    tmplset.useGhostedLook(1)
else:
    tmplset.setShadedMode(hou.glShadingType.Smooth)
    tmplset.useGhostedLook(0)