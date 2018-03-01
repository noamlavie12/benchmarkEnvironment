import time
import psutil
import subprocess
import os

def RunExe(fileName, outputFileName):
    procesObject = subprocess.Popen([fileName, outputFileName + "_01", "Quick"])
    pid = procesObject.pid
    psUtilObject = psutil.Process(pid)
    psUtilObject.cpu_percent()
    keepLooping = True
    while keepLooping:
        try:
            cpuPercent = psUtilObject.cpu_percent()
            outputFile = open(outputFileName,'a')
            outputFile.write(str(cpuPercent) + '\n')
            outputFile.close()
            time.sleep(1)
        except:
            keepLooping = False
            outputFile.close()
    
    return

print "starting..."

dirName = time.strftime("%Y%m%d%H%M%S", time.gmtime())
if not os.path.exists(dirName):
    os.makedirs(dirName)

fileName = "C:\\git\\rsEngineG2\\rsEngine.Tester\\bin\\Debug\\rsEngine.Tester.exe"
outputFileName = dirName + "\\katamonOutput"

RunExe(fileName, outputFileName)
