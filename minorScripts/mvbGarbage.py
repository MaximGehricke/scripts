#rename autocomp and merges DIRTY fuck script
print("fuck")
for ac in hou.selectedNodes():
    print(ac)
    n = ac.name()
    print(n)
    p = ac.input(0)
    while p.type().name() != "arnold" and p.input(0):
        p = p.input(0)
    shot = p.parm("cmp_shot_override").eval()
    print(shot)
    
    name = str(ac.name())
    print(name)
    name = name.replace("202_005_TAA_0010",shot)
    print(name)
    ac.setName(name,1)


#shotify autocomp

for ac in hou.selectedNodes():
    if "autocomp" in ac.type().name():
        p = ac.input(0)
        while p.type().name() != "arnold" and p.input(0):
            #print(p.type().name())
            p = p.input(0)
        
        shot = p.parm("cmp_shot_override").eval()
        seq = p.parm("cmp_seq_override").eval()
            
        ac.parm("cmp_seq_override").set(seq)
        ac.parm("cmp_shot_override").set(shot)
        
        comppath = "/job/comms/redacted/"+seq+"/"+shot+"/work/lighting/lighting/nuke/workfile/"+shot+"_lighting_autocomp_v001.nk"
        
        ac.parm("nuke_script_path").set(comppath)
        


#nuke set buildover mode to disable, set on_error to "nearest frame"
for n in nuke.selectedNodes():
    if 'buildover_fail_mode' in n.knobs():
        n['buildover_fail_mode'].setValue(1)
    if 'on_error' in n.knobs():
        n['on_error'].setValue(3)


#SL switch baby subdivs GEV
if "ipr" in output_name.lower():
    print("set baby subdivs to 1")
    hou.parm('/obj/char_redacted_asset/gev_iterations').set(1)
else:
    print("set baby subdivs to 3")
    hou.parm('/obj/char_redacted_asset/gev_iterations').set(3)
