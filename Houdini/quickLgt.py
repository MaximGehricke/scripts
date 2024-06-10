#quickLgt
#quickly creates pre-configured arnold lights
#icon = OBJ_light

import hou

network = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
networkpath = network.pwd().path()

nodes = hou.selectedNodes()
light = hou.node(networkpath).createNode('arnold_light')

choice = hou.ui.displayMessage("",buttons=("skydome","quad","cancel"))

if choice == 0:
    print("set to skydome settings!")
    light.parm("ar_light_type").set(6)
    light.parm("ar_camera").set(0.0)
    light.setUserData("nodeshape", "circle")
    light.setColor(hou.Color((1.0,0.976,0.666)))
    light.setName("arnold_skydome",1)
    light.setSelected(1,1)
    
if choice == 1:
    print("set to quad settings!")
    light.parm("ar_light_type").set(3)
    light.parm("ar_exposure").set(10)
    light.setUserData("nodeshape", "slash")
    light.setColor(hou.Color((1.0,0.976,0.666)))
    light.setName("arnold_quad",1)
    light.setSelected(1,1)


