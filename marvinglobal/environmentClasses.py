
import os
import simplejson as json
from marvinglobal import marvinglobal as mg
from marvinglobal import cartClasses

from dataclasses import dataclass
#from typing import List, Set, Dict, Tuple, Optional


###########################################
# environment data classes
###########################################
@dataclass
class RoomData:
    newRoom:bool = False
    roomName:str = "unknown"
    fullScanDone:bool = False




@dataclass
class Marker:
    markerId:int
    cameraType:int
    cartLocation:mg.Location
    camLocation:mg.Location
    yawInImage:int
    distanceCamToMarker:int
    markerLocation:mg.Location
    markerColor = (255, 255, 0)  # yellow


class MarkerList:

    def __init__(self, fileName):
        self.markerList:list[Marker] = []
        self.fileName = fileName


    def reset(self):
        self.markerList = []
        self.saveMarkerList()


    def addMarker(self, marker:Marker):
        self.markerList.append(marker)
        self.saveMarkerList()


    def loadMarkerList(self):

        if os.path.exists(self.filename):
            with open(self.filename, "r") as read_file:
                markerList = json.load(read_file)


    def saveMarkerList(self):

        with open(self.filename, "w") as write_file:
            json.dump(self.markerList, write_file, indent=2)


    def updateMarkerFoundResult(resultList, camType:mg.CamTypes, cartLocation:mg.Location, camYaw:int):
        """
        :param resultList:      list of partial marker data  {'markerId', 'distanceCamToMarker', 'angleInImage', 'markerYaw'}
        :param camType:         mg.camTypes.EYE_CAM or CART_CAM
        :param cartLocation:    cart location at time of image taken
        :param camDegrees:
        """

        for marker in resultList:

            # complete the partial marker results
            # calculate marker location based on cartLocation, camLocation, distanceCamToMarker and yawInImage
            newMarker.degrees = markerInfo['angleInImage'] + camYaw      # relative to cart yaw
            newMArker.distanceCamToMarker = int(markerInfo['distanceCamToMarker'])
            newMarker.markerLocation.yaw = int(markerInfo['markerYaw'])

            config.log(f"calcMarkerXY, cart: {cartX} / {cartY}, angleFromCart: {degrees}, dist: {distance}")

            xOffset = int(distance * np.cos(np.radians(int(degrees))))
            yOffset = int(distance * np.sin(np.radians(int(degrees))))

            # check whether the marker is already in the list
            appendMarker = False
            existingMarkerInfo = next((item for item in config.markerList if item.markerId == markerId), None)
            if existingMarkerInfo is None:
                appendMarker = True
                config.log(f"new marker found: {markerId}, distance: {distance}")
            else:
                # check for closer observation distance and use only the closest observation
                if existingMarkerInfo.distanceCamToMarker > distance:
                    config.log(f"update marker information because of closer observation point, distance: {distance:.0f}")
                    index = next(i for i, item in enumerate(config.markerList) if item.markerId == markerId)
                    del config.markerList[index]
                    appendMarker = True

            if appendMarker:
                oMarker = config.cMarker()
                oMarker.markerId = markerId
                oMarker.cameraType = camera
                oMarker.cartX = cartX
                oMarker.cartY = cartY
                oMarker.cartDegrees = cartDegrees
                oMarker.camDegrees = camDegrees     # eyecam: head degrees, cartcam = 0
                oMarker.atAngleFromCart = degrees
                oMarker.distanceCamToMarker = distance
                oMarker.markerX = cartX + xOffset
                oMarker.markerY = cartY + yOffset

                # a marker observation with distance > 1500 does not have a very accurate dockMarker.markerYaw value
                # half the value in that case
                if distance > 1500:
                    markerYaw = round(markerYaw/2)

                oMarker.markerYaw = (cartDegrees + camDegrees + 90 + markerYaw + 360) % 360

                config.markerList.append(oMarker)

                config.log(f"marker added: {oMarker.markerId}, X: {oMarker.markerX}, Y: {oMarker.markerY}, degrees: {oMarker.markerYaw}")

        # persist list of markers
        navMap.saveMarkerList()


