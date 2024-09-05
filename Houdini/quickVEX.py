#quickVEX
#quickly add wrangles with commonly used code
#icon = SOP_attribwrangle

import hou
import toolutils
import vexpressionmenu


def findLowestSelNode():
    #finds the lowest of all selected nodes
    selectedNodes = hou.selectedNodes()
    lowestNode = None
    
    if selectedNodes:    
        lowestYPos = 10000000000;

        for node in selectedNodes:
            yPos = node.position()[1]
            if yPos<lowestYPos:
                lowestYPos = yPos
                lowestNode = node
    return lowestNode


def placeNode(node):
        #node.setCurrent(1, 1)
        networkEditor = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
        screenBounds = networkEditor.visibleBounds()
        screenCenter = screenBounds.center()
        node.move(screenCenter)
        #sceneViewer = hou.ui.paneTabOfType(hou.paneTabType.SceneViewer)
        #sceneViewer.enterCurrentNodeState()
        lowestNode = findLowestSelNode()
        if lowestNode:
            node.setPosition(lowestNode.position())
            node.move(hou.Vector2(0.0,-1.0))
        
        
def wrangleCreate():
    #use selected wrangle or create new one:
    newWrangle = 0
    nodes = hou.selectedNodes()
    if nodes:
        for node in nodes:
            if "attribwrangle" in str(node.type()):
                if "attribwrangle" in node.name():
                    wrangle = node
                    break
    if not newWrangle:
        pane = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
        
        if pane is None:
           hou.ui.displayMessage(
                   'Cannot create node: cannot find any network pane')
           sys.exit(0)

        wrangle = pane.pwd().createNode('attribwrangle')
    return wrangle
        
   
def connectNode(node):
    #connect to lowest of selected nodes:
    lowestNode = findLowestSelNode()
    if lowestNode:
        if lowestNode.outputConnections():
            output = lowestNode.outputs()[0]
            output.setInput(0,node)
        
        node.setInput(0,lowestNode)
   
   
def main():

    ##########################################################
    #ADD ALL THE QUICK VEX SCRIPTS HERE:
    
    #add it to option
    options = ("pcfilter","percentage","NaN","ramp","primUvDeform","packedRandomize","boxify","spherify","twirl","masklerp")
    #...and create a variable of the same name containing the VEX code
    
    pcfilter = '''//pcfilter
    float radius = chf("radius");
    int maxPts = chi("maxPts");
    int handle = pcopen(0,"P",@P,radius,maxPts);
    vector p1 = pcfilter(handle,"P");
    @P = p1;
    
    '''
    packedRandomize = '''//randomize rotation and scale of packed prims
    
    matrix3 x = primintrinsic(0,'transform',i@primnum);
    
    vector r = sample_direction_uniform(rand(@primnum));
    
    float scale = fit01(rand(i@primnum),chf("min"),chf("max"));
    vector s = set(scale, scale, scale);
    
    if(chi("rotate")) rotate(x, PI*pow(rand(@primnum-666),0.5), r);
    if(chi("scale")) scale(x,s);
    setprimintrinsic(0,'transform',i@primnum,x);'''
    
    twirl = '''float a = chf('angle') * length(@P * {1, 0, 1});
    float u = atan2(@P.x, @P.z);
    float r = length(@P * {1, 0, 1});
    @P = set(sin(u-a), @P.y, cos(u-a)) * set(r,1,r);'''
    
    boxify = '''vector centroid = getbbox_center(0);
    vector size = getbbox_size(0);
    size = max(size); // Largest component
    @P -= centroid;
    @P *= (1.0/size);
    @P = lerp(@P, @P+clamp(normalize(@P)*1.75,vector(-1),vector(1)) * (1.0-length(max(abs(@P)))), chf('blend'));
    @P *= size;
    @P += centroid;'''
    
    spherify = '''vector centroid = getbbox_center(0);
    vector size = getbbox_size(0);
    size = min(size); // Largest component
    @P -= centroid;
    @P *= (1.0/size);
    @P = lerp(@P, normalize(@P), chf('blend'));
    @P *= size;
    @P += centroid;'''
    
    percentage = '''if(rand(@ptnum)>chf("keep"))removepoint(0,@ptnum);
    
    '''
    
    
    NaN = '''//fix NaNs wrangle
    string attribs[] = split(chs("attributes")," ");
    
    foreach(int i; string name; attribs){
        int size = pointattribsize(0,name);
    
        if(size==1){
            if(isnan(pointattrib(0,name,@ptnum,0))){
                setpointattrib(0,name,@ptnum,0);
                }
        }
        if(size==3){
            if(isnan(pointattrib(0,name,@ptnum,0))){
                setpointattrib(0,name,@ptnum,{0,0,0});
                }
        }
    }
    '''
    ramp = '''v@Cd = vector(chramp("viz", @attrib));
    '''
    
    primUvDeform = '''int posprim;
    vector parm_uv;
    float dist = xyzdist(1,@P,posprim,parm_uv);
    @P = primuv(2,"P",posprim,parm_uv);
    '''
    
    minSpeed = '''if(length(v@v)<chf("minSpeed"))removepoint(0,@ptnum);'''
    
    masklerp = '''v@P=lerp(v@P,v@opinput1_P,@mask*chf("lerp"));'''
    
    ##########################################################
    
    #choose quickVex preset:
    choice = hou.ui.selectFromList(options,exclusive=True,clear_on_cancel=True)
    if choice:
        choice = int(choice[0])
    else:
        exit()
    
    #make, place and connect node, create parameters
    wrangle = wrangleCreate()
    placeNode(wrangle)
    connectNode(wrangle)
            
    #set wrangle options
    wrangle.setName(options[choice],True)
    wrangle.parm("snippet").set(eval(str(options[choice])))
    vexpressionmenu.createSpareParmsFromChCalls(wrangle, 'snippet')
    
    wrangle.setDisplayFlag(1)
    wrangle.setRenderFlag(1)
    return wrangle

main()
