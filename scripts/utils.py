import numpy as np
import os

def PID(kp, ki, kd, I,
        error, last_error, dt):
    """PID control.

    Args:
        kp (float): proportional gain.
        ki (float): integral gain.
        kd (float): derivative gain.
        I (float): previous value of the integral part.
        error (float): current system error.
        last_error (float): previous system error.
        dt (float): elapsed time since the last iteration.

    Returns:
        float: PID control value.
        float: new value of the integral part.
    """
    
    # Avoids error in the PID calculation in the first iteration
    if dt == 0:
        dt+=1e-5
    
    P = kp*error
    D = kd*(error - last_error)/dt
    I += ki*error*dt
 
    return P + D + I, I

def rotate_vector(vector, angle):
    """Rotates a vector in an angle.
    
    Args:
        vector (tuple): vector to be rotated (x, y).
        angle (float): rotation angle, in radians.
        
    Returns:
        tuple: rotated vector (x, y).
    """
    
    # Rotation matrix
    rotation_matrix = np.array([[np.cos(angle), -np.sin(angle)],
                                [np.sin(angle), np.cos(angle)]])
    
    # Multiply the vector by the rotation matrix
    rotated_vector = rotation_matrix.dot(vector)
    
    return rotated_vector

def is_darker(color1, color2):
    """Checks if color1 is darker than color2.
    
    Args:
        color1, color2 (tuple): Colors in RGB format (R, G, B).
        
    Returns:
        bool: True if color1 is darker than color2, False otherwise.
    """
    # Calculates the average of the RGB values of each color (grayscale)
    gray1 = sum(color1) / len(color1)
    gray2 = sum(color2) / len(color2)
    
    return gray1 < gray2

def write_setup_file(setup_info):
    """Writes the setup.txt file.
    
    Args:
        setup_info (str): Setup information.
    """
    
    if os.path.isfile('setup.txt'):
        # There is a setup.txt file already
        with open('setup.txt', 'w') as file:
            pass # Erases the file content
        with open('setup.txt', 'w') as file:
            file.write(setup_info) # Writes new content
    else:
        # There is no setup.txt file yet
        with open('setup.txt', 'w') as file:
            file.write(setup_info)

def read_setup_file():
    """Reads the setup.txt file and returns the robot parameters.
    
    Returns:
        tuple: Robot parameters: ROBOT_WIDTH, INITIAL_MOTOR_SPEED, MAX_MOTOR_SPEED, WHEEL_RADIUS, SENSORS_NUMBER, MAP_DIMENSIONS, ROBOT_START, SENSORS_POSITIONS, SENSOR_COLORS.
    """
    
    with open('setup.txt', 'r') as file:
        # Read the file content
        content = file.read()
        
        # Split the content in lines
        lines = content.split('\n')
        
        # Read the robot parameters
        ROBOT_WIDTH = float(lines[0])
        INITIAL_MOTOR_SPEED = int(lines[1])
        MAX_MOTOR_SPEED = int(lines[2])
        WHEEL_RADIUS = float(lines[3])
        SENSORS_NUMBER = int(lines[4])
        MAP_DIMENSIONS = eval(lines[5])
        ROBOT_START = eval(lines[6])
        SENSORS_POSITIONS = eval(lines[7])
        SENSOR_COLORS = eval(lines[8])
        
        return ROBOT_WIDTH, INITIAL_MOTOR_SPEED, MAX_MOTOR_SPEED, WHEEL_RADIUS, SENSORS_NUMBER, MAP_DIMENSIONS, ROBOT_START, SENSORS_POSITIONS, SENSOR_COLORS