import numpy as np
import matplotlib.pyplot as plt
from adafruit_rplidar import RPLidar
from adafruit_rplidar import RPLidarException

# Grid constants
GRID_RESOLUTION = 0.1  # Grid cell size in meters
GRID_SIZE = 100  # 100x100 grid
MAP_SIZE = GRID_SIZE * GRID_RESOLUTION  # Physical map size
FREE_SPACE_INCREMENT = -1
OCCUPIED_INCREMENT = 5
MAX_PROB = 100  # Maximum probability for a cell
MIN_PROB = 0  # Minimum probability for a cell
INITIAL_ROBOT_POSE = [GRID_SIZE // 2, GRID_SIZE // 2, 0]  # Start in the center of the grid

'''
# RPLidar setup
PORT_NAME = "COM8"  #Different port when connected to pi
BAUDRATE = 115200
lidar = RPLidar(None, PORT_NAME, BAUDRATE, timeout = 3)

# Lidar variables
max_distance = 0
scan_data = [0] * 360

def get_data():
    for scan in lidar.iter_scans():
        for angle, distance in scan:
            scan_data[min([359, np.floor(angle)])] = (angle, distance)
'''

def process_data(angle, distance):
    theta_obj = angle * np.pi / 180.0 # Convert the angle from degrees to radians
    x_obj = distance * np.cos(theta_obj)
    y_obj = distance * np.sin(theta_obj)
    return x_obj, y_obj, theta_obj

# Convert the local object coordinates 
def obj_to_global(x_obj, y_obj, robot_pose):
    x_robot, y_robot, theta_robot = robot_pose
    x_global = x_robot + (x_obj * np.cos(theta_robot)) - (y_obj * np.sin(theta_robot))
    y_global = y_robot + (x_obj * np.sin(theta_robot)) + (y_obj * np.cos(theta_robot))
    return x_global, y_global

def update_grid(grid, lidar_data, robot_pose):
    for angle, distance in lidar_data:
        if distance > 0:
            # Convert data to local cartesian coordinates
            theta_obj = angle * np.pi / 180.0 # Convert the angle from degrees to radians
            x_obj = distance * np.cos(theta_obj)
            y_obj = distance * np.sin(theta_obj)

            # Convert local (obj) to global cartesian coordinates
            x_global, y_global = obj_to_global(x_obj, y_obj, robot_pose)

            # Convert global to grid coordinates
            grid_x = int(x_global / GRID_RESOLUTION)
            grid_y = int(y_global / GRID_RESOLUTION)

            # Mark free space along the ray (Bresenham's line algorithm)
            x_start, y_start = int(robot_pose[0]), int(robot_pose[1])
            bresenham_line_update(grid, x_start, y_start, grid_x, grid_y, FREE_SPACE_INCREMENT)

            # Mark the end cell as occupied
            if 0 <= grid_x < GRID_SIZE and 0 <= grid_y < GRID_SIZE:
                grid[grid_y, grid_x] = min(grid[grid_y, grid_x] + OCCUPIED_INCREMENT, MAX_PROB)

# Update cells along a ray using Bresenham's line algorithm
def bresenham_line_update(grid_map, x0, y0, x1, y1, increment):
    dx, dy = abs(x1 - x0), abs(y1 - y0)
    sx, sy = 1 if x0 < x1 else -1, 1 if y0 < y1 else -1
    err = dx - dy

    while True:
        if 0 <= x0 < GRID_SIZE and 0 <= y0 < GRID_SIZE:
            grid_map[y0, x0] = max(grid_map[y0, x0] + increment, MIN_PROB)
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy

# Simulate robot movement
def move_robot(robot_pose, dx, dy, dtheta):
    x_robot, y_robot, theta_robot = robot_pose
    x_robot += dx
    y_robot += dy
    theta_robot += dtheta
    return [x_robot, y_robot, theta_robot]

# Simulate LiDAR data (random obstacles)
def simulate_lidar(robot_pose, num_readings=360):
    angles = np.linspace(0, 2 * np.pi, num_readings)
    distances = np.random.uniform(0.5, 3.0, num_readings)  # Random distances
    return list(zip(angles, distances))

# Visualize the grid map and robot
def visualize_map(grid_map, robot_pose):
    plt.imshow(grid_map, cmap='gray', origin='lower')
    plt.plot(robot_pose[0], robot_pose[1], 'ro')  # Plot robot position
    plt.title("Occupancy Grid Map")
    plt.xlabel("X (cells)")
    plt.ylabel("Y (cells)")
    #plt.colorbar(label="Occupancy Probability")
    plt.pause(0.01)


# Main SLAM loop
def run_slam():
    grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=np.int8)
    robot_pose = INITIAL_ROBOT_POSE
    plt.figure()

    for _ in range(100):  # Run for 100 iterations
        lidar_data = simulate_lidar(robot_pose)  # Simulated LiDAR data
        update_grid(grid, lidar_data, robot_pose)  # Update map
        visualize_map(grid, robot_pose)

        # Simulate robot movement (straight line with slight rotation)
        robot_pose = move_robot(robot_pose, dx=1, dy=0, dtheta=0.1)


    plt.show()

# Run the SLAM algorithm
if __name__ == "__main__":
    run_slam()
