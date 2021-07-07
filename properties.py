import bpy
from bpy.props import StringProperty, BoolProperty, IntProperty, CollectionProperty, BoolVectorProperty, PointerProperty, EnumProperty 
from bpy.types import PropertyGroup

def update_state(self, context):
    for item in self.objects_list:
        if context.scene.objects.get(item.name):
            bl_object = context.scene.objects.get(item.name)
            bl_object.hide_viewport = self.hide_viewport
            bl_object.hide_select = self.hide_select
            bl_object.hide_render = self.hide_render
            bl_object.display_type = self.display_type

class AssetTracing_Properties(PropertyGroup):
    # property for AssetManager
    images_list_index: IntProperty(default=-1)
    image_column_name: BoolProperty(default= True)
    image_column_users: BoolProperty(default= False)
    image_column_size: BoolProperty(default= False)
    image_column_has_data: BoolProperty(default= False)
    image_column_file_format: BoolProperty(default= False)
    image_column_packed_file: BoolProperty(default= False)
    image_column_filepath: BoolProperty(default= True)
    image_folder: StringProperty(default="//", subtype="DIR_PATH")
    linked_list_index: IntProperty(default=-1)
    linked_file_folder: StringProperty(default="//", subtype="DIR_PATH")

classes = (
    AssetTracing_Properties,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.Moonshine_AssetTracking = bpy.props.PointerProperty(type=AssetTracing_Properties)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.Moonshine_AssetTracking

    
if __name__ == '__main__':
    register()
