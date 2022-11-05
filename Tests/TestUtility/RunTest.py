import importlib

from Tests.TestUtility import TestInit
import traceback
import sys
import os
import shutil
import sys
import time

sys.path.insert(1, '/home/pi/actions-runner/_work/Project2/Project2/')


from Tests.TestUtility.CreateTestReport import CreateTestReport

from Controls import ReadUSB
from os.path import exists
import subprocess

#main test runner class
class RunTest:
    #run method, pass in file containing tests to run
    def run(self,testFile):
        #stores test python modules, key = name of test
        self.testsDict = { }
        #stores paths to test folders, key = name of test
        self.pathsDict = { }
        #dictionary of tests to run, retreived from txt file
        self.testsToRun = { }
        #writes to results file created in init
        self.resultsFile.write("---- Running " + testFile + " tests ----\n\n")
        #parse test run file
        file = open('Tests/TestRuns/' + testFile,'r')
        #split on new line
        file = file.read().split('\n')
        #remove empty values
        file = list(filter(None,file))
        self.testsToRun = file

        #all tests will be added to module dict and path dict
        self.findTests()

        self.resultsFile.write("Building hex files\n\n")
        #go through every test path and build c++ file into hex
        startTime = time.time()
        for i in self.testsToRun:
            if(i != ""):
                if self.buildUBitCode(i) == 0:
                    return False
        endTime = time.time()

        timeE = endTime - startTime
        formatTime = "{:.2f}".format(timeE)
        self.resultsFile.write("\nAll files compiled in - " + formatTime +  "\n\nRunnning tests\n\n")
        startTime = time.time()
        #run every test
        for i in self.testsToRun:
            if(i != ""):
                self.runTest(i)
        endTime = time.time()
        timeE = endTime - startTime
        formatTime = "{:.2f}".format(timeE)
        self.resultsFile.write("\nAll tests run in  - " + formatTime)
        self.resultsFile.write("\n\n")

        return self.allPassed

    def runTest(self,NameOfTest):
        #create test report instance for next test
        report = CreateTestReport(self.testInit.path + "/" + NameOfTest)
        #add size of hex file
        report.setSize(os.path.getsize(self.pathsDict[NameOfTest] + "/MICROBIT.hex")/1024)
        endTime = 0
        try:
            #copy hex to microbit
            self.copyHex(NameOfTest)
            startTime = time.time()
            #call run method on test module
            self.testsDict[NameOfTest].run(self.testInit.serial,report)
            endTime = time.time()
            #if no error, passed test. Test will throw exception on error
            self.resultsFile.write(NameOfTest + " ====== Passed ======\n")
        except:
            endTime = time.time()
            self.resultsFile.write(NameOfTest +  " ------ Failed ------\n")
            #add caught exception to test report
            report.addError(traceback.format_exc())
            self.allPassed = False
            print(NameOfTest + " failed")

        timeE = endTime - startTime
        formatTime = "{:.2f}".format(timeE)
        report.addTime(formatTime)
        report.writeToFile()


    def buildUBitCode(self,testPath = None):

        #locate c++ file of current test
        self.testPath = self.pathsDict[testPath] + "/" +  testPath + ".cpp"
        #copy to build source
        shutil.copyfile(self.testPath, "../microbit-v2-samples/source/main.cpp")
        #build
        process = subprocess.Popen("./Scripts/buildScript.sh", shell=True, stdout=subprocess.PIPE)
        process.wait()

        #if built success, hex no exists 
        if  exists('../microbit-v2-samples/MICROBIT.hex'):
            size = os.path.getsize("../microbit-v2-samples/MICROBIT.hex")/1024
            formatSize = "{:.2f}".format(size)
            self.resultsFile.write(testPath +  " built succesfully - size of file + " +  str(formatSize) + "kB\n")
            #temp move back to test folder
            process = subprocess.Popen("./Scripts/moveScript.sh " + self.pathsDict[testPath] + "/MICROBIT.hex", shell=True, stdout=subprocess.PIPE)
            process.wait()
            time.sleep(0.4)
        else:
            self.resultsFile.write(testPath +   " failed to build\n")
            print(testPath + " failed to build")
            self.allPassed = False
            return 0

    def copyHex(self,path):
        #copy hex to ubit
        process = subprocess.Popen("./Scripts/copyScript.sh " + self.pathsDict[path] + "/MICROBIT.hex", shell=True, stdout=subprocess.PIPE)
        process.wait()
        #sleep important as checks it exists too fast
        time.sleep(1)
        #if hex file still in folder, failed to transfer
        if exists( path + '/MICROBIT.hex'):
                self.resultsFile.write(path +   " failed to copy to micro:bit\n")
                os.remove(path + '/MICROBIT.hex')
                time.sleep(0.4)
                self.allPassed = False
                print(path + " failed to copy")

                return 0
        #get ready code
        wait  = ReadUSB.readReady(self.testInit.serial,3)
        if("Ready" not in wait):
            return 0

        time.sleep(0.4)
        return 1

    def findTests(self):
        #go through all subfolders in testfolders and check if contains c++ and .py file
        for a,b,c in os.walk(os.getcwd() + "/Tests/TestFolders"):
            for x in range(len(c)):
                if("__pycache__" not in a and  "__init__" not in c[x] and ".py" in c[x]):
                    temp = c[x].split(".")[0]
                    testname = temp
                    #check if file is to be run
                    if testname not in self.testsToRun:
                        break
                    #if already been run in this test run
                    if exists(self.testInit.path + "/" + testname + ".txt"):
                        print("Attempted to run same test twice in 1 run - " + testname + " - removing from current run")
                        self.testsToRun.remove(testname)
                        break
                    #import module into dict
                    rel_dir = os.path.relpath(a, "project")
                    new_rel = rel_dir.replace("/",".") + "." + testname
                    i = importlib.import_module(new_rel[3:])
                    self.testsDict[testname] = i
                    self.pathsDict[testname] = rel_dir[3:]

    def cleanUp(self):
        #close open files
        self.testInit.serial.close()
        self.resultsFile.close()

        #delete built hex file, so not carried over
        if exists('../microbit-v2-samples/MICROBIT.hex'):
            os.remove('../microbit-v2-samples/MICROBIT.hex')
        #delete all remaining hex files
        for a,b,c in os.walk(os.getcwd() + "/Tests/TestFolders"):
            for x in range(len(c)):
                if ".hex" in c[x]:
                    os.remove(a + "/" + c[x])



    def __init__(self) -> None:

        #init
        self.testsDict = { }

        self.pathsDict = { }

        self.testsToRun = { }

        self.allPassed = True
        #create test init instance for current run
        self.testInit = TestInit.testInit()
        self.resultsFile = self.testInit.resultsFile
