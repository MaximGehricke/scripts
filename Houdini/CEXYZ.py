#CEXYZ
#sets pivot to $CEX $CEY $CEZ
#icon = SOP_xform

import hou

network = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
networkpath = network.pwd().path()
print(network,networkpath)
pos = network.cursorPosition()
name = "pivot_to_centroid"

#find lowest selected node:
selectedNodes = hou.selectedNodes()
lastNode = "noNodeSelected29834787320~###"

lowestPos = 10000000000;
for node in selectedNodes:
    #check if transf already exists, if so also move to orig
    if name in node.name():
        if node.type().name()=="xform":
            node.parm("tx").setExpression("-$CEX")
            node.parm("ty").setExpression("-$CEY")
            node.parm("tz").setExpression("-$CEZ")
            node.setName("move_to_origin")
            exit()
    position = node.position()[1]
    if position<lowestPos:
        lowestPos = position
        lastNode = node
        

transf = hou.node(networkpath).createNode('xform')
transf.setPosition(pos)
transf.setUserData("nodeshape", "circle")
transf.setColor(hou.Color((0.29,0.565,0.886)))
transf.setName(name,1)
transf.setSelected(1,1)
transf.parm("px").setExpression("$CEX")
transf.parm("py").setExpression("$CEY")
transf.parm("pz").setExpression("$CEZ")

if lastNode!="noNodeSelected29834787320~###":
    transf.setInput(0,lastNode)
    transf.moveToGoodPosition()
