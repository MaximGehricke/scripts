#OUT
#creates an output node, sets name, shape, color
#icon = SOP_output

import hou

network = hou.ui.curDesktop().paneTabUnderCursor()
networkpath = network.pwd().path()
pos = network.cursorPosition()

out = hou.node(networkpath).createNode('output')
out.setPosition(pos)
out.setUserData("nodeshape", "null")
out.setColor(hou.Color((0.29,0.565,0.886)))

out.setName("OUT_"+networkpath.split("/")[-1],1)

#connect to last selected node:
selectedNodes = hou.selectedNodes()
lastNode = "noNodeSelected29834787320~###"

lowestPos = 10000000000;
for node in selectedNodes:
    position = node.position()[1]
    if position<lowestPos:
        lowestPos = position
        lastNode = node
        
if lastNode!="noNodeSelected29834787320~###":
    out.setInput(0,lastNode)
    out.moveToGoodPosition()
