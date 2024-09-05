#DEBUG
#renames selected nodes or current node to DEBUG___nodename
#icon = SOP_cache

import hou


nodes = hou.selectedNodes()

if nodes:
    for node in nodes:
        #freeze default timeshift to current frame:
        if "timeshift" in str(node) and len(str(node))<13:
            frameparm = node.parm('frame')
            if frameparm.rawValue()=="$F":
                print("froze timeshift at current frame")
                frameparm.deleteAllKeyframes()
                frameparm.set(hou.frame())
                node.setName("freeze___"+str(hou.frame()).split(".")[0]+"___",unique_name=True)
                
        node.setName("DEBUG___"+str(node),unique_name=True)
        node.setColor(hou.Color((1,0,0)))
else:
    pane = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
    if pane is None:
       hou.ui.displayMessage('Cannot create node: cannot find any network pane')
    
    node = pane.currentNode()
    node.setName("DEBUG___"+str(node),unique_name=True)
    node.setColor(hou.Color((1,0,0)))
