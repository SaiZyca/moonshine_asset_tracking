import bpy
from bpy.props import StringProperty, BoolProperty, IntProperty, CollectionProperty, BoolVectorProperty, PointerProperty, EnumProperty 
from bpy_extras.io_utils import ExportHelper, ImportHelper
import os, shutil, uuid, ntpath

class ASSET_TRACKING_OT_actions(bpy.types.Operator):
    bl_idname = "moonshine.asset_manager"
    bl_label = "Moonshine AssetManager Ops"
    bl_description = "Moonshine AssetManager Operators"

    button: StringProperty(default="") 

    def execute(self, context):
        button=self.button
        new_folder = bpy.path.abspath(context.scene.Moonshine_AssetTracking.image_folder)
        
        try:
            ## ObjectOperator
            if button == "find missing": self.find_missing(new_folder)
            elif button == "collect images": self.collect_images(new_folder)
            elif button == "absolute path": self.absolute_path()
            elif button == "relative path": self.relative_path()
            elif button == "fix map name": self.fix_map_name()
            else:
                self.report({'INFO'}, "%s Not defined !" % button)

        except Exception as e:
            self.report({'INFO'}, "Execute Error:%s" % (e) )

        return {"FINISHED"}

    def find_missing(self, new_folder):
        bpy.ops.file.find_missing_files(find_all=True, directory=new_folder)


    def collect_images(self, new_folder):
        images = bpy.data.images
        try:
            for image in images:
                image_path = bpy.path.abspath(image.filepath)
                if os.path.exists(image_path):
                    new_path = shutil.copy(image_path, new_folder)
                    # image.filepath = new_path
                    # self.report({'INFO'}, new_path )
                
        except Exception as e:
            self.report({'INFO'}, "Execute Error:%s" % (e) )

    def absolute_path(self):
        bpy.ops.file.make_paths_absolute()

    def relative_path(self):
        bpy.ops.file.make_paths_relative()

    def fix_map_name(self):
        images = bpy.data.images

        for image in images:
            image.name = ntpath.basename(image.filepath)

class ASSET_TRACKING_OT_collectTextures(bpy.types.Operator, ExportHelper):
    bl_idname = "asset_tracking.collect_textures"
    bl_label = "Collect Textures"
    bl_description = "collect textures used in scenes"

    filename_ext = ".*" 

    def execute(self, context):
        images = bpy.data.images
        new_folder = os.path.dirname(self.filepath)
        try:
            for image in images:
                image_path = bpy.path.abspath(image.filepath)
                if os.path.exists(image_path):
                    new_path = shutil.copy(image_path, new_folder)
                    # image.filepath = new_path
                    # self.report({'INFO'}, new_path )
                
        except Exception as e:
            self.report({'INFO'}, "Execute Error:%s" % (e) )

        return {"FINISHED"}

classes = (
    ASSET_TRACKING_OT_actions,
    ASSET_TRACKING_OT_collectTextures,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

        

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    

if __name__ == '__main__':
    register()