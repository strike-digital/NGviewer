bl_info = {
    "name": "NGviewer beta 1.1",
    "author": "Andrew Stevenson",
    "version": (1, 1),
    "blender": (2, 80, 0),
    "location": "View3D > N-Panel",
    "description": "easily edit node group perameters from the 3D view",
    "category": "Node",
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

#Feel free to change this but it would be great for me if you would consider buying the addon first ;)
is_trial = False

# class NGPreferences(bpy.types.AddonPreferences):
#     bl_idname = __name__

#     category : EnumProperty(
#         name = "Panel area:",
#         description = "area to display the addon",
#         items = (
#             ("Tool", "Tool", "Display addon in the Tool panel in the sidebar"),
#             ("NGviewer", "New panel", "Display addon in a new panel in the sidebar")
#             ),
#         default = "Tool")
        

#     def draw(self, context):
#         layout = self.layout
#         if is_trial:
#             draw_trial(layout)
#         row = layout.row()
#         row.label(text = "Panel location:")
#         row.prop(self, "category",expand = True)


def draw_trial(col):
    row = col.row(align=True)
    row.operator('wm.url_open',
                 text="",
                 icon='FUND',
                 emboss=False).url = "https://gumroad.com/l/qWuvv"
    row.alert = True
    row.label(text="Trial Version")

def node_group_enum(self, context):
    enum_items = []
    node_group_names = []
    node_group_labels = []
    ng_tool = bpy.context.scene.ng_tool
    nodes = bpy.data.materials[ng_tool.material].node_tree.nodes

    for node in nodes:
        if node.type == 'GROUP':
            node_group_names.append(node.name)
            node_group_labels.append(node.label)

    for group, label in zip(node_group_names, node_group_labels):
        if label == "":
            enum_items.append((group,
                            group,
                            group,
                            ))
        else:
            enum_items.append((group,
                            label,
                            group,
                            ))
    return enum_items

def material_enum(self, context):
    enum_items = []
    material_slots = bpy.context.active_object.material_slots
    ng_tool = bpy.context.scene.ng_tool
    i = 0
    
    for material_slot in material_slots:
        if ng_tool.show_non_group_materials:
            if material_slot.material is not None:
                material_name = material_slot.material.name
                enum_items.append((material_name,
                                material_name,
                                material_name,
                                bpy.data.materials[material_name].preview.icon_id,
                                i
                                ))
                i+=1
        else:
            nodes = material_slot.material.node_tree.nodes
            node_groups = []

            for node in nodes:
                if node.type == 'GROUP':
                    node_groups.append(node.name)

            if material_slot.material is not None and len(node_groups) != 0:
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

    category : EnumProperty(
        name = "Panel area:",
        description = "area to display the addon",
        items = (
            ("Tool", "Tool", "Display addon in the Tool panel in the sidebar"),
            ("NGviewer", "New panel", "Display addon in a new panel in the sidebar")
            ),
        default = "Tool")

    node_group : EnumProperty(
            name = "",
            description = "node group to display",
            items = node_group_enum,
            )

    #material settings
    show_material_settings : BoolProperty(
        name = "show material settings",
        description = "show material settings",
        default = False,
    )

    show_non_group_materials : BoolProperty(
        name = "show non node group materials",
        description = "show materials with no node groups in them",
        default = False,
    )

    grumpy : BoolProperty(
        name = "grumpy",
        description = "remove happiness from messages",
        default = False,
    )

    #group settings
    show_group_settings : BoolProperty(
        name = "show group settings",
        description = "show group settings",
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

# class NG_PT_node_panel(Panel):
#     """Creates a Panel in the node"""
#     bl_space_type = "VIEW_3D"
#     bl_idname = "ng.panel"
#     bl_region_type = "UI"
#     bl_label = "NGviewer"
#     bl_category = "Tool"

class NG_PT_panel(Panel):
    """Creates a Panel in the Tool panel"""
    bl_space_type = "VIEW_3D"
    bl_idname = "ng.panel"
    bl_region_type = "UI"
    bl_label = "NGviewer"
    bl_category = "Tool"
    # ng_tool = bpy.context.scene.ng_tool
    #  if ng_tool.category is "Tool":
    #     bl_category = "Tool"
    # else:
    #     bl_category = "NGviewer"

    def draw(self, context): 
        ng_tool = bpy.context.scene.ng_tool
        grumpy = ng_tool.grumpy
        layout = self.layout
        

        if grumpy:
            face = ""
        else:
            face = ": )"

        if is_trial:
            draw_trial(layout)

        try:
            
            #check for active object
            if bpy.context.active_object is not None:
                material_slots = bpy.context.active_object.material_slots

                #check for material slots
                if len(material_slots) != 0:

                    #check for materials
                    if bpy.data.materials[ng_tool.material] is not None and bpy.context.active_object.active_material is not None:
                        col = layout.column(align = True)
                        row = col.row(align = True)
                        row.scale_y = 1.2
                        row.scale_x = 1.13
                        row.prop(ng_tool, "material",)
                        row.prop(ng_tool, "show_material_settings", text="", icon='PREFERENCES')

                        #settings panel
                        if ng_tool.show_material_settings:
                            box = col.box()
                            boxcol = box.column(align = True)
                            boxcol.prop(ng_tool, "show_non_group_materials")
                            boxcol.prop(ng_tool, "grumpy")

                        col.separator()

                        #check for node tree
                        if bpy.data.materials[ng_tool.material].node_tree is not None:
                            node_groups = []
                            nodes = bpy.data.materials[ng_tool.material].node_tree.nodes

                            #check for node groups
                            for node in nodes:
                                if node.type == 'GROUP':
                                    node_groups.append(node.name)
                        
                            if len(node_groups) is not 0:

                                node_tree = bpy.data.materials[ng_tool.material].node_tree
                                group_node = node_tree.nodes[ng_tool.node_group]
                                #def_input_boxes(group_node)

                                
                                row = col.row(align = True)
                                
                                row.scale_y = 1.2
                                row.scale_x = 1.13

                                row.prop(ng_tool, "node_group", icon = "NODETREE")
                                row.prop(ng_tool, "show_group_settings", text="", icon='PREFERENCES')

                                #settings panel
                                if ng_tool.show_group_settings:
                                    box = col.box()
                                    boxcol = box.column(align = True)
                                    boxcol.prop(ng_tool, "edit_node_links")
                                    boxcol.prop(ng_tool, "use_boxes")
                                    boxcol.prop(ng_tool, "align_inputs")

                                #draw inputs
                                value_inputs = [socket for socket in group_node.inputs if socket.enabled and not socket.is_linked and not socket.hide_value]
                                if value_inputs:
                                        layout.label(text="Inputs:")
                                        #use boxes or not
                                        if ng_tool.use_boxes:
                                            box = layout.box()
                                        else:
                                            box = layout
                                        #align or not
                                        col = box.column(align = ng_tool.align_inputs)
                                        #draw type
                                        if ng_tool.edit_node_links:
                                            for socket in range(len(value_inputs)):
                                                col.template_node_view(node_tree, group_node, group_node.inputs[socket])
                                        else:
                                            for socket in value_inputs:
                                                socket.draw(context, col, group_node, socket.name)


                            else:
                                layout.label(text = "No node groups in this material " + face)            
                        else:
                            layout.label(text = "No active node tree " + face)
                    else:
                        layout.label(text = "No active material " + face)
                else:
                    layout.label(text = "No material slots " + face) 
            else:
                layout.label(text = "No object selected " + face) 
        except KeyError:
            layout.label(text = "Please select a material " + face)

classes = (
    NodeGroupSettings,
    NG_PT_panel,
    #NGPreferences,
    #NG_PT_node_panel,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.ng_tool = bpy.props.PointerProperty(type=NodeGroupSettings)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
        
if __name__ == "__main__":
    register()
    
