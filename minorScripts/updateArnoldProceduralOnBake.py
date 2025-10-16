#update arnold procedural when sending .assbake to farm
node = hou.pwd()
print(str(node))
version = node.evalParm("cmp_version")
target = node.parm("spare_input0").evalAsNode()
if target:
    target.parm("cmp_template_version").set(version)
