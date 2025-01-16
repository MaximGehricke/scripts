#makeRelative
#replaces absolute paths with relative ones
#icon = SOP_name
# hotkey = alt + r


import hou

nodes = hou.selectedNodes()
parmsToAffect = ["cache_path","cachepath","campath","cmp_camera","source","shop_materialpath","shop_materialpath1","shop_materialpath2","shop_materialpath3","shop_materialpath4","objpath1","objpath2","objpath3","objpath4","objpath5","objpath6","objpath7","objpath8","objpath9","objpath10","soppath","sop_path"]

for node in nodes:
    for parm in node.parms():
        for name in parmsToAffect:
            if parm.name()==name:
                print(parm.name())
                try:
                    #for all matching parms:
                    #if whole path except last is equal - replace whole thing with ../
                    #otherwise, go through bit by bit - if same, replace by ../
                    #if not same, leave                 
                    nodepath = node.path()
                    parmpath = parm.eval()
                    
                    n = nodepath.split("/")
                    n = [x for x in n if x]
                    p = parmpath.split("/")
                    p = [x for x in p if x]
                    pRel = list(p)
                
                    pathN=list(n[:-1])
                    pathP=list(p[:-1])
                    
                    relativepath = ""
    
                    if pathN[0]!="obj":
                        print('not supported in "'+pathN[0]+'"')
                        continue
                        
                    if pathP[0]=="..":
                        print('already relative!')
                        continue
                        
                        
                    for index, nElem in enumerate(pathN):
                        
                        additional = list()
                        try:
                            pElem = pathP[index]
                        except IndexError:
                            pElem = None
                        if pElem == nElem:
                           
                            pRel[index] = ".."
                        else:
                            additional.append("..")
                         
                        if additional:
                            pRel = additional + pRel
                        else:
                            pRel = [i for i in pRel if i != ".."]
                            pRel = [".."] + pRel
                            
                        
                        relativepath = ""
                        
                        for i,x in enumerate(pRel):
                            
                            relativepath += x
                            if i != len(pRel)-1:
                                relativepath += "/"
                        relativepath = relativepath
                    
                    
                    parm.set(relativepath)
                except:
                    pass
