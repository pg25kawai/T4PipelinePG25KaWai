**PG25 T4 A3: Tool App**
Submitted by: pg25kawai KaWai Chen
Date: April 10 2024
----------
This is a python script for Unreal. It imports static mesh and texture assets and automatically create a new material instance using the textures.
The material is hooked up according to the template provided. 
I followed this tutorial: https://www.youtube.com/watch?v=yv7o43xsJ3I

**Download/Install**
---------
 - Clone from https://github.com/pg25kawai/T4PipelinePG25KaWai.git
 - Make sure the branch is main


**How to use**
--------
 - After cloning the repo, open the folder PythonImport, copy the folder AssetImportTemplate (there is a file called M_Template.uasset in it)
 - Paste the folder into the Content folder in any Unreal project. Note that this step is done via file explorer. Do NOT import the uasset into Unreal
 - Open the Unreal project (i.e. the project you just pasted the AssetImportTemplate folder into)
 - On the top bar, click Tools, then select Execute Python Script
 - Select AssetImporter.py in the PythonImport folder you just cloned
 - In Unreal, go to Content/Import, which is created by the script
 - You will find that Yoda is imported and the material instances are hooked up the same way as M_Template