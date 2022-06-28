from gltflib import (GLTF, GLTFModel, GLBResource)
import gltflib


class model:
    currentzero = 0
    
    
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
        self.gltf.model.buffers = [gltflib.Buffer(uri=None, byteLength=0)]
        
        self.gltf.resources = [gltflib.GLBResource(data=bytes())]



exportable = model()
exportable.set_empty()

# GLB
thing = model(GLTF.load('file1.glb'))
thing2 = model(GLTF.load('file2.glb'))

# GLTF
thing3 = model(GLTF.load('file3.gltf'))

# Embedded GLTF
# thing4 = model(GLTF.load('file4.gltf'))


filearray = [thing, thing2, thing3]

for file in filearray:
    # Buffer and binary
    for buffer in file.gltf.model.buffers:
        exportable.gltf.model.buffers[0].byteLength += buffer.byteLength
            
        if (buffer.uri != None) and ['.bin' in buffer.uri]:
            with open(buffer.uri, 'rb') as bin:
                bytes = bin.read()
                exportable.gltf.resources[0].data += bytes
        else:
            exportable.gltf.resources[0].data += file.gltf.resources[0].data
    
    
    # Buffer views
    exportable.gltf.model.bufferViews.extend(file.gltf.model.bufferViews)
    
    for i in range(1, len(exportable.gltf.model.bufferViews)):
        prior = exportable.gltf.model.bufferViews[i - 1]
        exportable.gltf.model.bufferViews[i].byteOffset = (
            prior.byteLength + prior.byteOffset
        )

    # Accessors
    file.currentzero = len(exportable.gltf.model.accessors)
    for accessor in file.gltf.model.accessors:
       accessor.bufferView += file.currentzero


    for mesh in file.gltf.model.meshes:
        for primitive in mesh.primitives:
            primitive.attributes.POSITION += file.currentzero
            primitive.attributes.NORMAL += file.currentzero
            primitive.attributes.TEXCOORD_0 += file.currentzero
        
            primitive.indices += file.currentzero
       
       
    exportable.gltf.model.accessors.extend(file.gltf.model.accessors)


    # Materials    
    if file.gltf.model.materials is not None:
        file.currentzero = len(exportable.gltf.model.materials)
        
        for mesh in file.gltf.model.meshes:
            for primitive in mesh.primitives:
                if primitive.material != None:
                    primitive.material += file.currentzero
        
        exportable.gltf.model.materials.extend(file.gltf.model.materials)


    # Meshes
    file.currentzero = len(exportable.gltf.model.meshes)

    exportable.gltf.model.meshes.extend(file.gltf.model.meshes)


    # Nodes
    for x in file.gltf.model.nodes:
        x.mesh += file.currentzero

    exportable.gltf.model.nodes.extend(file.gltf.model.nodes)


    # Scenes
    for scene in file.gltf.model.scenes:
        for x in range(len(scene.nodes)):
            scene.nodes[x] += file.currentzero
    
        
        if file.gltf.model.scenes.index(scene) == len(exportable.gltf.model.scenes) - 1: 
            exportable.gltf.model.scenes[file.gltf.model.scenes.index(scene)].nodes.extend(scene.nodes)
        else:
            exportable.gltf.model.scenes.append(scene)


exportable.gltf.export('exportedmodel.glb')