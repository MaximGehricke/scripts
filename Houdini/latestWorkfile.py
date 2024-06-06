#latestWorkfile
#loads the latest workfile from a selection. Meant to be customized manually for a show.
#icon = SOP_file

import hou, os

##########################################################
#ADD YOUR WORKFILES HERE:

#add it to option
options = ("copy current .hip path","cable","torch")
#...and create a variable of the same name containing the workfile path

filename = """/path/to/file/filename"""

##########################################################

#choose workfile:
choice = hou.ui.selectFromList(options,exclusive=True,clear_on_cancel=True)

#if first option is selected, copy to clipboard
if choice[0]==0:
    import sys
    if sys.platform.startswith('win'):
        # Code for Windows
        print("Windows: copying .hip path to clipboard")
        import win32clipboard
        text = hou.hipFile.path()
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_UNICODETEXT, text)
        win32clipboard.CloseClipboard()
    
    elif sys.platform.startswith('linux'):
        # Code for Linux
        print("Linux: copying .hip path to clipboard")
        import subprocess
        text = hou.hipFile.path()
        p2 = subprocess.Popen(['xclip', '-selection', 'clipboard', '-i'], stdin=subprocess.PIPE)
        p2.communicate(input=text.encode())
    else:
        # Code for other platforms
        print("Running on a platform other than Windows or Linux! Did not copy .hip path")

    exit()


try:
    choice = int(choice[0])
except:
    print("latestWorkfile -- improper selection!")
    exit()
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
hou.hipFile.load(fileToLoad,suppress_save_prompt=True)
