import numpy as np
import pygame

from simulator import Robot, Sensor, Graphics
import utils


# +=====================================================================+
# |                         Initialization                             |
# +=====================================================================+

# Initialize the map
MAP_DIMENSIONS = (1300, 660) # 1360x768
gfx = Graphics(MAP_DIMENSIONS, 'images/robot.png', 'images/map.png')

# Initialize the robot
ROBOT_START, closed = gfx.robot_positioning()
ROBOT_WIDTH = 0.1
INITIAL_MOTOR_SPEED = 10000
MAX_MOTOR_SPEED = 20000
WHEEL_RADIUS = 0.04
robot = Robot(initial_position=ROBOT_START,
              width=ROBOT_WIDTH,
              initial_motor_speed=INITIAL_MOTOR_SPEED,
              max_motor_speed=MAX_MOTOR_SPEED,
              wheel_radius=WHEEL_RADIUS)

# Initialize sensors
# TODO: save the robot and sensor positions in a file, so the user doesn't have to do it every time
SENSORS_POSITIONS, closed = gfx.sensors_positioning(ROBOT_START, closed)
sensors = [Sensor(position, ROBOT_START) for position in SENSORS_POSITIONS]

# +=====================================================================+
# |                            Simulation                               |
# +=====================================================================+

last_time = pygame.time.get_ticks()
last_error = 0
I = 0 # PID integral

running = True

while running and not(closed):
        
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
    for sensor in sensors:
        gfx.draw_sensor(sensor)
    
    # Read the sensors
    for idx in range(len(sensors)):
        sensors[idx].read_data(gfx.map_image)
    #
    # Write sensors data on the screen
    gfx.show_sensors_data(sensors)

    # Calculate the elapsed time since the last iteration
    current_time = pygame.time.get_ticks()
    dt = (current_time - last_time)/1000
    last_time = current_time

    # +=====================================================================+
    # |                         Control logic                               |
    # |                                                                     |
    # Calculate the error and write it on the screen
    error = sensors[3].data - sensors[1].data
    gfx.show_text(text=f"Error: "+ str(error),
                    position=(10, 10 + 130))
    
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
    for idx in range(len(sensors)):
        sensors[idx].update_position(robot_position=(robot.x, robot.y, robot.heading),
                            sensor_relative_position=SENSORS_POSITIONS[idx])
    
    # Check if the robot is out of bounds
    robot_is_out = gfx.is_out_of_bounds(robot)
    sensor_is_out = bool(np.sum([gfx.is_out_of_bounds(sensor) for sensor in sensors]))
    #
    # Write error message if robot is out of bounds
    if robot_is_out or sensor_is_out:
            
            gfx.show_out_of_bounds_error()
            
            # Write error message on the screen
            pygame.display.update()
            pygame.time.wait(3500)
            running = False
            
    if running:
        pygame.display.update()
