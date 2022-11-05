import subprocess
import sys
import traceback

#for imports
sys.path.append('../Project2')
from Tests.TestUtility import RunTest



class main_test:
    
    if __name__ == '__main__':
        #check recieved file path as parameter
        if(len(sys.argv) < 2):
            print("Missing test file .txt")
            exit(1)
        test = RunTest.RunTest()
        allPassed = True

        try:
            #if returns false something failed
            if test.run(sys.argv[1]) == False:
                allPassed = False
            if allPassed == False:
                print("1 or more tests failed")
                exit(1)
            else:
                print("All tests passed")
        except Exception as e:
            #if exception recieved something crashed
            print("Failed to run tests\n")
            print(traceback.format_exc())
            print(e)
            exit(1)
        finally:
            #always cleanup and push results to repo
            test.cleanUp()
            process = subprocess.Popen("./Scripts/pushScript.sh", shell=True, stdout=subprocess.PIPE)
            process.wait()