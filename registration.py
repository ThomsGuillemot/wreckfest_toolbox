import bpy
from bpy.utils import register_class, unregister_class

CLASSES = [
    ("preferences", ["WreckfestToolboxAddonPreference", "WreckfestPanelContext"]),
    ("utils.export_bgo", ["WFTB_OP_export_bgo_with_dialog", "WFTB_OP_export_bgo"]),
    ("utils.material_node", ["WreckfestWrapperNode", "WreckfestGeneralPBRNode"]),
    ("operators.wreckfest_properties_operators", ["WreckfestCustomDataGroup", "WFTB_OT_toggle_wreckfest_custom_data"]),
    ("operators.wreckfest_physical_material_operator", ["WFTB_OT_set_physical_material", ]),
    ("operators.wreckfest_custom_parts_operators", [
        "WFTB_OT_set_custom_part",
        "WFTB_OT_swith_custom_part_visibility"]
     ),
    ("ui.menus", ["WFTB_PT_wreckfest_toolbox_panel",
                  "WFTB_PT_wreckfest_material_panel",
                  "WFTB_MT_object_context_menu"])
]


def register_classes(classlists, debug=False):
    classes = []

    for fr, imps in classlists:
        impline = "from .%s import %s" % (fr, ", ".join([i for i in imps]))
        classline = "classes.extend([%s])" % (", ".join([i for i in imps]))

        exec(impline)
        exec(classline)

    for c in classes:
        if debug:
            print("REGISTERING", c)

        register_class(c)

    return classes


def unregister_classes(classes, debug=False):
    for c in classes:
        if debug:
            print("UN-REGISTERING", c)

        unregister_class(c)


def register_menus():
    bpy.types.VIEW3D_MT_object_context_menu.append(object_context_menu)


def unregister_menus():
    bpy.types.VIEW3D_MT_object_context_menu.remove(object_context_menu)


def object_context_menu(self, context):
    self.layout.separator()
    self.layout.menu("WFTB_MT_object_context_menu")
