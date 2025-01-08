#bypassDebug
#bypasses nodes with "DEBUG" in the name
import hou

def search_debug_nodes():
    # List of specific paths to search for "DEBUG" nodes
    search_paths = ['/obj/fx_balefire','/obj/fx_channeling']
    
    curPath = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor).pwd().path()
    search_path.append(curPath)

    
    found_paths = []

    
    for path in search_paths:
    
        parent_node = hou.node(path)
                
        if parent_node:
            # Iterate through all child nodes of the parent node
            for node in parent_node.children():
                # Check if "DEBUG" is in the node's name
                if "DEBUG" in node.name():
                    node.bypass(1)                       
                    # If found, append the path to the list
                    found_paths.append(node.path())
    
        
        # Display a message popup with the found paths
    if found_paths:
        message = "Bypassed DEBUG nodes at the following paths:\n" + "\n".join(found_paths)
        hou.ui.displayMessage(message, title="DEBUG Nodes Found", severity=hou.severityType.Message)

# Call the function when the shelf tool is pressed
search_debug_nodes()
