import json
import sys

sys.path.append('../../Project2/')

from Tests.TestUtility import uBitTests

#Class used to store data readings, can be used to output readings to .txt and json files.

class CreateTestReport:

    # Write current data to files. Will write everything stored in instance variables to a .txt and json file
    def writeToFile(self):

        #Check file exists
        if(self.file == None):
            print('error - no file for report')

        #Write data that exists
        self.file.write("Test: " + self.testName + " run at " + self.testTime +  "\n")
        if(self.size != 0 ):
            formatSize = "{:.2f}".format(self.size)
            self.file.write("Size of .hex file " + str(formatSize) + "MB\n")
        if self.passed:
            self.file.write("`````Passed`````\n\n")
        else:
            self.file.write("`````Failed`````\n\n")

        if self.timeElapsed != 0:
            self.file.write("Time elapsed: " + str(self.timeElapsed) + " seconds\n\n")
        if self.error != '':
            self.file.write("~~~~~~~~~Error encountered~~~~~~~~~: \n\n" + self.error + "\n\n")

        if len(self.events) > 0:
            self.file.write("Event counts: \n\n")
            for i in self.events.keys():
                self.file.write(str(i) + " - " + str(self.events[i]) + "\n")
        if len(self.data) > 0:
            self.file.write("\nData detected: ")
            for i in self.data:
                self.file.write("\n" + i + " data: \n")
                for x in self.data[i]:
                    self.file.write(str(x) + " , ")

        if len(self.outputs) > 0:
            for i in self.outputs:
                self.file.write("\nOutput detected from " + i+"\n\n")
                for x in self.outputs[i]:
                    self.file.write(str(x) + "\n")


        self.file.close()
        self.jsonFile.write(json.dumps(self.dataDict,indent=4))
        self.jsonFile.close()



    #Add time reading
    def addTime(self, time):
        self.timeElapsed = time

    #Set size of hex file
    def setSize(self,sizeMb):
        self.size = sizeMb

    #Format event reading
    def formatEvents(self,data):
        split = data.replace(" ", "")

        split = data.split("|")

        componentID = int(split[2])
        eventID = int(split[3])

        componentName = uBitTests.COMPONENTS_NAME_DICT[componentID]

        eventDict = uBitTests.EVENTS_DICT[componentID]
        event = eventDict[eventID]

        eventName =  event

        if eventName not in self.events:
            self.events[eventName] = 1
        else:
            self.events[eventName] += 1

    #Format data reading
    def formatData(self,source, data):
        sourceName = uBitTests.COMPONENTS_NAME_DICT[int(source)]
        dataToinsert = []

        if source == 5:
            xyz = data.split(",")
            xyz = [xyz[0],xyz[1],xyz[2]]
            dataToinsert = xyz

        if sourceName not in self.data:
            self.data[sourceName] = [dataToinsert]
        else:
            self.data[sourceName].append(dataToinsert)


    #Get reading type and call correct formatting method
    def formatReadings(self,data):
        temp = data.split("\n")
        for i in temp:
            if "uBitTest" in i:
                new = i.split("|")
                if "Event" in new[1]:
                    self.formatEvents(i)
                elif "Data" in new[1]:
                    self.formatData(new[2],new[3])
    #add data reading
    def addData(self,data):
        self.formatReadings(str(data))
        pass

    #add memory usage reading
    def addMemory(self,data):
        self.memory.append(data)

    #add labeled data
    def formatLabeled(self,label,data):
        if label not in self.data:
            self.data[label] = [data]
        else:
            self.data[label].append(data)

    #add output reading
    def addOutput(self,data,code):
        if code in uBitTests.COMPONENTS_NAME_DICT:
            sourceName = uBitTests.COMPONENTS_NAME_DICT[code]
        else:
            sourceName = code
        if sourceName not in self.outputs:
            self.outputs[sourceName] = [str(data)]
        else:
            self.outputs[sourceName].append(str(data))

        pass

    #Add labled data
    def addLabeledData(self,data,label):
        temp = data.split("\n")
        for i in temp:
            if "uBitTest" in i:
                new = i.split("|")
                if "Data" in new[1]:
                    if new[2] == uBitTests.DEVICE_ID_ACCELEROMETER and "," in new[3]:
                        xyz = data.split(",")
                        xyz = [xyz[0],xyz[1],xyz[2]]
                        new[3] = xyz
                        
                    self.formatLabeled(label,new[3])

    #Add error reading
    def addError(self,error):
        self.passed = False
        self.error = error
        pass 

    #Check valid event
    def checkEvent(self,event):
        if event in self.events:
            return True
        return False

    #Init for instance, set all default values, open .txt and json files to write to
    def __init__(self,path):

        self.file = ''

        self.passed = True
        self.path = path

        self.error = ''
        self.size = 0
        self.data = {}
        self.events ={}
        self.outputs= {}
        self.memory = []
        self.timeElapsed = 0

        temp = path.split("/")
        self.testName = temp[len(temp) - 1]
        self.testTime = temp[len(temp) - 2]

        self.dataDict =  [self.file,self.testName,self.testTime,self.timeElapsed ,self.passed,self.error,self.size,self.data,self.events,self.outputs,self.memory]

        self.file = open(path + ".txt",'a+')
        self.jsonFile = open(path + ".json",'w+')
        pass