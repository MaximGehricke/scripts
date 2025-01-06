#change speed on v project
import hou

nodes = hou.selectedNodes()
parmsToAffect = ["speed1x","speed1y","speed2x","speed2y","speed3x","speed3y","speed4x","speed4y","speed","flow_speed_mult","flow_speed_mult2"]

input = str(hou.ui.readInput("expression pls")[1])

for node in nodes:
    for parm in node.parms():
        for name in parmsToAffect:
            if parm.name()==name:
                print(parm.name())
                parmVal = parm.rawValue()
                parm.setExpression(str(parmVal)+input)
