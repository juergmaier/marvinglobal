
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
        ShareManager.register('getServoDict')
        ShareManager.register('getCartDict')
        ShareManager.register('getEnvironmentDict')

        ShareManager.register('getSharedDataUpdateQueue')
        ShareManager.register('getSkeletonGuiUpdateQueue')
        ShareManager.register('getCartGuiUpdateQueue')
        ShareManager.register('getMapGuiUpdateQueue')
        ShareManager.register('getMainGuiUpdateQueue')
        ShareManager.register('getIkUpdateQueue')
        ShareManager.register('getSkeletonRequestQueue')
        ShareManager.register('getCartRequestQueue')
        ShareManager.register('getSpeakRequestQueue')
        ShareManager.register('getImageProcessingRequestQueue')
        ShareManager.register('getPlayGestureQueue')
        ShareManager.register('getNavManagerRequestQueue')

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

        if 'processDict' in ressourceList:
            if verbose: mg.log(f"try to connect with processDict")
            try:
                self.processDict = self.m.getProcessDict()
                mg.log(f"processDict available")
            except Exception as e:
                mg.log(f"could not get access to processDict, {e}")
                return False

        if 'arduinoDict' in ressourceList:
            if verbose: mg.log(f"try to connect with arduinoDict")
            try:
                self.arduinoDict = self.m.getArduinoDict()
                mg.log(f"arduinoDict available")
            except Exception as e:
                mg.log(f"could not get access to arduinoDict, {e}")
                return False

        if 'servoDict' in ressourceList:
            if verbose: mg.log(f"try to connect with servoDict")
            try:
                self.servoDict = self.m.getServoDict()
                mg.log(f"servoDict available")
                #mg.log(self.servoTypeDict.get('MG996R').typeMaxPos)
            except Exception as e:
                mg.log(f"could not get access to servoDict, {e}")
                return False

        if 'cartDict' in ressourceList:
            if verbose: mg.log(f"try to connect with cartDict")
            try:
                self.cartDict = self.m.getCartDict()
                mg.log(f"cartDict available")
            except Exception as e:
                mg.log(f"could not get access to cartDict, {e}")
                return False

        if 'environmentDict' in ressourceList:
            if verbose: mg.log(f"try to connect with EnvironemntDict")
            try:
                self.environmentDict = self.m.getEnvironmentDict()
                mg.log(f"environmentDict available")
            except Exception as e:
                mg.log(f"could not get access to environmentDict, {e}")
                return False

        # Queues
        if 'sharedDataUpdateQueue' in ressourceList:
            if verbose: mg.log(f"try to connect with sharedDataUpdateQueue")
            try:
                self.sharedDataUpdateQueue = self.m.getSharedDataUpdateQueue()
                mg.log(f"sharedDataUpdateQueue available")
            except Exception as e:
                mg.log(f"could not get access to sharedDataUpdateQueue, {e}")
                return False

        if 'skeletonGuiUpdateQueue' in ressourceList:
            if verbose: mg.log(f"try to connect with skeletonGuiUpdateQueue")
            try:
                self.skeletonGuiUpdateQueue = self.m.getSkeletonGuiUpdateQueue()
                mg.log(f"skeletonGuiUpdateQueue available")
            except Exception as e:
                mg.log(f"could not get access to skeletonGuiUpdateQueue, {e}")
                return False

        if 'cartGuiUpdateQueue' in ressourceList:
            if verbose: mg.log(f"try to connect with cartGuiUpdateQueue")
            try:
                self.cartGuiUpdateQueue = self.m.getCartGuiUpdateQueue()
                mg.log(f"cartGuiUpdateQueue available")
            except Exception as e:
                mg.log(f"could not get access to cartGuiUpdateQueue, {e}")
                return False

        if 'mapGuiUpdateQueue' in ressourceList:
            if verbose: mg.log(f"try to connect with mapGuiUpdateQueue")
            try:
                self.mapGuiUpdateQueue = self.m.getMapGuiUpdateQueue()
                mg.log(f"mapGuiUpdateQueue available")
            except Exception as e:
                mg.log(f"could not get access to mapGuiUpdateQueue, {e}")
                return False


        if 'mainGuiUpdateQueue' in ressourceList:
            if verbose: mg.log(f"try to connect with mainGuiUpdateQueue")
            try:
                self.mainGuiUpdateQueue = self.m.getMainGuiUpdateQueue()
                mg.log(f"mainGuiUpdateQueue available")
            except Exception as e:
                mg.log(f"could not get access to mainGuiUpdateQueue, {e}")
                return False

        if 'ikUpdateQueue' in ressourceList:
            if verbose: mg.log(f"try to connect with ikUpdateQueue")
            try:
                self.ikUpdateQueue = self.m.getIkUpdateQueue()
                mg.log(f"ikUpdateQueue available")
            except Exception as e:
                mg.log(f"could not get access to ikUpdateQueue, {e}")
                return False

        if 'skeletonRequestQueue' in ressourceList:
            if verbose: mg.log(f"try to connect with SkeletonRequestQueue")
            try:
                self.skeletonRequestQueue = self.m.getSkeletonRequestQueue()
                mg.log(f"SkeletonRequestQueue available")
            except Exception as e:
                mg.log(f"could not get access to SkeletonRequestQueue, {e}")
                return False

        if 'cartRequestQueue' in ressourceList:
            if verbose: mg.log(f"try to connect with CartRequestQueue")
            try:
                self.cartRequestQueue = self.m.getCartRequestQueue()
                mg.log(f"CartRequestQueue available")
            except Exception as e:
                mg.log(f"could not get access to CartRequestQueue, {e}")
                return False

        if 'speakRequestQueue' in ressourceList:
            if verbose: mg.log(f"try to connect with speakRequestQueue")
            try:
                self.speakRequestQueue = self.m.getSpeakRequestQueue()
                mg.log(f"speakRequestQueue available")
            except Exception as e:
                mg.log(f"could not get access to speakRequestQueue, {e}")
                return False

        if 'navManagerRequestQueue' in ressourceList:
            if verbose: mg.log(f"try to connect with navManagerRequestQueue")
            try:
                self.navManagerRequestQueue = self.m.getNavManagerRequestQueue()
                mg.log(f"navManagerRequestQueue available")
            except Exception as e:
                mg.log(f"could not get access to navManagerRequestQueue, {e}")
                return False

        if 'imageProcessingRequestQueue' in ressourceList:
            if verbose: mg.log(f"try to connect with imageProcessingRequestQueue")
            try:
                self.imageProcessingRequestQueue = self.m.getImageProcessingRequestQueue()
                mg.log(f"imageProcessingRequestQueue available")
            except Exception as e:
                mg.log(f"could not get access to imageProcessingRequestQueue, {e}")
                return False

        if 'playGestureQueue' in ressourceList:
            if verbose: mg.log(f"try to connect with playGestureQueue")
            try:
                self.playGestureQueue = self.m.getPlayGestureQueue()
                mg.log(f"playGestureQueue available")
            except Exception as e:
                mg.log(f"could not get access to PlayGestureQueue, {e}")
                return False

        if 'navManagerRequestQueue' in ressourceList:
            if verbose: mg.log(f"try to connect with NavManagerRequestQueue")
            try:
                self.navManagerRequestQueue = self.m.getNavManagerRequestQueue()
                mg.log(f"NavManagerRequestQueue available")
            except Exception as e:
                mg.log(f"could not get access to NavManagerRequestQueue, {e}")
                return False

        return True


    def shutdown(self):
        self.m.join()


    def updateSharedData(self, msg):
        try:
            # process list gets updated regularly to work as life signal, do not log it
            #if cmd[0] != mg.SharedDataItems.PROCESS:
            if msg['msgType'] in mg.logDataUpdates:
                mg.log(f'sharedDataUpdate {msg}')
            self.sharedDataUpdateQueue.put(msg)
            return True
        except Exception as e:
            print(f"connection with shared data lost, {e}")
            return False


    def startProcess(self, processName):
        pyVersion = "py39"
        pyExec = "python3.9"
        if processName == "imageProcessing":
            pyVersion = "py37"
            pyExec = "python3.7"
        #executable = f"{mg.INMOOV_BASE_FOLDER}/batchStarter/{processName}.sh"
        pythonPath = f"/home/marvin/miniconda3/envs/{pyVersion}/bin/{pyExec}"
        processPath = f"/home/marvin/InMoov/{processName}/{processName}.py"
        print(f"starting process {pythonPath}, {processPath}")
        executable = f"{pythonPath} {processPath}"
        try:
            subprocess.Popen([sys.executable, processPath], shell=True)
        except Exception as e:
            print(f"could not start process: {processPath}, {e}")

    def startAllProcesses(self):
        processList =  ['marvinGui'] #, 'skeletonControl', 'cartControl', 'speechControl', 'imageProcessing']
        for processName in processList:
            self.startProcess(processName)


    def updateProcessDict(self, processName):
        #cmd = (mg.SharedDataItems.PROCESS, processName, {'lastUpdate': time.time()})
        msg = {'msgType': mg.SharedDataItems.PROCESS, 'sender': processName,
               'info': {'processName': processName, 'running': True, 'lastUpdate': time.time()}}
        return self.updateSharedData(msg)


    def removeProcess(self, processName):
        #cmd = (mg.SharedDataItems.PROCESS, processName, {'remove': True})
        msg = {'msgType': mg.SharedDataItems.PROCESS, 'sender': processName,
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

