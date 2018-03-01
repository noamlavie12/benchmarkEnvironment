import time
import psutil
import subprocess
import os
from shutil import copyfile
from filecmp import cmpfiles
from pickle import FALSE

def RunExe(fileName, outputFileName):
    procesObject = subprocess.Popen([fileName, outputFileName, "Quick"])
    pid = procesObject.pid
    psUtilObject = psutil.Process(pid)
    psUtilObject.cpu_percent()
    cpuUse = []
    keepLooping = True
    while keepLooping:
        try:
            cpuPercent = psUtilObject.cpu_percent()
            cpuUse.append(cpuPercent)
            time.sleep(1)
        except:
            keepLooping = False

    return cpuUse

print "starting..."

def CreateDictFromFile(filePath, delimiter):
    dict = {}
    file = open(filePath, 'r')
    for line in file:
        splitedLine = line.split(delimiter)
        lineList = splitedLine[1:]
        dict[splitedLine[0]] = lineList
        
    file.close()
    return dict
        
def CmpFiles(file1, file2):
    d1 = CreateDictFromFile(file1, ',')
    d2 = CreateDictFromFile(file2, ',')
    
    d1_keys = set(d1.keys())
    d2_keys = set(d2.keys())
    intersect_keys = d1_keys.intersection(d2_keys)
    added = d1_keys - d2_keys
    removed = d2_keys - d1_keys
    modified = {o : (d1[o], d2[o]) for o in intersect_keys if d1[o] != d2[o]}
    same = set(o for o in intersect_keys if d1[o] == d2[o])
    print "added = " + str(added)
    print "removed = " + str(removed)
    return (0 == len(added) and 0 == len(removed))


def WriteScanResFile(dirName, outputFileName, expectedFileName, counter):
    scanResualtFileName = dirName + "\\scan_resualte_" + str(counter) + ".txt"
    expectedDict = CreateDictFromFile(expectedFileName, ',')
    realDict = CreateDictFromFile(outputFileName, ',')
    scanResualtsFile = open(scanResualtFileName, 'a')
    for threat in realDict:
        scanResualtsFile.write(threat)
        if threat in expectedDict:
            scanResualtsFile.write('-find')
        else:
            scanResualtsFile.write('-didnt find')
        scanResualtsFile.write('\n')
    
    scanResualtsFile.close()

def TestSpecigicDLL(dllName):
    #replace the dll to the new one
#     engineDllPlace = "C:\\git\\rsEngineG2\\rsEngine.Tester\\bin\\Debug\\rsEngine.dll"
#     copyfile(dllName, engineDllPlace)

    dirName = time.strftime("%Y%m%d%H%M%S", time.gmtime())
    if not os.path.exists(dirName):
        os.makedirs(dirName)
    
    fileName = "C:\\git\\rsEngineG2\\rsEngine.Tester\\bin\\Debug\\rsEngine.Tester.exe"
    #fileName = "dummyFile.py"
    outputFileName = dirName + "\\runOutput"
    expectedFileName = "katamonOutput-expected.txt"
    cpuUseFileName = dirName + "\\cpu_use.txt"
    runAmount = 5
    runDetailsFileName = dirName + "\\run details.txt"
    
    for i in range(runAmount):
        print "run number: " + str(i)
        start = time.time()
        cpuUse = RunExe(fileName, outputFileName + "_" + str(i) + ".txt")
        end = time.time()
        duration = end - start
        
        runDetailsFile = open(runDetailsFileName, 'a')
        isCorrect = CmpFiles(outputFileName, expectedFileName)
        runDetailsFile.write('run number: ' + str(i) + str(duration) + ',' + isCorrect + '\n')
        runDetailsFile.close()
        
#         cpuUseFileName = dirName + "\\cpu_use_" + str(i) + ".txt"
        cpuFile = open(cpuUseFileName, 'a')
        cpuFile.write('0.0')
        for sample in cpuUse:
            cpuFile.write(',' + str(sample))
        cpuFile.write('\n')
        cpuFile.close()
        
        #WriteScanResFile(dirName, outputFileName, expectedFileName, i)
        
    #CmpFiles(outputFileName, expectedFileName)
    
    
    
    # max = max(cpuUse)
    # avg = sum(cpuUse)/len(cpuUse)
    # print "time: " + str(end - start)
    # print "max: " + str(max)
    # print "avg: " + str(avg)
if __name__ == '__main__':
    print "rak hapoel"
    TestSpecigicDLL("dllName")
    