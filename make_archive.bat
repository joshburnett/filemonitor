echo off

rem *** Create a .zip file for distribution
del /Q "dist\File Monitor.exe"
del /Q "dist\File Monitor.zip"


rem ** add 7-Zip location to path
path C:\Program Files\7-Zip;%PATH%

rem *** Change directory name so .zip file has a more sensible structure
rem move dist "File Monitor"

7z a -sfx "dist\FileMonitor.exe" ".\dist\File Monitor"
7z a "dist\FileMonitor.zip" ".\dist\File Monitor"

rem *** Change directory name back for consistency (py2exe always creates 'dist' directories)
rem move "File Monitor" dist

pause "done... press any key to quit"
