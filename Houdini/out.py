#OUT
#creates an output node, sets name, shape, color. toggles to null if it already exists
#icon = SOP_output

import hou

network = hou.ui.curDesktop().paneTabUnderCursor()
networkpath = network.pwd().path()
pos = network.cursorPosition()
name = "OUT_"+networkpath.split("/")[-1]

#find lowest selected node:
selectedNodes = hou.selectedNodes()
lastNode = "noNodeSelected29834787320~###"

lowestPos = 10000000000;
for node in selectedNodes:
    #check if OUT already exists, if so toggle to Null
    if name in node.name():
        if node.type().name()=="output":
            node.changeNodeType("null")
            exit()
        if node.type().name()=="null":
            node.changeNodeType("output")
            exit()
            
    position = node.position()[1]
    if position<lowestPos:
        lowestPos = position
        lastNode = node
        

out = hou.node(networkpath).createNode('output')
out.setPosition(pos)
out.setUserData("nodeshape", "null")
out.setColor(hou.Color((0.29,0.565,0.886)))
out.setName(name,1)
out.setSelected(1,1)

if lastNode!="noNodeSelected29834787320~###":
    out.setInput(0,lastNode)
    out.moveToGoodPosition()
