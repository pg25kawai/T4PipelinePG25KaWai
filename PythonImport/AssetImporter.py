# Copyright PG25KaWai

import unreal
import os


def importAssets():

    # The parent directory of this python script
    dir_path = os.path.dirname(os.path.realpath(__file__))

    fileNames = [
        dir_path + '/Yoda.FBX',
        dir_path + '/Yoda_BaseColorOpacity.TGA',
        dir_path + '/Yoda_NormalDX.TGA',
        dir_path + '/Yoda_EmissiveRoughAOMetal.TGA',
    ]

    # Create asset tools object
    assetTools = unreal.AssetToolsHelpers.get_asset_tools()
    assetImportData = unreal.AutomatedAssetImportData()

    # Set assetImportData attributes
    assetImportData.destination_path = '/Game/Import'
    assetImportData.filenames = fileNames
    assetImportData.replace_existing = True
    assetTools.import_assets_automated(assetImportData)

    buildSelectedAssets(assetImportData.destination_path, fileNames)


def buildSelectedAssets(folderPath, fileNames):

    textures = []
    geo = []

    EAL = unreal.EditorAssetLibrary()

    # Iterate files in folder to find Static Mesh and Texture files
    for assetPath in EAL.list_assets(folderPath):
        assetPath = assetPath.split('.')[0]
        asset = EAL.load_asset(assetPath)

        try:
            asset.get_editor_property('asset_import_data')
                
            if isinstance(asset, unreal.StaticMesh):
                geo.append(asset)
            if isinstance(asset, unreal.Texture):
                textures.append(asset)

        except:
            # Not all assets have asset import data 
            pass

    replaceDefaultMaterialInstances(folderPath, geo, textures)


def replaceDefaultMaterialInstances(folderPath, geo, textures):

    materialInstances = []
    assetTools = unreal.AssetToolsHelpers.get_asset_tools()

    # This is the material template
    # We will swap out the default base color, normal map, and emissive...
    materialParent = unreal.EditorAssetLibrary().load_asset(
        '/Game/AssetImportTemplate/M_Template')
    for staticMesh in geo:

        assetName = staticMesh.get_name()
        for staticMaterial in staticMesh.static_materials:

            # Get the index of the current static material
            index = staticMesh.static_materials.index(staticMaterial)

            # Locate and delete the materials come with import
            matPath = staticMaterial.material_interface.get_path_name()
            unreal.EditorAssetLibrary.delete_asset(matPath)

            # Create new material instance
            materialInstance = assetTools.create_asset(
                staticMaterial.material_slot_name,
                folderPath,
                unreal.MaterialInstanceConstant,
                unreal.MaterialInstanceConstantFactoryNew(),
            )

            materialInstances.append(materialInstance)

            # Set parent material so that we can use the same connections
            materialInstance.set_editor_property('parent', materialParent)

            # Assign new material instance to correct material slot
            staticMesh.set_material(index, materialInstance)

            swapTextures(textures, assetName, materialInstance)


def swapTextures(textures, assetName, materialInstance):

    for texture in textures:

        # Identify textures associated with asset by naming convention
        if assetName in texture.get_name():

            # Get the last string after _ 
            # i.e. Yoda_BaseColorOpacity -> BaseColorOpacity
            parameterName = texture.get_name().split('_')[-1]
            # Set up material instance parameter
            unreal.MaterialEditingLibrary.set_material_instance_texture_parameter_value(
                materialInstance,
                parameterName,
                texture
        )

importAssets()