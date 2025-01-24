#chef
#force cooks the selected networks
#icon = opdef:/labs::Sop/simple_baker::2.0?IconSVG

import hou

frame = (int(hou.frame()),int(hou.frame()))
selected_nodes = hou.selectedNodes()


for node in selected_nodes:
    print(node)
    node.cook(force=True,frame_range=(frame))
    for child in node.children():
        child.cook(force=True,frame_range=(frame))
        if child.type().category() == hou.objNodeTypeCategory():
            for childchild in child.children(): 
                childchild.cook(force=True,frame_range=(frame))
