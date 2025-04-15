# splitGrp
# Splits geometry based on multiple primitive groups
# icon = SOP_split
# Written by HoudiniZone

import os
import hou

# Ensure a node is selected
if len(hou.selectedNodes()) == 0:
    hou.ui.displayMessage("No Nodes Selected")
else:
    node = hou.selectedNodes()[0]
    geo = node.geometry()
    full_path = os.path.dirname(node.path())
    pos = node.position()
    groups = geo.primGroups()

    x_offset = -3
    for group in groups:
        x_offset += 3
        name = group.name()
        
        # Create blast node
        blast_node = hou.node(full_path).createNode("blast", f"isolate_{name}")
        blast_node.setFirstInput(node)
        blast_node.setPosition([pos[0] + x_offset, pos[1] - 2])
        blast_node.parm("group").set(name)
        blast_node.parm("negate").set(1)
        
        # Create output null
        output = hou.node(full_path).createNode("null", f"OUT_{name}")
        output.setInput(0, blast_node)
        output.setPosition([pos[0] + x_offset, pos[1] - 3])
        output.setColor(hou.Color((0.4, 0.4, 0.4)))
