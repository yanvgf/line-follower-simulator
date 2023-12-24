import numpy as np

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

