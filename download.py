## DATA SOURCE: http://vterrain.org/Elevation/global.html

import urllib, os, time, socket, sys
from Tkinter import Tk
import tkFileDialog

Tk().withdraw() # keep the root window from appearing

root = r'D:\Code\PythonScripts\demfiles'

def inputExists(location):
    if (location == ""):
        sys.exit()
    else:
        return

#options for opening a file
file_opts = options = {}
options['defaultextension'] = '.txt'
options['filetypes'] = [('all files', '.*'), ('text files', '.txt')]
options['initialdir'] = root
options['title'] = 'Select download list txt file'

listFile = tkFileDialog.askopenfilename(**file_opts)
inputExists(listFile)

print "Download list: " + listFile

#options for saving to directory    
dir_opts = options = {}
options['initialdir'] = root
options['mustexist'] = True
options['title'] = 'Downloaded file(s) save location'

saveLoc = tkFileDialog.askdirectory(**dir_opts)
inputExists(saveLoc)

print "Save directory: " + saveLoc

#options for opening error list file
errorfile_opts = options = {}
options['defaultextension'] = '.txt'
options['filetypes'] = [('all files', '.*'), ('text files', '.txt')]
options['initialdir'] = root
options['title'] = 'Select an error txt file'

errorFile = tkFileDialog.askopenfilename(**errorfile_opts)
inputExists(errorFile)

print "Error txt File: " + errorFile + "\n"






counter = 1
current = 0
errorList = []
socket.setdefaulttimeout(30)

#Functions
    
def progress_callback(blocks, block_size, total_size):
    global current
    if (current == 0):       
        percent(blocks, block_size, total_size)
        current = time.time()
    else:        
        now = time.time()        
        if ((now - current) >= 5):
            percent(blocks, block_size, total_size)
            current = time.time()

def percent(blocks, block_size, total_size):
    #blocks->data downloaded so far (first argument of your callback)
    #block_size -> size of each block
    #total-size -> size of the file

    percentage = ((blocks*block_size)/float(total_size))*100
    print ("%.2f %% complete" % percentage)


dlist = open(listFile, "r")

with dlist as f:
    total = sum(1 for _ in f)

print "Total files to download = " + str(total) + "\n"    

dlist = open(listFile, "r")

for i in dlist:
    try:        
        path, name = os.path.split(i)    
        name = ''.join(name.split())
        
        print "DOWNLOADING -->  " + i + " (file %s of %s .... %s remaining)\n" % (counter, total, total-counter)
        
        (file, headers) = urllib.urlretrieve(i, os.path.join(saveLoc, name), progress_callback)
        print ""
        print headers
        print "------file downloaded------\n\n"
        counter +=1
        
##    except KeyboardInterrupt:
##        print "Cancelled file download with Keyboard\n"
##        errorList.append(i)
##        counter +=1
##        pass
    
    except socket.timeout:
        print "TIMEOUT ERROR\n"
        errorWrite = open(errorFile, "w")
        errorWrite.write(i + "\n")
        errorWrite.close()
        #errorList.append(i)
        counter +=1
        pass
    except:
        "UNKNOWN ERROR"
    

errorTotal = open(errorFile, "r")
with errorTotal as e:
    e_total = sum(1 for _ in e)
if (e_total > 0):
    print "DOWNLOAD COMPLETE, %s ERROR(S):" % e_total  
    
else:
    print "DOWNLOAD COMPLETE"
