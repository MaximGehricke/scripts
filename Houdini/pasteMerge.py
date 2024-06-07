# pasteMerge
# paste nodes in clipboard as objmerges, in rop context as fetches
# icon = SOP_object_merge
# hotkey = alt + v

#this tool is based on a script I found online.

import hou

network = hou.ui.curDesktop().paneTabUnderCursor()
networkpath = network.pwd().path()
pos = network.cursorPosition()

clipboard = hou.ui.getTextFromClipboard()

n = 0

if clipboard:
    list = clipboard.split()
    for item in list:
    
        #paste an objectmerge if we're in a sop context - this could be more elegant
        try:
            if hou.node(item) != None:
                merge = hou.node(networkpath).createNode('object_merge','IN_'+item.split('/')[-1])
                merge.parm('objpath1').set(str(item))
                name = merge.name().replace("OUT_","")
                merge.setName(name,1)
                merge.setColor(hou.Color((0.29,0.565,0.886)))
                merge.setPosition(pos)
                merge.move([n*2,0])
                if n == 0:
                    merge.setSelected(True,True)
                else:
                    merge.setSelected(True,False)
                n = n + 1
        except:
            print("not a sop context")
        
        #paste a fetch if we're in a rop context - this could be more elegant
        try:
            if hou.node(item) != None:
                
                try:
                    #FS pipeline?
                    import commstd.houdini
                    merge = commstd.houdini.create_node('networkpath','fetch', 'fetch_'+item.split('/')[-1])
                except:
                    #Home computer!
                    merge = hou.node(networkpath).createNode('fetch','fetch_'+item.split('/')[-1])
                
                merge.parm('source').set(str(item))
                merge.setPosition(pos)
                merge.move([n*2,0])
                if n == 0:
                    merge.setSelected(True,True)
                else:
                    merge.setSelected(True,False)
                n = n + 1
        except:
            print("not a rop context")
