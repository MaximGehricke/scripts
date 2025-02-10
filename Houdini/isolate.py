#isolate
#connects selected node to OUT_material - and back!
#icon = SHOP_surface

import hou
import toolutils
import htoa


def isolateSelOrRestore():
    network = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
    networkpath = network.pwd().path()
    mat_out = hou.node(networkpath+"/OUT_material")
    
    #try connect selected node to OUT or reconnect previously connected
    try:
        if hou.session.maximsCurrentMatNode:
            mat_out.setInput(0,hou.session.maximsCurrentMatNode)
            hou.session.maximsCurrentMatNode = None
        else:
            if not hou.selectedNodes():
                print("nothing selected")
                return
            hou.session.maximsCurrentMatNode = mat_out.input(0)
            sel = hou.selectedNodes()[0]
            mat_out.setInput(0,sel)
    except:
            hou.session.maximsCurrentMatNode = mat_out.input(0)
            sel = hou.selectedNodes()[0]
            mat_out.setInput(0,sel)

isolateSelOrRestore()
            
