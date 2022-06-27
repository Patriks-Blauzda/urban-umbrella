from gltflib import (GLTF, GLTFModel, GLBResource)
import gltflib


class model:
    relativezero = 0
    
    
    def __init__(self, gltftemplate = GLTF(model=GLTFModel())):
        self.gltf = gltftemplate
        
        
    def set_empty(self):
        self.gltf.model.asset = gltflib.Asset(generator="Khronos glTF Blender I/O v3.2.40", version="2.0")
        
        self.gltf.model.scene = 0
        self.gltf.model.scenes = []
        
        self.gltf.model.nodes = []
        self.gltf.model.materials = []
        self.gltf.model.meshes = []
        self.gltf.model.accessors = []
        
        self.gltf.model.bufferViews = []
        self.gltf.model.buffers = [gltflib.Buffer(byteLength=0)]
        
        self.gltf.resources = [gltflib.GLBResource(data=None)]
    
    
    def append_buffer(self, *buffervalues):
        for bytelength in buffervalues:
            self.gltf.model.buffers[0].byteLength += bytelength



exportable = model()
exportable.set_empty()

thing = model(GLTF.load('file1.glb'))
thing2 = model(GLTF.load('file2.glb'))


# Buffer
exportable.append_buffer(
    thing.gltf.model.buffers[0].byteLength, thing2.gltf.model.buffers[0].byteLength
)


# Buffer views
exportable.gltf.model.bufferViews.extend(thing.gltf.model.bufferViews)
exportable.gltf.model.bufferViews.extend(thing2.gltf.model.bufferViews)


# Accessors
exportable.gltf.model.accessors.extend(thing.gltf.model.accessors)

thing2.currentzero = len(exportable.gltf.model.accessors)
for accessor in thing2.gltf.model.accessors:
   accessor.bufferView += thing2.currentzero


for mesh in thing2.gltf.model.meshes:
    for primitive in mesh.primitives:
        primitive.attributes.POSITION += thing2.currentzero
        primitive.attributes.NORMAL += thing2.currentzero
        primitive.attributes.TEXCOORD_0 += thing2.currentzero
    
        primitive.indices += thing2.currentzero
   
   
exportable.gltf.model.accessors.extend(thing2.gltf.model.accessors)


# Materials
if thing.gltf.model.materials is not None:
    exportable.gltf.model.materials.extend(thing.gltf.model.materials)

if thing2.gltf.model.materials is not None:
    exportable.gltf.model.materials.extend(thing2.gltf.model.materials)


# Meshes
exportable.gltf.model.meshes.extend(thing.gltf.model.meshes)

thing2.currentzero = len(exportable.gltf.model.meshes)

# for mesh in thing2.gltf.model.meshes:
    # for primitive in mesh.primitives:
        # primitive.attributes.TEXCOORD_0 += thing2.currentzero

exportable.gltf.model.meshes.extend(thing2.gltf.model.meshes)


# Nodes
exportable.gltf.model.nodes.extend(thing.gltf.model.nodes)

for x in thing2.gltf.model.nodes:
    x.mesh += thing2.currentzero

exportable.gltf.model.nodes.extend(thing2.gltf.model.nodes)


# Scenes
exportable.gltf.model.scenes.extend(thing.gltf.model.scenes)

for scene in thing2.gltf.model.scenes:
    for x in range(len(scene.nodes)):
        scene.nodes[x] += thing2.currentzero
        
    exportable.gltf.model.scenes[0].nodes.extend(scene.nodes)
   

# Binary
exportable.gltf.resources[0].data = (
    thing.gltf.resources[0].data + thing2.gltf.resources[0].data
)

exportable.gltf.export('exportedmodel.glb')