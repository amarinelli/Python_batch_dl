## DATA SOURCE: http://vterrain.org/Elevation/global.html

import urllib, os, time, socket

dlist = open(r"D:\Code\PythonScripts\demfiles\Files5.txt", "r")
saveLoc = r"D:\Code\PythonScripts\demfiles\downloaded"

counter = 1
current = 0
errorList = []
socket.setdefaulttimeout(30)

with dlist as f:
    total = sum(1 for _ in f)

print "Total files to download = " + str(total) + "\n"

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

dlist = open(r"D:\Code\PythonScripts\demfiles\Files5.txt", "r")

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
        
    except KeyboardInterrupt:
        print "Cancelled file download with Keyboard\n"
        errorList.append(i)
        counter +=1
        pass
    except socket.timeout:
        print "TIMEOUT\n"
        errorList.append(i)
        counter +=1
        pass
    except:
        "UNKNOWN ERROR"
    
if (len(errorList) > 0):
    print "DOWNLOAD COMPLETE, %s ERROR(S):" % len(errorList)
    errorFile = open(r"D:\Code\PythonScripts\demfiles\errorList.txt", "w")
    for e in errorList:        
        errorFile.write(e + "\n")
    errorFile.close()
    
else:
    print "DOWNLOAD COMPLETE"
