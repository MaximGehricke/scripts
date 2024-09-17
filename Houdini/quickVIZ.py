#quickVIZ
#quickly add a visualizer based on attribute name
#icon = SOP_visualize

import hou
import sys
import random
import math

scope = hou.viewportVisualizerCategory.Scene
viewport = hou.ui.paneTabOfType(hou.paneTabType.SceneViewer).selectedViewport()

"""
hou.viewportVisualizers.types():
viz_marker
viz_color
viz_generic
viz_volume
viz_tag
viz_constraints
viz_captureweight
"""

def getUserInput():
    input = hou.ui.readInput("attribute name pls",buttons=('Keep Existing','Destroy Existing','Cancel'),default_choice = 0, close_choice=2)
    if not input or input[0]==2:
        print("no input, exiting")
        sys.exit(0)
    else:
        return input
        
        
def destroyExistingViz():
    #destroy all existing
    existingViz = hou.viewportVisualizers.visualizers(scope)
    for visualizer in existingViz:
        visualizer.destroy()


def createViz(input):
    newViz = hou.viewportVisualizers.createVisualizer(hou.viewportVisualizers.types()[1],scope)
    newViz.setName(input+"_quickViz")
    newViz.setLabel(input)
    newViz.setParm("attrib",input)
    return newViz


def getCurrentNode():
    #get the current node, either the lowest selected or the one with display flag    

    #finds displayed node
    network = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
    curNode = hou.node(network.pwd().path()).displayNode()
    
    #finds the lowest of all selected nodes
    selectedNodes = hou.selectedNodes()
    if selectedNodes:   
        lowestNode = None
        lowestYPos = 10000000000;

        for node in selectedNodes:
            yPos = node.position()[1]
            if yPos<lowestYPos:
                lowestYPos = yPos
                lowestNode = node
        curNode=lowestNode

    return curNode


def getAttributeInfo(attribname, node):
    #returns info about an attribute on a node
    attribute = node.geometry().findPointAttrib(attribname)
    if not attribute:
        return None
    name = attribute.name()
    datatype = str(attribute.dataType()).split(".")[-1]
    size = attribute.size()
    min = 0
    max = 1
    if size==1:        
        ptArray = node.geometry().points()
        if len(ptArray)<100000000:
            for point in ptArray:
                av = point.attribValue(attribute)
                if av>max:
                    max = av
                elif av<min:
                    min = av    

    info = {
    "attribute" : name,
    "datatype" : datatype,
    "size" : size,
    "min" : math.floor(min),
    "max" : math.ceil(max)
    }  
    return info
    
def vizSetVectorColor(viz,info):
    #sets the color of the viz vectors based on name
    if info["attribute"]=="v":
        #yellow if its v
        viz.setParm("markercolorr",1)
        viz.setParm("markercolorg",1)
        viz.setParm("markercolorb",0)
        viz.setParm("markercolora",1)
    elif info["attribute"]=="N":
        #blue if its N
        viz.setParm("markercolorr",0)
        viz.setParm("markercolorg",0)
        viz.setParm("markercolorb",1)
        viz.setParm("markercolora",1)
    else:
        viz.setParm("markercolorr",random.random())
        viz.setParm("markercolorg",random.random())
        viz.setParm("markercolorb",random.random())
        viz.setParm("markercolora",1)


def customizeViz(viz, info): 
    #set type based on float or vector
    if info["size"]== 3:
        viz.setType(hou.viewportVisualizers.types()[0]) #viz_marker
        viz.setIsActive(1,viewport)
        viz.setParm("style",4) #set vector
        viz.setParm("arrowheads",1)#set arrow
        #set color
        vizSetVectorColor(viz,info)       
    elif info["size"] == 1:
        viz.setType(hou.viewportVisualizers.types()[1]) #viz_color
        viz.setIsActive(1,viewport)#set active
        viz.setParm("colortype",1) #set ramped attrib
        viz.setParm("rangespec",1) #set to manual range
        viz.setParm("minscalar",info["min"]) #set min 
        viz.setParm("maxscalar",info["max"]) #set max
        
        #set ramp to infrared        
        bases = [hou.rampBasis.Linear]
        keys = [0.0, 0.25, 0.5, 0.75, 1.0]
        values = [(0.2, 0.0, 1.0), (0.0, 0.85, 1.0), (0.0, 1.0, 0.1),(0.95, 1.0, 0.0), (1.0, 0.0, 0.0)]
        ramp = hou.Ramp(bases, keys, values)
        viz.setParm("colorramp",ramp)
   
    else:
        hou.ui.displayMessage("attribute type is not supported. Info: "+ str(info))
    return
        
def main():
        
    #get user input
    input = getUserInput()

    #gather info about attribute on current node...
    info = getAttributeInfo(input[1],getCurrentNode())
    if not info:
        hou.ui.displayMessage("Attribute does not exist on current node")
        exit()
    
    #destroy existing if chosen
    if input[0] == 1:
        destroyExistingViz()
    
    #create new viz
    viz = createViz(input[1])
      
    #customize visualizer based on attrib info
    customizeViz(viz, info)
    
main()
