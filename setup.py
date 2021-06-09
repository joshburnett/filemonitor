# -*- coding: utf-8 -*-

# A simple setup script to create an executable using PyQt4. This also
# demonstrates the method for creating a Windows executable that does not have
# an associated console.
#
# PyQt4app.py is a very simple type of PyQt4 application
#
# Run the build process by running the command 'python setup.py build'
#
# If everything works well you should find a subdirectory in the build
# subdirectory that contains the files needed to run the application

import sys, os
import guidata
from cx_Freeze import setup, Executable


'''
Parse the build_record.txt file, determining the last build number.
Increment the build number, and add the appropriate info to the build record.

build_record.txt looks like:

build #,version,datetime
1,0.0.5,2010.10.22 12:00:00
'''

from datetime import datetime
from filemonitor import __version__

buildRecord = open('build_record.txt','a+')
buildNum = int(buildRecord.readlines()[-1].split(',')[0]) + 1
buildDate = datetime.now()
buildRecord.write('%i,%s,%s\n' % (buildNum,__version__,buildDate.strftime('%Y.%m.%d %H:%M:%S')))
buildRecord.close()



base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

options = {
    'build_exe': {
        'includes':      'atexit',
        'excludes':      'urllib,matplotlib,collections.sys,collections._weakref,scipy,PIL,nose,compiler,pyreadline,_ssl,lxml.etree,pandas.algos,_hashlib',
        'bin_excludes':  ['QtWebKit4.dll','QtScript4.dll','QtNetwork4.dll','tk85.dll','tcl85.dll','QtOpenGL4.dll'],
        'include_files': ['format_strings.txt', 'sample_data.log', 'build_record.txt',
                         (os.path.join(guidata.__path__[0], 'images'), 'guidata/images')],
    }
}

executables = [
    Executable('filemonitor.py', base=base,
               targetName   = 'File Monitor.exe',
               icon         = 'icons/graph_icon.ico',
               targetDir    = 'dist/File Monitor',
               )
]

setup(name          = 'File Monitor',
      version       = "%s.%03i" % (__version__,buildNum),
      description   = "File Monitor, build %i (%s)" % (buildNum,buildDate.strftime('%Y.%m.%d %H:%M:%S')),
      options       = options,
      executables   = executables, requires=['pyqtgraph', 'guidata', 'scanf']
      )
