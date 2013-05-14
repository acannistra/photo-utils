#!/usr/bin/env/python
import fnmatch
import sys
import os
import shutil

# Script to move RAW files. Should be run inside named directory that contains raw files.
# To be run on OSX only.


backupDir  = "/Volumes/Tony Cannistra 4017930916/PhotoBackup"
currentDir = os.getcwd()
topLevel   = 'Photography'  # ensures that we're exactly one level 
                            # down from the main photo directory
rawFmts    = ["*.CR2", "*.cr2", "*.DNG", "*.dng"]
jpgFmts    = ["*.JPG", "*.jpg"]

def confirm(prompt, resp=True):
       
    if prompt is None:
        prompt = 'Confirm'

    if resp:
        prompt = '%s [%s]|%s: ' % (prompt, 'y', 'n')
    else:
        prompt = '%s [%s]|%s: ' % (prompt, 'n', 'y')
        
    while True:
        ans = raw_input(prompt)
        if not ans:
            return resp
        if ans not in ['y', 'Y', 'n', 'N']:
            print 'please enter y or n.'
            continue
        if ans == 'y' or ans == 'Y':
            return True
        if ans == 'n' or ans == 'N':
            return False

#check to see if drive is mounted:
print "Looking for drive...",
if os.path.exists(backupDir):
	print "ok."
else:
	raise IOError("Drive not mounted (tried "+backupDir+").")





# find raw files
rawfiles = []
numjpgs  = 0
for folder, subs, files in os.walk(currentDir):
    if len(subs) > 5:
        raise RuntimeError("Too many subdirectories. folder: "+folder+".")
    for rawFmt in rawFmts:
        for filename in fnmatch.filter(files, rawFmt):
            rawfiles.append(os.path.abspath(os.path.join(folder, filename)))
    for jpgFmt in jpgFmts:
        for filename in fnmatch.filter(files, jpgFmt):
            numjpgs = numjpgs + 1

if len(rawfiles) == 0:
    raise RuntimeError("No raw files found in this directory.")

#check for jpgs:
if numjpgs == 0:
	if not confirm("There are no jpgs in this directory. Continue?"): sys.exit(1)

# Check for raw move:

if not confirm("Found "+str(len(rawfiles))+" raw files. Move?"): sys.exit(1)

#Create Destination Directory

# Top directory should be 'Photography':

if os.path.split(os.path.dirname(os.getcwd()))[1] == topLevel:
    curName = os.path.split(currentDir)[1]
    if confirm("Name ok?: "+os.path.join(backupDir, curName)):
        destDir = os.path.join(backupDir, curName)
    else:
        destDir = raw_input("Desired backup directory name: ")
else:
    raise RuntimeError("Not at top level "+topLevel+" directory, aborting.")

if not os.path.exists(destDir):
    os.makedirs(destDir)
else:
    if not confirm("Destination directory exists. Continue?"): sys.exit(1)

# Move Files!

print "Begin move:"
for rawFile in rawfiles:
    filename = os.path.split(rawFile)[1]
    destPath = os.path.join(destDir, filename)
    print "\t"+os.path.split(rawFile)[1]+ " --> "+ destPath
    shutil.move(rawFile, destPath)

print "Done. Moved "+str(len(rawfiles))+" files to "+destDir




