@echo off
for %%a in (%*) do (
	echo %%a
	call "C:\Program Files\Steam\steamapps\common\Wreckfest\tools\custom_build_asset.bat" %%a
	echo:
)
pause