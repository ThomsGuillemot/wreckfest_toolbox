@echo off
setlocal EnableDelayedExpansion
set scriptdir=%~dp0
set in_drive=%~d1
set in_path=%~p1
set in_filename=%~n1
set in_extension=%~x1
set in_fullpath=%~f1
set out_drive=%~d2
set out_path=%~p2
set out_filename=%~n2
set out_noext=%out_drive%%out_path%%out_filename%
if x"%out_noext%" == x"" set out_noext=%in_drive%%in_path%%in_filename%

REM Textures
if x"%in_extension%" == x".tga" goto :BuildTexture
if x"%in_extension%" == x".TGA" goto :BuildTexture
if x"%in_extension%" == x".png" goto :BuildTexture
if x"%in_extension%" == x".PNG" goto :BuildTexture

REM Geometry
if x"%in_extension%" == x".bgo3" goto :BuildObject
if x"%in_extension%" == x".BGO3" goto :BuildObject

echo Error: .tga, .png or .bgo3 file needed
pause
exit /b 1

:BuildTexture
"%scriptdir%bimage.exe" -auto -input "%in_fullpath%" -output "%out_noext%.bmap" || (pause && exit /b 1)

goto :TooltipBalloon

:BuildObject
set vehicle_test=vehicle
if not "x!in_path:%vehicle_test%=!"=="x%in_path%" (
	"%scriptdir%bgeometry.exe" -v -vhcl -input "%in_fullpath%" -output "%out_noext%.vhcl" || (pause && exit /b 1)
) else (
	"%scriptdir%bgeometry.exe" -v -input "%in_fullpath%" -output "%out_noext%.scne" || (pause && exit /b 1)
)

goto :TooltipBalloon

:TooltipBalloon
::Tooltib Balloon
::By SachaDee - 2016

@echo off
set "$Titre=BGO BUILDER"
Set "$Message=Build BGO done"

::Pour L'icone valeur possible Information, error, warning, none

Set "$Icon=Information"

for /f "delims=" %%a in ('powershell -c "[reflection.assembly]::loadwithpartialname('System.Windows.Forms');[reflection.assembly]::loadwithpartialname('System.Drawing');$notify = new-object system.windows.forms.notifyicon;$notify.icon = [System.Drawing.SystemIcons]::%$Icon%;$notify.visible = $true;$notify.showballoontip(10,'%$Titre%','%$Message%',[system.windows.forms.tooltipicon]::None)"') do (set$=)

goto :EOF

