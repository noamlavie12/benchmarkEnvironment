import os
import sys
from zipfile import ZipFile

print "Auto extractor for compressed malware"

rootPath = "C:\Users\Noam Lavie\Downloads\\theZoo-master"

print "Iterating over: " + rootPath
failedPaths = []

shouldClean = 0

print ""
if shouldClean:
    print "Cleaning!!!!!!!!"
print ""

i = 1;

for dirpath, dirs, files in os.walk(rootPath):   
    path = dirpath.split('/')
    zipFilePath = ""
    zipPassword = ""
    passFullPath = ""
    for f in files:
        if ".zip" in f:
            zipFilePath = os.path.join(dirpath, f)
            print zipFilePath
        elif ".pass" in f:
            passFullPath = os.path.join(dirpath, f)
            with open(passFullPath,"r") as passData:
                zipPassword = passData.readline()
                zipPassword = zipPassword.strip()
        elif not ((".md5" in f) or (".sha256" in f)):
            if shouldClean:
                fullPath = os.path.join(dirpath, f)
                os.remove(fullPath)
                print str(i) + ". Removed: " + fullPath
                i = i + 1


    if zipFilePath == "":
        continue

    if not shouldClean:
        print str(i) + ". Extracting: " + zipFilePath + ", with PWD: " + zipPassword
        i = i + 1
    try: 
        if not shouldClean:
            with ZipFile(zipFilePath) as aZip:
                aZip.extractall(pwd=zipPassword, path=dirpath)
            print "------- Success! ------"
    except Exception:
        failedPaths.append(zipFilePath)
        print "------- Fail! ------"

print ""
print ""
print "Failed paths: "
for aPath in failedPaths:
    print "--- " + aPath


print ""
print "Done!"