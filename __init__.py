# Thanks to Secrop for the Shader Node code : https://github.com/Secrop/ShaderNodesExtra2.80
bl_info = {
    "name": "Wreckfest Modding Toolbox",
    "author": "Dummiesman, TheSpacebarRider, Mazay",
    "version": (0, 1, 0),
    "blender": (2, 83, 0),
    "location": "Tool Bar",
    "description": "A toolbox that help creating mods for the game Wreckfest",
    "warning": "Actually in development",
    "wiki_url": "https://github.com/ThomsGuillemot/wreckfest-toolbox/wiki",
    "support": 'COMMUNITY',
    "category": "3D View"
}


def reload_modules(name):
    import importlib

    from . import registration
    importlib.reload(registration)

    modules = []

    for entry in registration.CLASSES:
        path = entry[0].split('.')
        module = path.pop(-1)

        if(path, module) not in modules:
            modules.append((path, module))

    for path, module in modules:
        if path:
            impline = "from . %s import %s" % (".".join(path), module)
        else:
            impline = "from . import %s" % (module)

        print("Reloading %s" % (".".join([name] + path + [module])))

        exec(impline)
        importlib.reload(eval(module))


if "bpy" in locals():
    reload_modules(bl_info['name'])

import bpy
from . import registration
from . import preferences
from nodeitems_utils import NodeItem, register_node_categories, unregister_node_categories
from nodeitems_builtins import ShaderNodeCategory
import threading
import subprocess


def popen_and_call(on_exit, popen_args):
    """
    Runs the given args in a subprocess.Popen, and then calls the function
    on_exit when the subprocess completes.
    on_exit is a callable object, and popen_args is a list/tuple of args that
    would give to subprocess.Popen.
    """
    def run_in_thread(on_exit_event, popen_args_list):
        proc = subprocess.Popen(popen_args_list, shell=True)
        proc.wait()
        on_exit_event()
        return

    thread = threading.Thread(target=run_in_thread, args=(on_exit, popen_args))
    thread.start()
    # returns immediately after the thread starts
    return thread


def register():
    global classes

    classes = registration.register_classes(registration.CLASSES)
    bpy.types.WindowManager.WFTBPanel = bpy.props.PointerProperty(
        type=preferences.WreckfestPanelContext
    )
    registration.register_menus()
    # Register Wrapper Node
    newcatlist = [ShaderNodeCategory("SH_NEW_CUSTOM", "Wreckfest", items=[NodeItem("WreckfestWrapperNode"), ]), ]
    register_node_categories("CUSTOM_NODES", newcatlist)


def unregister():
    global classes

    unregister_node_categories("CUSTOM_NODES")

    registration.unregister_menus()

    registration.unregister_classes(classes)

    del bpy.types.WindowManager.WFTBPanel



