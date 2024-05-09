import os
#load latest workfile for:
workfile = '/job/comms/dyson_n683_2006645/dn030/dn030_0060/work/fx/fx/houdini/workfile/dn030_0060_fx_default_v001.hip'

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
