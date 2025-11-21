# GameRig

GameRig is an auto rigging for games addon for Blender.
It is a so called feature set made for creating game engine compatible rigs using a workflow built on top of the Rigify system.
The current version has been developed for use with Blender 4.5.4 LTS and 5.0. Other versions might be compatible as well, this needs further testing.
Whenever Rigify updates, and it often does, it has potential to break GameRig so maintaining this extension is a constant effort. I will do my best to keep it working with the latest versions.


> ## Differences between GameRig and Rigify
> 
> There are three essential problems with Rigify when it comes to rigging for games:
> * The deformation bones, which is the only part that needs to be exported, are not in a single bone hierarchy. For that reason, many unnecessary bones will be exported together with the deform bones. Besides this resulting in adding unnecessary complexity, it could also produce root bone issues. Unreal Engine, for example, will compain if your skeleton has multiple root level bones.
> * Deformation bones are scaled. This can produce some weird behavior as scaling is handled completely differently in a Blender rig and in game engines.
> * Bendy bones are used for deformation. While this will not produce any errors because these bones will be exported as regular bones, it is still not desired to have them in the rig. Mainly because the deformation you will see in Blender will not reflect how this deformation will look in the game engine.

> GameRig solves all three of these problems. It puts the deformation bones in a single hierarchy for a clean export, scaling on deformation bones is disabled by default and there will be no bendy bones in the rig.

> ## Installation instructions
> 
> Download the latest release zip file from:
> 
> <https://github.com/Arminando/GameRig/releases>
> 
> Go to Edit > Preferences > Add-ons and enable Rigify (1)
> 
> Click on Install Feature Set From File... and in the file browser select the zip file you downloaded earlier (2)
> 
> ![Installation instructions](images/installation_enable_rigify.png)
> 
> That is it already.
> 

> ## Usage instructions
> 
> Exactly the same as regular rigify but make sure to only use the rig types that have the "game." prefix.
> With v2.0, GameRig automatically converts the regular rig types to game rig types. Just make your rig the usual rigify way but press the Generate GameRig button instead of Generate Rig.
> This will change the rig types to their game rig equivalents so when you continue editing your metarig you can adjust the game rig specific type properties.
