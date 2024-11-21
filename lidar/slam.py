'''Modified version of rpslam.py from BreezySLAM/examples to use the adafruit rplidar library instead'''

MAP_SIZE_PIXELS = 500
MAP_SIZE_METERS = 10
PORT_NAME = '/dev/ttyUSB1'
BAUDRATE = 115200
MIN_SAMPLES = 200

from math import floor

from breezyslam.algorithms import RMHC_SLAM
from breezyslam.sensors import RPLidarA1 as LaserModel
from adafruit_rplidar import RPLidar
from roboviz import MapVisualizer

if __name__ == '__main__':
    
    # Setup the RPLidar
    lidar = RPLidar(None, PORT_NAME, BAUDRATE,timeout = 3)

    # Create an RMHC SLAM object with a laser model and optional robot model
    slam = RMHC_SLAM(LaserModel(), MAP_SIZE_PIXELS, MAP_SIZE_METERS)

    # Initialize an empty trajectory
    trajectory = []

    # Create an iterator to collect scan data from the RPLidar
    scans = lidar.iter_scans()

    # We will use these to store previous scan in case current scan is inadequate
    previous_distances = None
    previous_angles    = None
    
    # First scan is crap, so ignore it
    #next(scans)

    while True:
        items = [item for item in scans]
        
        # Extract (quality, angle, distance) triples from current scan
        angles = [item[1] for item in items]
        distances = [item[2] for item in items]
        
        # Update SLAM with current Lidar scan and scan angles if adequate
        if len(distances) > MIN_SAMPLES:
            slam.update(distances, scan_angles_degrees = angles)
            previous_distances = distances.copy()
            previous_angles = angles.copy()
            
        # If not adequate, us previous
        elif previous_distances is not None:
            slam.update(previous_distances, scan_angles_degrees = previous_angles)
            
        # Get current robot position
        x, y, theta = slam.getpos()
        
        print("x:", x, "y:", y, "theta:", theta)
        
    # Shut down the lidar connection
    lidar.stop()
    lidar.stop_motor()
    lidar.disconnect()
