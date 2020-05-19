bl_info = {
    "name": "Node group tools",
    "author": "Andrew Stevenson",
    "version": (0, 1),
    "blender": (2, 80, 0),
    "location": "View3D > N-Panel",
    "description": "easily edit node group perameters",
    "category": "node",
}

import bpy
import nodeitems_utils 
from bpy.types import Panel
from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       EnumProperty,
                       PointerProperty,
                       )

def node_group_enum(self, context):
    enum_items = []
    node_groups = []
    group_tool = bpy.context.scene.group_tool
    nodes = bpy.data.materials[group_tool.material].node_tree.nodes

    for node in nodes:
        if node.type == 'GROUP':
            node_groups.append(node.name)

    for group in node_groups:
        enum_items.append((group,
                           group,
                           group,
                           ))
    
    return enum_items

def material_enum(self, context):
    enum_items = []
    material_slots = bpy.context.active_object.material_slots
    i = 0
    for material_slot in material_slots:
        if material_slot.material is not None:
            material_name = material_slot.material.name
            enum_items.append((material_name,
                            material_name,
                            material_name,
                            bpy.data.materials[material_name].preview.icon_id,
                            i
                            ))
            i+=1
    
    return enum_items

class NodeGroupSettings(bpy.types.PropertyGroup):
    
    material : EnumProperty(
            name = "",
            description = "material to display",
            items = material_enum,
            )

    node_group : EnumProperty(
            name = "",
            description = "node group to display",
            items = node_group_enum,
            )

    show_settings : BoolProperty(
        name = "show settings",
        description = "show settings",
        default = False,
    )

    edit_node_links : BoolProperty(
        name = "show node links",
        description = "show node links",
        default = False,
    )

    use_boxes : BoolProperty(
        name = "use boxes",
        description = "put inputs in a box",
        default = True,
    )

    align_inputs : BoolProperty(
        name = "align",
        description = "align inputs",
        default = False,
    )

def def_input_boxes(group_node,):
    categories = ["misc"]
    print(categories.count[box])
    for inputs in group_node.inputs:
        #has category
        if inputs.name.count("_") != 0:
            box, name = inputs.name.split("_")
            #add to categorys
            
            #if categories.count[box] != 0:
                #categories.append[box]
    
    print(categories)


class GROUP_PT_panel(Panel):
    """Creates a Panel in the Object properties window"""
    bl_space_type = "VIEW_3D"
    bl_context = "objectmode"
    bl_region_type = "UI"
    bl_label = "Node group tools"
    bl_category = "Tool"

    def draw(self, context): 
        group_tool = bpy.context.scene.group_tool
        layout = self.layout
        
        #check for materials
        if bpy.data.materials[group_tool.material] is not None:
            row = layout.row()
            row.scale_y = 1.4
            row.prop(group_tool, "material",)

            #check for node tree
            if bpy.data.materials[group_tool.material].node_tree is not None:
                node_groups = []
                nodes = bpy.data.materials[group_tool.material].node_tree.nodes

                #check for node groups
                for node in nodes:
                    if node.type == 'GROUP':
                        node_groups.append(node.name)
            
                if len(node_groups) is not 0:

                    node_tree = bpy.data.materials[group_tool.material].node_tree
                    group_node = node_tree.nodes[group_tool.node_group]
                    def_input_boxes(group_node)

                    col = layout.column(align = True)
                    row = col.row(align = True)
                    
                    row.scale_y = 1.2
                    row.scale_x = 1.13

                    row.prop(group_tool, "node_group", icon = "NODETREE")
                    row.prop(group_tool, "show_settings", text="", icon='PREFERENCES')

                    if group_tool.show_settings:
                        box = col.box()
                        col = box.column(align = True)
                        row = col.row()
                        row.prop(group_tool, "edit_node_links")
                        col.prop(group_tool, "use_boxes")
                        col.prop(group_tool, "align_inputs")

                    #draw inputs
                    value_inputs = [socket for socket in group_node.inputs if socket.enabled and not socket.is_linked and not socket.hide_value]
                    if value_inputs:
                            layout.label(text="Inputs:")
                            #use boxes or not
                            if group_tool.use_boxes:
                                box = layout.box()
                            else:
                                box = layout
                            #align or not
                            col = box.column(align = group_tool.align_inputs)
                            #draw type
                            if group_tool.edit_node_links:
                                for socket in range(len(value_inputs)):
                                    col.template_node_view(node_tree, group_node, group_node.inputs[socket])
                            else:
                                for socket in value_inputs:
                                    socket.draw(context, col, group_node, socket.name)


                else:
                    layout.label(text = "no node groups in this material")            
            else:
                layout.label(text = "no active node tree")
        else:
            layout.label(text = "no active material")
         


classes = (
    NodeGroupSettings,
    GROUP_PT_panel,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.group_tool = bpy.props.PointerProperty(type=NodeGroupSettings)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
        
if __name__ == "__main__":
    register()
    
