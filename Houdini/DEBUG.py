#DEBUG
#renames selected nodes or current node to DEBUG___nodename
#icon = SOP_cache

import hou


nodes = hou.selectedNodes()

if nodes:
    for node in nodes:
        node.setName("DEBUG___"+str(node))
        node.setColor(hou.Color((1,0,0)))
else:
    pane = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
    if pane is None:
       hou.ui.displayMessage('Cannot create node: cannot find any network pane')
    
    node = pane.currentNode()
    node.setName("DEBUG___"+str(node))
    node.setColor(hou.Color((1,0,0)))
