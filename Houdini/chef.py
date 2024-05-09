#chef
#force cooks the selected networks
#icon = opdef:/labs::Sop/simple_baker::2.0?IconSVG

import hou

root = hou.node("/obj/")
frame = (int(hou.frame()),int(hou.frame()))
selected_nodes = hou.selectedNodes()


for node in selected_nodes:
    print(node)
    node.cook(force=True,frame_range=(frame))
