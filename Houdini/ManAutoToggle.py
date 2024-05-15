#ManAutoToggle
#toggles between manual and AutoUpdate mode
#icon = DOP_staticsolver
#hotkey = F11,F5

import hou
mode = hou.updateModeSetting().name()
if mode == 'AutoUpdate':
    hou.setUpdateMode(hou.updateMode.Manual)
if mode == 'Manual':
    hou.setUpdateMode(hou.updateMode.AutoUpdate)
