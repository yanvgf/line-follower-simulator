import numpy as np
import pygame

from classes import Robot, Graphics
import utils


# +=====================================================================+
# |                         Initialization                             |
# +=====================================================================+

# Read the setup file
setup_info = utils.read_setup_file()
#
ROBOT_WIDTH = setup_info[0]
INITIAL_MOTOR_SPEED = setup_info[1]
MAX_MOTOR_SPEED = setup_info[2]
WHEEL_RADIUS = setup_info[3]
SENSORS_NUMBER = setup_info[4]
MAP_DIMENSIONS = setup_info[5]
ROBOT_START = setup_info[6]
SENSORS_POSITIONS = setup_info[7]
SENSOR_COLORS = setup_info[8]

# Initialize the map
gfx = Graphics(MAP_DIMENSIONS, 'images/robot.png', 'images/map.png')

# Initialize the robot
robot = Robot(initial_position=ROBOT_START,
              width=ROBOT_WIDTH,
              initial_motor_speed=INITIAL_MOTOR_SPEED,
              max_motor_speed=MAX_MOTOR_SPEED,
              wheel_radius=WHEEL_RADIUS)

# Initialize sensors
for position in SENSORS_POSITIONS:
    robot.add_sensor(position, ROBOT_START)

# +=====================================================================+
# |                            Simulation                               |
# +=====================================================================+

last_time = pygame.time.get_ticks()
last_error = 0
I = 0 # PID integral

running = True

while running:
        
    # Check if the user closed the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Draw map
    gfx.map.blit(gfx.map_image, (0, 0))
    #
    # Draw the robot
    gfx.draw_robot(robot.x, robot.y, robot.heading)
    #
    # Draw the sensors
    for sensor in robot.sensors:
        gfx.draw_sensor(sensor, color=SENSOR_COLORS[robot.sensors.index(sensor)])
    
    # Read the sensors
    for idx in range(len(robot.sensors)):
        robot.sensors[idx].read_data(gfx.map_image)
    #
    # Write sensors data on the screen
    gfx.show_sensors_data(robot.sensors, sensor_colors=SENSOR_COLORS[:SENSORS_NUMBER])

    # Calculate the elapsed time since the last iteration
    current_time = pygame.time.get_ticks()
    dt = (current_time - last_time)/1000
    last_time = current_time

    # +=====================================================================+
    # |                         Control logic                               |
    # |                                                                     |
    # Calculate the error
    error =  robot.sensors[1].data - robot.sensors[3].data
    
    # Calculate PID
    pid, I = utils.PID(kp=50, ki=3, kd=0.01, I=I,
                    error=error, last_error=last_error, dt=dt)
    
    # Update the previous error
    last_error = error
    
    # Update motors speed based on the controller
    robot.left_motor.set_speed(robot.left_motor.max_motor_speed + pid)
    robot.right_motor.set_speed(robot.right_motor.max_motor_speed - pid)
    # |                                                                     |
    # |                                                                     |
    # +=====================================================================+
    
    # Update robot position
    robot.update_position(dt)
    
    # Update sensors position
    for idx in range(len(robot.sensors)):
        robot.sensors[idx].update_position(robot_position=(robot.x, robot.y, robot.heading),
                            sensor_relative_position=SENSORS_POSITIONS[idx])
    
    # Check if the robot is out of bounds
    robot_is_out = gfx.is_out_of_bounds(robot)
    sensor_is_out = bool(np.sum([gfx.is_out_of_bounds(sensor) for sensor in robot.sensors]))
    #
    # Write error message if robot is out of bounds
    if robot_is_out or sensor_is_out:
            
            gfx.show_important_message("The robot went off the map!")
            
            # Write error message on the screen
            pygame.display.update()
            pygame.time.wait(3500)
            running = False
            
    if running:
        pygame.display.update()
