#shotify autocomp
import os

for ac in hou.selectedNodes():
    if "autocomp" in ac.type().name():
        p = ac.input(0)
        while p.type().name() != "arnold" and p.input(0):
            #print(p.type().name())
            p = p.input(0)
        
        shot = p.parm("cmp_shot_override").eval()
        seq = p.parm("cmp_seq_override").eval()
        f1 = p.parm("cmp_f1").eval()
        f2 = p.parm("cmp_f2").eval()
            
        ac.parm("cmp_seq_override").set(seq)
        ac.parm("cmp_shot_override").set(shot)
        ac.parm("cmp_f1").deleteAllKeyframes()
        ac.parm("cmp_f1").set(f1)
        ac.parm("cmp_f2").deleteAllKeyframes()
        ac.parm("cmp_f2").set(f2)
        
        #o = original
        o = ac.parm("nuke_script_path").eval().split("/")
        print(o)
        comppath = "/"+o[0]+"/"+o[1]+"/"+o[2]+"/"+o[3]+"/"+seq+"/"+shot+"/"+o[6]+"/"+o[7]+"/"+o[8]+"/"+o[9]+"/"+o[10]+"/"+shot+"_fx_autocomp_v001.nk"
        #/job/comms/emirates_sport_2025_2007042/rg020/rg020_0010/work/fx/fx/nuke/workfile/rg020_0010_fx_autocomp_v009.nk
        ac.parm("nuke_script_path").set(comppath.replace("//","/"))
        
        
        

        
def patternmatch(src, pattern):
    #write this. regex? easier way?
    
    
def findNearestArnoldRopInInputChain():
    p = ac.input(0)
    while p.type().name() != "arnold" and p.input(0):
        p = p.input(0)
    return p
    
    
    
    
#toggle ignoremissingtextures
import hou

# Get the selected node
sel = hou.selectedNodes()
if not sel:
    raise hou.Error("No node selected.")
node = sel[0]

# Iterate through all children of type "arnold::image"
for child in node.children():
    if child.type().name() == "arnold::image":
        parm = child.parm("ignore_missing_textures")
        if parm:
            parm.set(1)
