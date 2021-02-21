# Wreckfest Toolbox
A blender addon

### Why ?
This addon aim to stream line the process of creating mod for the Game [Wreckfest](https://bugbeargames.com/).

### How ?
By bundling easy to use tools in a nice UI, and give hints on how to create mods for Wreckfest in Blender

## Tools
### Wreckfest Wrapper Node
The Wreckfest Wrapper Node is a Shader Node that allow you to set the textures of your materials, with a wreckfest naming display.
It use a Principled BSDF shader in the end for maximum compatibility, and try to show your model in blender as close as it should appear in wreckfest

**Where to Find :** in the material node graph, do Shift+A -> Wreckfest -> Wreckfest Wrapper **OR** Add -> Wreckfest -> Wreckfest Wrapper.

### Wreckfest Custom Data
Set wreckfest custom data, to handle collision models, visibility, and other technical stuff.
An easy to use tool, where you just have to set the custom data to True, False, or select Unset if you want to remove the data.

**Where to Find :** select an object, Right Click -> Wreckfest -> Manage Custom Data

### Wreckfest Exporter
Export your scene into a .bgo3 file. First, select Set Path & Export, select your file in the export window, when you valid, the addon store the path into your .scene file. And then, you just have to use direct export to export the scene into the previously set path. You can change the path at any moment by using Set Path & Export again.

**Where to Find:** show your side menu (Shortcut : N) and go into Wreckfest Panel. Into the Export SubMenu

## How to install
Download the master branch as a .zip file. Then into blender go into Edit -> Preferences -> Add-ons, then press Install... and select the archive. Don't forget to enable the add-on

## Usefull links
[Addon Roadmap](https://trello.com/b/ttLmiQLY)

[Addon Discord](https://discord.gg/BKB6geB3ku)

[Bugbear Community Forum](http://community.bugbeargames.com/)

[Bugbear Modding Discord](https://discord.gg/Zxv3JuVXrk)
