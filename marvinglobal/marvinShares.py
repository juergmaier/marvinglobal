
import time
import sys
from multiprocessing.managers import SyncManager
import subprocess
from tenacity import retry, TryAgain, stop_after_delay, wait_fixed

from marvinglobal import marvinglobal as mg
from marvinglobal import usedSharedRessources

verbose = False

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
        ShareManager.register('getMainGuiUpdateQueue')
        ShareManager.register('getIkUpdateQueue')
        ShareManager.register('getSkeletonRequestQueue')
        ShareManager.register('getCartRequestQueue')
        ShareManager.register('getSpeakRequestQueue')
        #ShareManager.register('getSpeakResponseQueue')
        ShareManager.register('getNavManagerRequestQueue')
        ShareManager.register('getImageProcessingQueue')
        ShareManager.register('getPlayGestureQueue')

        # connect with marviData process
        self.m = ShareManager(address=('127.0.0.1', mg.SHARED_DATA_PORT), authkey=b'marvin')


    @retry(wait=wait_fixed(2), stop=stop_after_delay(10))
    def sharedDataConnect(self, process):


        try:
            self.m.connect()
        except Exception as e:
            mg.log(f"retry to connect, {e}")
            raise TryAgain
        ressourceList = usedSharedRessources.usedSharedRessources[process]

        mg.log(f"{process}, {ressourceList}")

        if 'ProcessDict' in ressourceList:
            if verbose: mg.log(f"try to connect with processDict")
            try:
                self.processDict = self.m.getProcessDict()
                mg.log(f"processDict available")
            except Exception as e:
                mg.log(f"could not get access to processDict, {e}")
                return False

        if 'ArduinoDict' in ressourceList:
            if verbose: mg.log(f"try to connect with arduinoDict")
            try:
                self.arduinoDict = self.m.getArduinoDict()
                mg.log(f"arduinoDict available")
            except Exception as e:
                mg.log(f"could not get access to arduinoDict, {e}")
                return False

        if 'ServoTypeDict' in ressourceList:
            if verbose: mg.log(f"try to connect with servoTypeDict")
            try:
                self.servoTypeDict = self.m.getServoTypeDict()
                mg.log(f"servoTypeDict available")
                #mg.log(self.servoTypeDict.get('MG996R').typeMaxPos)
            except Exception as e:
                mg.log(f"could not get access to servoTypeDict, {e}")
                return False

        if 'ServoStaticDict' in ressourceList:
            if verbose: mg.log(f"try to connect with servoStaticDict")
            try:
                self.servoStaticDict = self.m.getServoStaticDict()
                mg.log(f"servoStaticDict available")
            except Exception as e:
                mg.log(f"could not get access to servoStaticDict, {e}")
                return False

        if 'ServoDerivedDict' in ressourceList:
            if verbose: mg.log(f"try to connect with servoDerivedDict")
            try:
                self.servoDerivedDict = self.m.getServoDerivedDict()
                mg.log(f"servoDerivedDict available")
            except Exception as e:
                mg.log(f"could not get access to servoDerivedDict, {e}")
                return False

        if 'ServoCurrentDict' in ressourceList:
            if verbose: mg.log(f"try to connect with servoCurrentDict")
            try:
                self.servoCurrentDict = self.m.getServoCurrentDict()
                mg.log(f"servoCurrentDict available")
            except Exception as e:
                mg.log(f"could not get access to servoCurrentDict, {e}")
                return False

        if 'CartDict' in ressourceList:
            if verbose: mg.log(f"try to connect with cartDict")
            try:
                self.cartDict = self.m.getCartDict()
                mg.log(f"cartDict available")
            except Exception as e:
                mg.log(f"could not get access to cartDict, {e}")
                return False

        # Queues
        if 'SharedDataUpdateQueue' in ressourceList:
            if verbose: mg.log(f"try to connect with sharedDataUpdateQueue")
            try:
                self.sharedDataUpdateQueue = self.m.getSharedDataUpdateQueue()
                mg.log(f"sharedDataUpdateQueue available")
            except Exception as e:
                mg.log(f"could not get access to sharedDataUpdateQueue, {e}")
                return False

        if 'SkeletonGuiUpdateQueue' in ressourceList:
            if verbose: mg.log(f"try to connect with skeletonGuiUpdateQueue")
            try:
                self.skeletonGuiUpdateQueue = self.m.getSkeletonGuiUpdateQueue()
                mg.log(f"skeletonGuiUpdateQueue available")
            except Exception as e:
                mg.log(f"could not get access to skeletonGuiUpdateQueue, {e}")
                return False

        if 'CartGuiUpdateQueue' in ressourceList:
            if verbose: mg.log(f"try to connect with cartGuiUpdateQueue")
            try:
                self.cartGuiUpdateQueue = self.m.getCartGuiUpdateQueue()
                mg.log(f"cartGuiUpdateQueue available")
            except Exception as e:
                mg.log(f"could not get access to cartGuiUpdateQueue, {e}")
                return False

        if 'MainGuiUpdateQueue' in ressourceList:
            if verbose: mg.log(f"try to connect with mainGuiUpdateQueue")
            try:
                self.mainGuiUpdateQueue = self.m.getMainGuiUpdateQueue()
                mg.log(f"mainGuiUpdateQueue available")
            except Exception as e:
                mg.log(f"could not get access to mainGuiUpdateQueue, {e}")
                return False

        if 'IkUpdateQueue' in ressourceList:
            if verbose: mg.log(f"try to connect with ikUpdateQueue")
            try:
                self.ikUpdateQueue = self.m.getIkUpdateQueue()
                mg.log(f"ikUpdateQueue available")
            except Exception as e:
                mg.log(f"could not get access to ikUpdateQueue, {e}")
                return False

        if 'SkeletonRequestQueue' in ressourceList:
            if verbose: mg.log(f"try to connect with SkeletonRequestQueue")
            try:
                self.skeletonRequestQueue = self.m.getSkeletonRequestQueue()
                mg.log(f"SkeletonRequestQueue available")
            except Exception as e:
                mg.log(f"could not get access to SkeletonRequestQueue, {e}")
                return False

        if 'CartRequestQueue' in ressourceList:
            if verbose: mg.log(f"try to connect with CartRequestQueue")
            try:
                self.cartRequestQueue = self.m.getCartRequestQueue()
                mg.log(f"CartRequestQueue available")
            except Exception as e:
                mg.log(f"could not get access to CartRequestQueue, {e}")
                return False

        if 'SpeakRequestQueue' in ressourceList:
            if verbose: mg.log(f"try to connect with speakRequestQueue")
            try:
                self.speakRequestQueue = self.m.getSpeakRequestQueue()
                mg.log(f"speakRequestQueue available")
            except Exception as e:
                mg.log(f"could not get access to speakRequestQueue, {e}")
                return False

        if 'NavManagerRequestQueue' in ressourceList:
            if verbose: mg.log(f"try to connect with navManagerRequestQueue")
            try:
                self.navManagerRequestQueue = self.m.getNavManagerRequestQueue()
                mg.log(f"navManagerRequestQueue available")
            except Exception as e:
                mg.log(f"could not get access to navManagerRequestQueue, {e}")
                return False

        if 'ImageProcessingQueue' in ressourceList:
            if verbose: mg.log(f"try to connect with imageProcessingQueue")
            try:
                self.imageProcessingQueue = self.m.getImageProcessingQueue()
                mg.log(f"imageProcessingQueue available")
            except Exception as e:
                mg.log(f"could not get access to imageProcessingQueue, {e}")
                return False

        if 'PlayGestureQueue' in ressourceList:
            if verbose: mg.log(f"try to connect with playGestureQueue")
            try:
                self.playGestureQueue = self.m.getPlayGestureQueue()
                mg.log(f"playGestureQueue available")
            except Exception as e:
                mg.log(f"could not get access to playGestureQueue, {e}")
                return False

        return True


    def shutdown(self):
        self.m.join()


    def updateSharedData(self, msg):
        try:
            # process list gets updated regularly to work as life signal, do not log it
            #if cmd[0] != mg.SharedDataItem.PROCESS:
            if msg['cmd'] in mg.logDataUpdates:
                mg.log(f'sharedDataUpdate {msg}')
            self.sharedDataUpdateQueue.put(msg)
            return True
        except Exception as e:
            print(f"connection with shared data lost, {e}")
            return False


    def startProcess(self, processName):
        subprocess.Popen([sys.executable, f"d:/projekte/InMoov/{processName}/{processName}.py"])


    def updateProcessDict(self, processName):
        #cmd = (mg.SharedDataItem.PROCESS, processName, {'lastUpdate': time.time()})
        msg = {'cmd': mg.SharedDataItem.PROCESS, 'sender': processName,
               'info': {'processName': processName, 'running': True, 'lastUpdate': time.time()}}
        return self.updateSharedData(msg)


    def removeProcess(self, processName):
        #cmd = (mg.SharedDataItem.PROCESS, processName, {'remove': True})
        msg = {'cmd': mg.SharedDataItem.PROCESS, 'sender': processName,
               'info': {'processName': processName, 'remove': True}}
        return self.updateSharedData(msg)

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

