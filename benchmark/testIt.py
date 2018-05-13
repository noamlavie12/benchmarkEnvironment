import time
import psutil
import subprocess
import os
import sys
from shutil import copyfile

def RunExe(fileName, outputFileName):
    procesObject = subprocess.Popen([fileName, outputFileName, "Quick"])
#     procesObject = subprocess.Popen([fileName, outputFileName, "Full"])
    pid = procesObject.pid
    psUtilObject = psutil.Process(pid)
    cpuUse = []
    memoryList = []
    keepLooping = True
    while keepLooping:
        try:
            cpuPercent = psUtilObject.cpu_percent()
            memory = psUtilObject.memory_info().rss
            
            memoryList.append(memory)
            cpuUse.append(cpuPercent)
            if 0 == len(cpuUse) % 50:
                print len(cpuUse)
            time.sleep(1)
        except:
            keepLooping = False

    return cpuUse, memoryList

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
    try:
        d1 = CreateDictFromFile(file1, ',')
    except:
        print "failed to creact dictionary for file " + file1
        return False
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
    return 0 == len(removed)
#     return (0 == len(added) and 0 == len(removed))


def WriteScanResFile(dirName, outputFileName, expectedFileName, counter):
    scanResualtFileName = dirName + "\\scan_resualte_" + str(counter) + ".txt"
    try:
        expectedDict = CreateDictFromFile(expectedFileName, ',')
    except:
        print "failed to creact dictionary for file " + expectedFileName
    
    realDict = CreateDictFromFile(outputFileName, ',')
    scanResualtsFile = open(scanResualtFileName, 'a')
    for threat in expectedDict:
        scanResualtsFile.write(threat)
        if threat in realDict:
            scanResualtsFile.write('-find')
        else:
            scanResualtsFile.write('-didnt find')
        scanResualtsFile.write('\n')
    
    scanResualtsFile.close()


def WriteListToFile(fileName, currentList):
    cpuFile = open(fileName, 'a')
    cpuFile.write('0.0')
    for sample in currentList:
        cpuFile.write(',' + str(sample))
    
    cpuFile.write('\n')
    cpuFile.close()

def DeletCachFoldertContent(folder):
    if os.path.exists(folder):
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                #elif os.path.isdir(file_path): shutil.rmtree(file_path)
            except Exception as e:
                print(e)

def TestSpecigicDLL(rsEnginePath, testPath):

    mainDirName = "..\\scanRes\\" + time.strftime("%Y%m%d%H%M%S", time.gmtime())
    if not os.path.exists(mainDirName):
        os.makedirs(mainDirName)
    
#     folder = "C:\\git\\katamon\\rsEngineG2\\rsEngine.Tester\\bin\\Debug\\"
    fileName = rsEnginePath + "rsEngine.Tester.exe" 
    copyfile(testPath, fileName)
    
    
    cachFolder = rsEnginePath + "Cache"
    deleteCach = True
    

    subFolders = ["noCach", "withCach"]
    subFolders = ["withCach"]
    for subFolder in subFolders:
        if "noCach" == subFolder:
            deleteCach = True
        else:
            deleteCach = False
            
        dirName = mainDirName + "\\" + subFolder
        if not os.path.exists(dirName):
            os.makedirs(dirName)
        expectedFileName = "expected.txt"
        cpuUseFileName = dirName + "\\cpu_use.txt"
        memoryUseFileName = dirName + "\\memory_use.txt"
        runAmount = 10
        runDetailsFileName = dirName + "\\run details.txt"
        for i in range(runAmount):
            print "run number: " + str(i)
            if deleteCach:
                DeletCachFoldertContent(cachFolder)
            outputFileName = dirName + "\\runOutput"  + "_" + str(i) + ".txt"
            start = time.time()
            cpuUse, memoryUsage = RunExe(fileName, outputFileName)
            end = time.time()
            duration = end - start
            
            runDetailsFile = open(runDetailsFileName, 'a')
            isCorrect = CmpFiles(outputFileName, expectedFileName)
            if isCorrect:
                isCorrect = "good scan"
            else:
                isCorrect = "bad scan"
                
            runDetailsFile.write('run number: ' + str(i) + "," + str(duration) + ',' + isCorrect + '\n')
            runDetailsFile.close()
            
            #write cpu file
            WriteListToFile(cpuUseFileName, cpuUse)
            WriteListToFile(memoryUseFileName, memoryUsage)
            WriteScanResFile(dirName, outputFileName, expectedFileName, i)
            
    #CmpFiles(outputFileName, expectedFileName)
    
    
    
    # max = max(cpuUse)
    # avg = sum(cpuUse)/len(cpuUse)
    # print "time: " + str(end - start)
    # print "max: " + str(max)
    # print "avg: " + str(avg)
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "bad input, less than 2 argumants"
    
    dllpath = sys.argv[1]
    testPath = sys.argv[2]
    
#     dllpath = "C:\\git\\katamon\\rsEngineG2\\rsEngine.Tester\\bin\\Debug\\"
#     testPath = "C:\\git\\python\\dlls\\rsEngine.Tester.exe"
    print "start the benchmark environment"
    TestSpecigicDLL(dllpath, testPath)
    