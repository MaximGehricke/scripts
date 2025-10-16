#publishComment
#helps set a publishComment for your autocomp

import datetime

userDesc = "None"
animVer = None
cfxVer = None
layoutVer = None
astVer = None
grmVer = None

userDesc = hou.ui.readInput("What did you do? ")[1]

#get autocomp node
for c in hou.selectedNodes():
    print(c)
    if "autocomp" not in str(c.type()):
        p = c.input(0)
        while "autocomp" not in str(p.type()) and p.input(0):
            p = p.input(0)
        autocomp = p
    elif "autocomp" in str(c.type()):
        autocomp = c
    else:
        continue
       
    print("autocomp: "+str(autocomp))

    #get shot from autocomp
    shot = autocomp.parm("cmp_shot_override").eval()

    for node in hou.node("/obj/").children():
        n = node.name().lower()
        if "baby_asset" in n and "grey" not in n:
            definition = node.type().definition()
            if definition:
                full_name = definition.nodeTypeName()
                astVer = int(full_name.split('::')[-1])
        if "baby_groom" in n and "grey" not in n:
            definition = node.type().definition()
            if definition:
                full_name = definition.nodeTypeName()
                grmVer = int(full_name.split('::')[-1])
        if "baby" in n and "seqswitch" in str(node.type()).lower():
            for cache in hou.node("/obj/"+node.name()+"/Sequence_Caches/").children():
                if "cm_alembic" in str(cache.type()):
                    file = cache.parm("fileName").eval()
                    if shot in file:
                        print("fyck yeah")
                        if "cfx" in file:
                            cfxVer = cache.parm("cmp_template_version").eval()
                        if "anim" in file:
                            animVer = cache.parm("cmp_template_version").eval()
                        if "layout" in file:
                            layoutVer = cache.parm("cmp_template_version").eval()



    comment = f"""{userDesc}
    Asset OTL: v{astVer:03}
    Groom OTL: v{grmVer:03}
    """
    try:
        if(cfxVer):
            comment += f"Baby cache: CFX v{cfxVer:03}"
        elif(animVer):
            comment += f"Baby cache: ANIM v{animVer:03}"
        else:
            comment += f"Baby cache: LAYOUT v{layoutVer:03}"
    except:
        hou.ui.displayMessage("Could not find Baby CFX, ANIM or layout cache version!")
    
    autocomp.parm('output_annotation1').set(comment)

    #set node network view comment
    current_time = datetime.datetime.now().time()
    formatted_time = datetime.datetime.now().strftime("%d-%m %H:%M")
    autocomp.parm('cmp_node_label_description').set(f"{userDesc} ({formatted_time})")
    autocomp.parm('cmp_node_label_description').pressButton() #refresh callback pls
    autocomp.parm('cmp_node_label_output_toggle').set(0)
    autocomp.parm('cmp_node_label_output_toggle').pressButton()
