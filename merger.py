from gltflib import (GLTF, GLTFModel, GLBResource)
import gltflib
import os


class model:
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

filearray = []

for filename in os.listdir('./Put files here'):
    if filename.endswith('.glb') or filename.endswith('.gltf'):
        filearray.append("Put files here/{}".format(filename))


for filename in filearray:
    currentzero = 0

    file = model(GLTF.load(filename))
    
    # Buffer and binary
    for buffer in file.gltf.model.buffers: 
        exportable.gltf.model.buffers[0].byteLength += buffer.byteLength
        
        if (buffer.uri != None) and buffer.uri.endswith('.bin'):
            with open("Put files here/{}".format(buffer.uri), 'rb') as bin:
                bytes = bin.read()
                exportable.gltf.resources[0].data += bytes
        else:
            exportable.gltf.resources[0].data += file.gltf.resources[0].data
    
    
    # Buffer views
    currentzero = len(exportable.gltf.model.bufferViews)
    
    exportable.gltf.model.bufferViews.extend(file.gltf.model.bufferViews)
    
    for i in range(1, len(exportable.gltf.model.bufferViews)):
        prior = exportable.gltf.model.bufferViews[i - 1]
        
        exportable.gltf.model.bufferViews[i].byteOffset = (
            prior.byteLength + prior.byteOffset
        )
    
    
    # Textures
    if file.gltf.model.textures != None:
        for texture in file.gltf.model.textures:
            texture.sampler += currentzero
    
    
    # Accessors
    currentzero = len(exportable.gltf.model.accessors)
    for accessor in file.gltf.model.accessors:
       accessor.bufferView += currentzero


    for mesh in file.gltf.model.meshes:
        for primitive in mesh.primitives:
            primitive.attributes.POSITION += currentzero
            primitive.attributes.NORMAL += currentzero
            primitive.attributes.TEXCOORD_0 += currentzero
        
            primitive.indices += currentzero
       
       
    exportable.gltf.model.accessors.extend(file.gltf.model.accessors)


    # Materials and meshes
    if file.gltf.model.materials is not None:
        currentzero = len(exportable.gltf.model.materials)
        
        for mesh in file.gltf.model.meshes:
            for primitive in mesh.primitives:
                if primitive.material != None:
                    primitive.material += currentzero
                    
        
        exportable.gltf.model.materials.extend(file.gltf.model.materials)


    # Meshes
    currentzero = len(exportable.gltf.model.meshes)

    exportable.gltf.model.meshes.extend(file.gltf.model.meshes)
    
    
    # Nodes
    for x in file.gltf.model.nodes:
        x.mesh += currentzero

    exportable.gltf.model.nodes.extend(file.gltf.model.nodes)
    

    # Scenes
    for scene in file.gltf.model.scenes:
        for x in range(len(scene.nodes)):
            scene.nodes[x] += currentzero
    
        
        if file.gltf.model.scenes.index(scene) == len(exportable.gltf.model.scenes) - 1: 
            exportable.gltf.model.scenes[file.gltf.model.scenes.index(scene)].nodes.extend(scene.nodes)
        else:
            exportable.gltf.model.scenes.append(scene)


exportable.gltf.export('exportedmodel.glb')