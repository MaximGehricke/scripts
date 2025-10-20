ctx = next(tab for tab in hou.ui.currentPaneTabs() if isinstance(tab, hou.NetworkEditor) and tab.isCurrentTab()).pwd()
