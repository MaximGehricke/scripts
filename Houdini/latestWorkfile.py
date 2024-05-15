#latestWorkfile
#loads the latest workfile from a selection. Meant to be customized manually for a show.




import hou, os

##########################################################
#ADD YOUR WORKFILES HERE:

#add it to option
options = ("s0080")
#...and create a variable of the same name containing the workfile path

s0080 = """/job/comms/dyson_n683_2006645/dn030/dn030_0080/work/fx/fx/houdini/workfile/dn030_0080_fx_default_v001.hip"""

##########################################################

#choose workfile:
choice = hou.ui.selectFromList(options,exclusive=True)
#choice = hou.ui.displayMessage(str(node),buttons=options) button options instead of list
choice = int(choice[0])

workfile = (eval(str(options[choice])))


#load the latest workfile:
file = workfile.split("/")[-1]
path = workfile.replace(file,"")

orig_version = file.split(".hip")[0].split("_")[-1]
basename = file.split(orig_version)[0]
filesInDir = [f for f in os.listdir(path) if os.path.isfile(path + f)]

latest = 1
for found in filesInDir:
    if(basename in found and ".hip" in found):
        ver = int(found.split(".hip")[0].split("_")[-1].replace("v",""))
        if(ver>latest): latest=ver

print("latest: ",latest)
version = "v"+str(latest).zfill(3)
file = file.replace(orig_version,version)

fileToLoad = path+file
print(fileToLoad)
hou.hipFile.load(fileToLoad)
