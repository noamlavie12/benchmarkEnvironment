import time
import sys

outputPath = sys.argv[1]

print "start: " + outputPath
time.sleep(1)

file = open(outputPath, "w")
file.write("gordon:9\n")
file.write("gola:7\n")
file.write("hapoel:ole\n")
 
file.close() 
print "finish"