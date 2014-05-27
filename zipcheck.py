## DATA SOURCE: http://vterrain.org/Elevation/global.html

import os, zipfile
from Tkinter import Tk
import tkFileDialog
import tkMessageBox

Tk().withdraw() # keep the root window from appearing

fileroot = r'D:\Code\PythonScripts\demfiles'

def inputExists(location):
    if (location == ""):
        sys.exit()
    else:
        return

#options for download directory    
dir_opts = options = {}
options['initialdir'] = fileroot
options['mustexist'] = True
options['title'] = 'Downloaded file(s) check location'

saveLoc = tkFileDialog.askdirectory(**dir_opts)
inputExists(saveLoc)

print "Testing zip files located here: " + saveLoc

deleted = []

for root, dirs, files in os.walk(saveLoc):
    for i in files:
        print "Checking.... " + i
        ziploc = os.path.join(root, i)       
        try:
            test = zipfile.ZipFile(ziploc)
            ret = test.testzip()
            #print "GOOD zip file"
            test.close()        
        except:
            #print "BAD zip file"
            test.close()
            deleted.append(i)            
            pass

if (len(deleted) > 0):
    
    print "The following are corrupt zip files: "
    for d in deleted:
        print d
        
    result = tkMessageBox.askquestion("DELETE", "Delete corrupt zip files?", icon='warning')

    if (result == "yes"):
        for de in deleted:
            os.remove(os.path.join(root, de))
        print "Corrupt files removed"
    else:
        print "Files NOT deleted"

print "COMPLETED"
