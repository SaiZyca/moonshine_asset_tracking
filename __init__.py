# ##### BEGIN GPL LICENSE BLOCK #####
#
# This file is part of the Blender addon "3dsmax Style Tools".
#
# The addon "3dsmax Style Tools" is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation version 3 of the License or
# any later version.
#
# The addon "3dsmax Style Tools" is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with the addon. If not, see <http://www.gnu.org/licenses/>.
#
# ##### END GPL LICENSE BLOCK #####

import bpy
from . import ui, properties, operators, prefs


bl_info = {
    "name": "moonshine asset tracking",
    "author": "sai ling",
    "version": (1, 0, 3),
    "blender": (2, 90, 0),
    "location": "Properties > Scene",
    "description": "manage exterior files in blender.",
    "category": "Scene",
    "wiki_url": "",
}

classes = ()

def register():
    properties.register()
    operators.register()
    ui.register()
    prefs.register()

    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    properties.unregister()
    operators.unregister()
    ui.unregister()
    prefs.unregister()

    for cls in classes:
        bpy.utils.unregister_class(cls)
    

if __name__ == '__main__':
    register()
