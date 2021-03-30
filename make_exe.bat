echo off
rem *** Create a Python executable
 
rem *** First, get rid of all the old files in the build folder 
rmdir /S /Q "build"

rem *** Create the exe 
python setup.py build

rem *** Pause so we can see the exit codes for cx_Freeze
REM pause "Done compiling... press any key to continue"


rem *** skip creating distributable zip file for now
REM GOTO End


rem ===================================================

rem *** Create a .zip file for distribution
del /Q ".\File Monitor - executable.exe"
del /Q ".\File Monitor.zip"


rem ** add 7-Zip location to path
path C:\Program Files\7-Zip;%PATH%

rem *** Change directory name so .zip file has a more sensible structure
move "build\exe.win-amd64-2.7" "File Monitor - executable"

rem 7z u "File Monitor.zip" ".\File Monitor - executable"
7z a -sfx "File Monitor - executable.exe" ".\File Monitor - executable"

rem *** Change directory name back for consistency (cx_Freeze always creates 'build' directories)
rem move "File Monitor - executable" "build\exe.win-amd64-2.7"

rem pause "done... press any key to quit"

:End