#quickVEX
#quickly add wrangles with code used commonly
#icon = SOP_attribwrangle

import hou
import toolutils
import vexpressionmenu

#use selected wrangle or create new one:
wrangle = 0

nodes = hou.selectedNodes()
if nodes:
    for node in nodes:
        if "attribwrangle" in str(node.type()):
            if "attribwrangle" in node.name():
                wrangle = node
                break

if not wrangle:
    pane = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
    if pane is None:
       hou.ui.displayMessage(
               'Cannot create node: cannot find any network pane')
       sys.exit(0)
    print(str(pane.pwd()))
    wrangle = pane.pwd().createNode('attribwrangle')

    #connect to last selected node:
    selectedNodes = hou.selectedNodes()
    lastNode = "noNodeSelected29834787320~###"

    lowestPos = 10000000000;
    for node in selectedNodes:
        position = node.position()[1]
        if position<lowestPos:
            lowestPos = position
            lastNode = node

    if lastNode!="noNodeSelected29834787320~###":
        wrangle.setInput(0,lastNode)
    wrangle.moveToGoodPosition()


##########################################################
#ADD ALL THE QUICK VEX SCRIPTS HERE:

#add it to option
options = ("pcfilter","percentage","NaN","ramp","primUvDeform","packedRandomize","boxify","spherify","twirl")
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

rotate(x, PI*pow(rand(@primnum-666),0.5), r);
scale(x,s);
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

##########################################################

#choose quickVex preset:
choice = hou.ui.selectFromList(options,exclusive=True)
#choice = hou.ui.displayMessage(str(node),buttons=options) button options instead of list
choice = int(choice[0])

#set wrangle options
wrangle.setName(options[choice],True)
wrangle.parm("snippet").set(eval(str(options[choice])))
vexpressionmenu.createSpareParmsFromChCalls(wrangle, 'snippet')

wrangle.setDisplayFlag(1)
wrangle.setRenderFlag(1)
