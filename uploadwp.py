from dronekit import connect
from dronekit import Command
from dronekit import LocationGlobal
from dronekit import Locations
from dronekit import Vehicle
from dronekit import VehicleMode
from pymavlink import mavutil

connected = False

    
num = int(input("Number of coordinates to enter: ")) #ask user for number of coordinates in the mission

lat = [] #array of latitude
lon = [] #array of longitude

for i in range(num): #this for loop has users enter the long/lat of the coordinate in WGS84
        coordNum = i + 1
        lat.append(float(input("Enter latitude of Coordinate " + str(coordNum) + "(WGS84): ")))
        lon.append(float(input("Enter longitude of Coordinate " + str(coordNum) + "(WGS84): ")))

for i in range(128):  #this loop searches for a baton
    if connected == False:
        port = 'COM' + str(i)
        try:
            baton = connect(port, wait_ready=True, baud=9600)
            connected = True
        except:
            connected = False

if connected == True: # if a baton is found, upload the coordinates
    uploaded = False
    print("Baton found on port " + port)
    
    
    cmds = baton.commands 
    cmds.download() #sync existing commands
    cmds.wait_ready() #wait til baton ready
    cmds.clear() #clear existing commands
    
    
    baton.home_location  = baton.location.global_frame #set home location to current location
    print("Home location set!")
    
    for i in range(num): #add commands to the list defined earlier
        cmds.add(Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_TERRAIN_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, lat[i], lon[i], 30))
    
    try:
        cmds.upload() #upload commands
        print("Mission uploaded successfully!")
        uploaded = True
    except:
        print("Mission failed to upload")
        
    if uploaded == True: 
        baton.mode = VehicleMode('THROW')
        baton.armed = True
        print("Baton is ready to deploy")
     
else:
    print("Baton not found!")
