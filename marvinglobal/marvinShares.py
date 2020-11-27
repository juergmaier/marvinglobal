
import time
import sys
from multiprocessing.managers import SyncManager
import subprocess
from tenacity import retry, TryAgain, stop_after_delay, wait_fixed

import marvinglobal.marvinglobal as mg
import marvinglobal.usedSharedRessources as usr

class ShareManager(SyncManager): pass

class MarvinShares:

    def __init__(self):

        # register share functions
        mg.log(f"try to connect with marvinData")
        ShareManager.register('getProcessDict')
        ShareManager.register('getArduinoDict')
        ShareManager.register('getServoTypeDict')
        ShareManager.register('getServoStaticDict')
        ShareManager.register('getServoDerivedDict')
        ShareManager.register('getServoCurrentDict')
        ShareManager.register('getCartDict')

        ShareManager.register('getSharedDataUpdateQueue')
        ShareManager.register('getSkeletonGuiUpdateQueue')
        ShareManager.register('getCartGuiUpdateQueue')
        ShareManager.register('getIkUpdateQueue')
        ShareManager.register('getServoRequestQueue')
        ShareManager.register('getCartRequestQueue')
        ShareManager.register('getSpeakRequestQueue')
        ShareManager.register('getSpeakRespondQueue')
        ShareManager.register('getImageProcessingQueue')

        # connect with marviData process
        self.m = ShareManager(address=('127.0.0.1', mg.SHARED_DATA_PORT), authkey=b'marvin')


    @retry(wait=wait_fixed(2), stop=stop_after_delay(10))
    def sharedDataConnect(self, process):


        try:
            self.m.connect()
        except Exception as e:
            mg.log(f"retry to connect, {e}")
            raise TryAgain
        ressourceList = usr.usedSharedRessources[process]

        if 'ProcessDict' in ressourceList:
            try:
                self.processDict = self.m.getProcessDict()

                mg.log(f"processDict available")
            except Exception as e:
                mg.log(f"could not get access to processDict, {e}")
                return False

        if 'ArduinoDict' in ressourceList:
            try:
                self.arduinoDict = self.m.getArduinoDict()
                mg.log(f"arduinoDict available")
            except Exception as e:
                mg.log(f"could not get access to arduinoDict, {e}")
                return False

        if 'ServoTypeDict' in ressourceList:
            try:
                self.servoTypeDict = self.m.getServoTypeDict()
                mg.log(f"servoTypeDict available")
                #mg.log(self.servoTypeDict.get('MG996R').typeMaxPos)
            except Exception as e:
                mg.log(f"could not get access to servoTypeDict, {e}")
                return False

        if 'ServoStaticDict' in ressourceList:
            try:
                self.servoStaticDict = self.m.getServoStaticDict()
                mg.log(f"servoStaticDict available")
            except Exception as e:
                mg.log(f"could not get access to servoStaticDict, {e}")
                return False

        if 'ServoDerivedDict' in ressourceList:
            try:
                self.servoDerivedDict = self.m.getServoDerivedDict()
                mg.log(f"servoDerivedDict available")
            except Exception as e:
                mg.log(f"could not get access to servoDerivedDict, {e}")
                return False

        if 'ServoCurrentDict' in ressourceList:
            try:
                self.servoCurrentDict = self.m.getServoCurrentDict()
                mg.log(f"servoCurrentDict available")
            except Exception as e:
                mg.log(f"could not get access to servoCurrentDict, {e}")
                return False

        if 'CartDict' in ressourceList:
            try:
                self.cartDict = self.m.getCartDict()
                mg.log(f"cartDict available")
            except Exception as e:
                mg.log(f"could not get access to cartDict, {e}")
                return False

        # Queues
        if 'SharedDataUpdateQueue' in ressourceList:
            try:
                self.sharedDataUpdateQueue = self.m.getSharedDataUpdateQueue()
                mg.log(f"sharedDataUpdateQueue available")
            except Exception as e:
                mg.log(f"could not get access to sharedDataUpdateQueue, {e}")
                return False

        if 'SkeletonGuiUpdateQueue' in ressourceList:
            try:
                self.skeletonGuiUpdateQueue = self.m.getSkeletonGuiUpdateQueue()
                mg.log(f"skeletonGuiUpdateQueue available")
            except Exception as e:
                mg.log(f"could not get access to skeletonGuiUpdateQueue, {e}")
                return False

        if 'CartGuiUpdateQueue' in ressourceList:
            try:
                self.cartGuiUpdateQueue = self.m.getCartGuiUpdateQueue()
                mg.log(f"cartGuiUpdateQueue available")
            except Exception as e:
                mg.log(f"could not get access to cartGuiUpdateQueue, {e}")
                return False

        if 'IkUpdateQueue' in ressourceList:
            try:
                self.ikUpdateQueue = self.m.getIkUpdateQueue()
                mg.log(f"ikUpdateQueue available")
            except Exception as e:
                mg.log(f"could not get access to ikUpdateQueue, {e}")
                return False

        if 'ServoRequestQueue' in ressourceList:
            try:
                self.servoRequestQueue = self.m.getServoRequestQueue()
                mg.log(f"servoRequestQueue available")
            except Exception as e:
                mg.log(f"could not get access to servoRequestQueue, {e}")
                return False

        if 'CartRequestQueue' in ressourceList:
            try:
                self.cartRequestQueue = self.m.getCartRequestQueue()
                mg.log(f"cartRequestQueue available")
            except Exception as e:
                mg.log(f"could not get access to cartRequestQueue, {e}")
                return False

        if 'SpeakRequestQueue' in ressourceList:
            try:
                self.speakRequestQueue = self.m.getSpeakRequestQueue()
                mg.log(f"speakRequestQueue available")
            except Exception as e:
                mg.log(f"could not get access to speakRequestQueue, {e}")
                return False

        if 'SpeakRespondQueue' in ressourceList:
            try:
                self.speakRespondQueue = self.m.getSpeakRespondQueue()
                mg.log(f"speakRespondQueue available")
            except Exception as e:
                mg.log(f"could not get access to speakRespondQueue, {e}")
                return False

        if 'ImageProcessingQueue' in ressourceList:
            try:
                self.imageProcessingQueue = self.m.getImageProcessingQueue()
                mg.log(f"imageProcessingQueue available")
            except Exception as e:
                mg.log(f"could not get access to imageProcessingQueue, {e}")
                return False

        return True


    def shutdown(self):
        self.m.join()


    def updateSharedData(self, cmd):
        try:
            # process list gets updated regularly to work as life signal, do not log it
            if cmd[0] != mg.SharedDataItem.PROCESS:
                mg.log(f'sharedDataUpdate {cmd}')
            self.sharedDataUpdateQueue.put(cmd)
            return True
        except Exception as e:
            print(f"connection with shared data lost, {e}")
            return False


    def startProcess(self, processName):
        subprocess.Popen([sys.executable, f"d:/projekte/InMoov/{processName}/{processName}.py"])


    def updateProcessDict(self, processName):
        cmd = (mg.SharedDataItem.PROCESS, processName, {'lastUpdate': time.time()})
        return self.updateSharedData(cmd)


    def removeProcess(self, processName):
        cmd = (mg.SharedDataItem.PROCESS, processName, {'remove': True})
        return self.updateSharedData(cmd)

    def isProcessRunning(self, processName):
        '''
        each process needs to update the shared process list with the last update time
        '''
        if processName in self.processDict.keys():
            # print(f"process {processName} is running, last update {time.time()-self.processDict.get(processName)['lastUpdate']:.2f} s ago")
            return (time.time() - self.processDict.get(processName)['lastUpdate']) < 2
        else:
            # print(f"process {processName} is not running")
            return False
