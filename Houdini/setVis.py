#setVis
#sets -Use Visibility- to 0 on the alembics inside selected ObjNodes
#icon = SOP_visibility

times = 0
parents = hou.selectedNodes()
for parent in parents:
    abc = parent.children()[0]
    print(abc.path)
    abc.setParms({"usevisibility": 0})
    times += 1

hou.ui.displayMessage("visibility set for "+str(times)+" alembics!")
