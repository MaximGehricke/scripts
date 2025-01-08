#addScripts
#automatically adds all mgh scripts to the shelf
#icon = NETWORKS_top

import hou
import os

# Get the dir of current script
#thisDir = os.path.dirname(os.path.abspath(__file__))
#scripts_dir = thisDir+"/scripts"

# Path to the directory containing your Python scripts
scripts_dir = "/net/homes/mgehrick/personalPrefs/scripts"

# Name of the target shelf
shelf_name = "mgh"

# Ensure the shelf exists, or create it
shelf = hou.shelves.shelves().get(shelf_name)
if not shelf:
    shelf = hou.shelves.newShelf(
        name=shelf_name,
        label=shelf_name)

# Get the current tools in the shelf (if any)
existing_tools = list(shelf.tools())

# Iterate over all Python scripts in the directory
for script_file in os.listdir(scripts_dir):
    if script_file.endswith(".py"):  # Only consider Python files
        script_path = os.path.join(scripts_dir, script_file)

        # Read the Python script content
        with open(script_path, "r") as file:
            script_content = file.read()

        # Extract tool name from the file
        tool_name = script_content.splitlines()[0].replace(" ","").replace("#","").replace("\n","")
        icon =  script_content.splitlines()[2].replace(" ","").replace("#","").replace("\n","").replace("icon","").replace("=","")
        
        
        # Create a new tool
        tool = hou.shelves.newTool(
            name=tool_name,
            label=tool_name,
            script=script_content,
            icon= icon
        )

        # Add the tool to the list of existing tools
        existing_tools.append(tool)

# Update the shelf with the new list of tools
shelf.setTools(existing_tools)

hou.ui.displayMessage(f"Shelf tools added to {shelf_name}!")
