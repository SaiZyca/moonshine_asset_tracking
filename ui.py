import os
import bpy


class ASSET_TRACKING_PT_Main(bpy.types.Panel):
    bl_label = "Asset Tracking"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    def draw(self, context):
        pass

class ASSET_TRACKARE_PT_globalTools(bpy.types.Panel):
    bl_label = "Global Tools"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_parent_id = "ASSET_TRACKING_PT_Main"

    def draw(self, context):
        data_prop = context.scene.Moonshine_AssetTracking
        layout = self.layout
        layout.use_property_decorate = False 
        box = layout.box()
        row = box.row(align=True)
        row.operator("file.find_missing_files", text = "Find Missing")
        row.operator("file.make_paths_absolute", text = "Absolute path")
        row.operator("file.make_paths_relative", text = "Relative path")
        row.operator("asset_tracking.fix_map_node", text = "Fix Map Name")
        box = layout.box()
        row = box.row(align=True)
        split = row.split(factor=0.25, align=True)
        split.operator("asset_tracking.collect_textures", text = "Collect images")
        split.prop(data_prop, "image_folder", text="")
        row = box.row(align=True)
        split = row.split(factor=0.25, align=True)
        split.prop(data_prop, "image_proxy", text="Make Proxy")
        split.prop(data_prop, "image_proxy_size", text="")
        

class ASSET_TRACKING_PT_textures(bpy.types.Panel):
    bl_label = "Image Manager"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_parent_id = "ASSET_TRACKING_PT_Main"

    def draw(self, context):
        data_prop = context.scene.Moonshine_AssetTracking
        layout = self.layout
        data = bpy.data
        row = layout.row(align=True)
        row.prop(data_prop, "image_column_name", text="Name", toggle=True)
        row.prop(data_prop, "image_column_filepath", text="Path", toggle=True)
        row.prop(data_prop, "image_column_users", text="Used", toggle=True)
        row.prop(data_prop, "image_column_size", text="Size", toggle=True)
        row.prop(data_prop, "image_column_has_data", text="Load", toggle=True)
        row.prop(data_prop, "image_column_file_format", text="Format", toggle=True)
        row.prop(data_prop, "image_column_packed_file", text="Packed", toggle=True)
        row = layout.row()
        row.template_list("ASSET_TRACKING_UL_ImageList", "", data, "images", data_prop, "images_list_index")

        
class ASSET_TRACKING_PT_LinkedManager(bpy.types.Panel):
    bl_label = "Linked File Manager"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_parent_id = "ASSET_TRACKING_PT_Main"

    def draw(self, context):
        data_prop = context.scene.Moonshine_AssetTracking
        layout = self.layout
        data = bpy.data
        row = layout.row()
        row.template_list("ASSET_TRACKING_UL_LinkedList", "", data, "libraries", data_prop, "linked_list_index")
        

class ASSET_TRACKING_UL_ImageList(bpy.types.UIList):
    
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        data_prop = context.scene.Moonshine_AssetTracking
        # item = context.scene.objects[item.name]
        file_icon = {True:"OUTLINER_OB_IMAGE", False:"LIBRARY_DATA_BROKEN"}
        packed_icon = {True:"PACKAGE", False:"UGLYPACKAGE"}
        # load_icon = {True:"FAKE_USER_ON", False:"FAKE_USER_OFF"}
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            row = layout.split(factor=0.3)
            if data_prop.image_column_name:
                abspath = bpy.path.abspath(item.filepath)
                row.prop(item, "name", text="", icon=file_icon[os.path.exists(abspath)], emboss=False)
            if data_prop.image_column_filepath:
                row.prop(item, "filepath", text="", emboss=False)
            if data_prop.image_column_users:
                row.label(text=str(item.users))
            if data_prop.image_column_size:
                row.label(text="%s x %s" % (item.size[0], item.size[1]))
            if data_prop.image_column_has_data:
                row.label(text=str(item.has_data))
            if data_prop.image_column_file_format:
                row.label(text=str(item.file_format))
            if data_prop.image_column_packed_file:
                row.label(text="", icon=packed_icon[item.packed_file is not None])

        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'

    def invoke(self, context, event):
        pass  

class ASSET_TRACKING_UL_LinkedList(bpy.types.UIList):
    
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        data_prop = context.scene.Moonshine_AssetTracking
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            abspath = bpy.path.abspath(item.filepath)
            file_icon = {True:"FILE", False:"LIBRARY_DATA_BROKEN"}
            row = layout.split(factor=0.3)
            row.label(text=item.name, icon=file_icon[os.path.exists(abspath)])
            row.prop(item, "filepath", text="", emboss=False)
        
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'    
            if data_prop.image_column_file_format:
                row.label(text=str(item.file_format))

classes = (
    ASSET_TRACKING_PT_Main,
    ASSET_TRACKARE_PT_globalTools,
    ASSET_TRACKING_PT_textures,
    ASSET_TRACKING_PT_LinkedManager,
    ASSET_TRACKING_UL_ImageList,
    ASSET_TRACKING_UL_LinkedList,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == '__main__':
    register()
