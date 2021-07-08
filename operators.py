import bpy
from bpy.props import StringProperty, BoolProperty, IntProperty, CollectionProperty, BoolVectorProperty, PointerProperty, EnumProperty 
from bpy_extras.io_utils import ExportHelper, ImportHelper
import os, shutil, uuid, ntpath

class ASSET_TRACKING_OT_fixMapNodeName(bpy.types.Operator):
    bl_idname = "asset_tracking.fix_map_node"
    bl_label = "Fix Map Node"
    bl_description = "fix map node name after import"

    def execute(self, context):
        images = bpy.data.images

        for image in images:
            image.name = ntpath.basename(image.filepath)

        return {"FINISHED"}

class ASSET_TRACKING_OT_collectTextures(bpy.types.Operator):
    bl_idname = "asset_tracking.collect_textures"
    bl_label = "Collect Textures"
    bl_description = "collect textures used in scenes"

    def execute(self, context):
        data_prop = context.scene.Moonshine_AssetTracking
        new_folder = bpy.path.abspath(data_prop.image_folder)

        if data_prop.image_proxy:
            sub_folder =  data_prop.image_proxy_size + "%/"
            ratio = int(data_prop.image_proxy_size)/100
            new_folder = new_folder + sub_folder 
            copy_image(new_folder)
            scale_image(ratio)
        else:
            change_3dview_shade()
            # self.copy_image(new_folder)

        return {"FINISHED"}

def scale_image(ratio):
    message = "Success"
    images = bpy.data.images
    try:
        for image in images:
            image_path = bpy.path.abspath(image.filepath)
            if os.path.exists(image_path):
                image.scale(image.size[0]*ratio, image.size[1]*ratio)
                image.save()
            
    except Exception as e:
        message = "Execute Error:%s" % (e)

    return message


def copy_image(new_folder):
    message = "Success"

    if os.path.exists(new_folder) is False:
        os.mkdir(new_folder)

    images = bpy.data.images
    try:
        for image in images:
            image_path = bpy.path.abspath(image.filepath)
            if os.path.exists(image_path):
                new_path = shutil.copy(image_path, new_folder)
                image.filepath = new_path
            
    except Exception as e:
        message = "Execute Error:%s" % (e)
    
    return message


def change_3dview_shade(shading_mode='SOLID'):
    screens = bpy.context.workspace.screens
    view_3ds = []
    for screen in screens:
        [view_3ds.append(area) for area in screen.areas if area.type == 'VIEW_3D']

    for view in view_3ds:
        view.spaces[0].shading.type = shading_mode



classes = (
    ASSET_TRACKING_OT_collectTextures,
    ASSET_TRACKING_OT_fixMapNodeName,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

        

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    

if __name__ == '__main__':
    register()
