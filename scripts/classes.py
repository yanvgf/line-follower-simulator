import numpy as np
import pygame
import utils



# +===========================================================================+
# |                     Robot class (and related classes)                     |                              |
# +===========================================================================+

class Motor:
    """Robot motor. Composes the Robot class."""
    
    def __init__(self, max_motor_speed, wheel_radius):
        """Motor class constructor. Determines the maximum speed and wheel radius.
        
        Args:
            max_motor_speed (float): maximum motor speed, in rpm.
            wheel_radius (float): wheel radius, in meters.
        """
    
        self.max_motor_speed = max_motor_speed
        self.wheel_radius = wheel_radius
    
    def set_speed(self, speed):
        """Sets the motor speed.
        
        Args:
            speed (float): motor speed, in rpm.
        """
        
        self.speed = speed


class Sensor:
    """Line sensor. Composes the Robot class."""
    
    def __init__(self, sensor_relative_position, robot_initial_position):
        """Sensor class constructor. Positions the sensor relative to the robot's initial position.
        
        Args:
            sensor_relative_position (tuple): sensor position (x, y) relative to the robot, in meters.
            robot_initial_position (tuple): robot initial position (x, y, heading), in meters and radians.
        """
        
        # Rotates the sensor position vector according to the robot's angle
        sensor_position_rotated = utils.rotate_vector(sensor_relative_position, robot_initial_position[2])
        
        # Adds the relative position vector (rotated) to the robot's initial position
        self.x = robot_initial_position[0] + sensor_position_rotated[0] 
        self.y = robot_initial_position[1] - sensor_position_rotated[1] # y-axis is inverted
        
    def update_position(self, sensor_relative_position, robot_position):
        """Updates the sensor's position according to the robot's position.
        
        Args:
            robot_position (tuple): robot current position (x, y, heading), in meters and radians.
        """
        # Rotates the sensor's relative position vector according to the robot's angle
        sensor_position_rotated = utils.rotate_vector(sensor_relative_position, robot_position[2])
        
        # Adds the relative position vector to the robot's position to obtain the sensor's real position
        self.x = robot_position[0] + sensor_position_rotated[0] 
        self.y = robot_position[1] - sensor_position_rotated[1] # y-axis is inverted
    
    def read_data(self, map_image):
        """Reads the sensor data. The sensor returns 0 if it reads a dark color and 1 if it reads a light color.
        
        Args:
            map_image (pygame.Surface): arena image.
        """
        
        # Sensor reads the color of the arena pixel at the sensor position
        color = map_image.get_at((int(self.x), int(self.y)))[:-1]
        
        # Returns 1 if the color is lighter than medium gray and 0 otherwise.
        self.data = 0 if utils.is_darker(color, (255/2, 255/2, 255/2)) else 1
  
  
class Robot:
    """Differential robot model. Composed by the Motor class and the Sensor class."""
    
    def __init__(self, initial_position, width, 
                 initial_motor_speed=500, max_motor_speed=1000, wheel_radius=0.04):
        """Robot class constructor. Initializes the robot's position and speed.

        Args:
            initial_position (tuple): robot initial position (x, y, heading), where "x" and "y" \
                are the robot's coordinates in meters and "heading" is the angle in radians.
            width (float): robot width, in meters.
            initial_motor_speed (float, optional): initial motor speed, in rpm. \
                Defaults to 500.
            max_motor_speed (float, optional): maximum motor speed, in rpm. \
                Defaults to 1000.
            wheel_radius (float, optional): wheel radius, in meters. Defaults to 0.04.
        """
        
        # List of the robot sensors
        self.sensors = []
        
        # Scale factor from meters to pixels
        self.meters_to_pixels = 3779.52
        
        # Robot dimensions
        self.width = width
        
        # Robot initial position
        self.x = initial_position[0]
        self.y = initial_position[1]
        self.heading = initial_position[2]
        
        # Motor construction
        self.left_motor = Motor(max_motor_speed, wheel_radius)
        self.right_motor = Motor(max_motor_speed, wheel_radius)
        
        # Initial motor speed
        self.left_motor.set_speed(initial_motor_speed)
        self.right_motor.set_speed(initial_motor_speed)
        
    def update_position(self, dt):
        """Updates the robot's position according to the wheel speeds.
        
        Args:
            dt (float): time elapsed since the last iteration, in seconds."""
        
        # Linear wheel speeds
        left_wheel_linear_speed = 2*np.pi*self.left_motor.wheel_radius*self.left_motor.speed/60
        right_wheel_linear_speed = 2*np.pi*self.right_motor.wheel_radius*self.right_motor.speed/60
        
        # Differential movement
        #
        # Horizontal, vertical and angular movement speeds
        x_speed = (left_wheel_linear_speed + right_wheel_linear_speed)*np.cos(self.heading)/2
        y_speed = (left_wheel_linear_speed + right_wheel_linear_speed)*np.sin(self.heading)/2
        heading_speed = (right_wheel_linear_speed - left_wheel_linear_speed)/self.width
        #
        # Update position and angle according to the elapsed time
        self.x += x_speed*dt
        self.y -= y_speed*dt # y-axis is inverted
        self.heading += heading_speed*dt
        
        # Adjust the angle to the interval [-2pi, 2pi]
        if (self.heading > 2*np.pi) or (self.heading < -2*np.pi):
            self.heading = 0
        
    def move_forward(self):
        """Moves the robot forward at maximum speed."""
        self.left_motor.set_speed(self.left_motor.max_motor_speed)
        self.right_motor.set_speed(self.right_motor.max_motor_speed)
        
    def move_backward(self):
        """Moves the robot backward at maximum speed."""
        self.left_motor.set_speed(-self.left_motor.max_motor_speed)
        self.right_motor.set_speed(-self.right_motor.max_motor_speed)
        
    def turn_left(self):
        """Turns the robot left at maximum speed."""
        self.left_motor.set_speed(-self.left_motor.max_motor_speed)
        self.right_motor.set_speed(self.right_motor.max_motor_speed)
        
    def turn_right(self):
        """Turns the robot right at maximum speed."""
        self.left_motor.set_speed(self.left_motor.max_motor_speed)
        self.right_motor.set_speed(-self.right_motor.max_motor_speed)
    
    def stop(self):
        """Stops the robot."""
        self.left_motor.set_speed(0)
        self.right_motor.set_speed(0)
    
    def add_sensor(self, sensor_relative_position, robot_initial_position):
        """Adds a sensor to the robot.
        
        Args:
            sensor (Sensor): sensor to be added.
        """
        self.sensors.append(Sensor(sensor_relative_position, robot_initial_position))
        
        

# +===========================================================================+
# |                               Graphics class                              |
# +===========================================================================+

class Graphics:
    """Robot and arena graphics."""
    
    def __init__(self, screen_dimensions, robot_image_path, map_imape_path):
        """Graphics class constructor. Initializes the window and loads the images needed.
        
        Args:
            screen_dimensions (tuple): window dimensions (width, height), in pixels.
            robot_image_path (str): robot image path.
            map_imape_path (str): arena image path.
        """
        
        pygame.init()
        
        # Loads the images and adjusts the map to the screen size
        self.robot_image = pygame.image.load(robot_image_path)
        self.map_image = pygame.transform.scale(pygame.image.load(map_imape_path), screen_dimensions)
    
        # Creates the window 
        pygame.display.set_caption("Line Follower Simulator")
        self.map = pygame.display.set_mode(screen_dimensions)
    
        # Draws the arena
        self.map.blit(self.map_image, (0, 0))
    
    def robot_positioning(self):
        """Positions the robot according to the user's mouse click.
            
        Returns:
            tuple: robot initial position (x, y, heading).
            bool: True if the user closed the window, False otherwise.
        """

        running = True
        closed = False
        robot_start_heading = np.pi/2
        xy_positioned = False
        heading_positioned = False
        
        empty_box = "\u25A1"
        filled_box = "\u25A0"
        xy_marker = empty_box
        heading_marker = empty_box
        
        while running:
            
            for event in pygame.event.get():
                
                # Checks if the user closed the window
                if event.type == pygame.QUIT: 
                    running = False
                    closed = True
                
                # Left click: positioning (x,y)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: 
                    robot_start_x, robot_start_y = pygame.mouse.get_pos()
                    xy_positioned = True
                    xy_marker = filled_box
                
                # Mouse wheel: angular positioning
                if event.type == pygame.MOUSEBUTTONDOWN and event.button in [4, 5]:
                    if event.button == 4:
                        direction = 1
                    elif event.button == 5:
                        direction = -1
                    robot_start_heading += direction*np.pi/6
                    robot_start_heading = robot_start_heading % (2*np.pi)
                    heading_positioned = True
                    heading_marker = filled_box
                    
                # Confirmation
                if (event.type == pygame.KEYDOWN and 
                    xy_positioned and
                    heading_positioned):
                    running = False
                    
            # Draws the map
            self.map.blit(self.map_image, (0, 0))
            
            # Draws a box with instructions
            BOX_POSITION = (10, 80)
            BOX_SIZE = (480, 150)
            if xy_positioned and heading_positioned:
                BOX_SIZE = (480, 200)
            BOX_COLOR = (0, 0, 0)
            BOX_BACKGROUND_COLOR = (255, 255, 255)  # White for the background
            BOX_BORDER_WIDTH = 2
            box = pygame.Rect(BOX_POSITION, BOX_SIZE)
            #
            # Draw the box background
            pygame.draw.rect(self.map, BOX_BACKGROUND_COLOR, box)
            #
            # Draw the box border
            pygame.draw.rect(self.map, BOX_COLOR, box, BOX_BORDER_WIDTH)
            #
            # Writes the robot positioning instructions
            self.show_text(text="Position the robot:",
                        position=(20, 100), fontsize=25)
            #
            self.show_text(text=f"{heading_marker} Scroll the mouse wheel to rotate the robot.",
                        position=(40, 150), fontsize=20)
            #
            self.show_text(text=f"{xy_marker} Left click to position the robot.",
                        position=(40, 190), fontsize=20)
            #
            if xy_positioned and heading_positioned:
                self.show_text(text="Press any key to continue.",
                            position=(20, 240), fontsize=25)
                
            # Draws the robot at the mouse position if it hasn't been positioned yet
            if not(xy_positioned):
                mouse_x, mouse_y = pygame.mouse.get_pos()
                self.draw_robot(mouse_x, mouse_y, robot_start_heading)
            else:
                self.draw_robot(robot_start_x, robot_start_y, robot_start_heading)
                
            # Updates the screen
            pygame.display.update()
            
        return (robot_start_x, robot_start_y, robot_start_heading), closed
    
    def sensors_positioning(self, number_of_sensors, robot_start, closed):
        """Positions the sensors according to the user's mouse click.
        
        Args:
            number_of_sensors (int): number of sensors (max = 10).
            robot_start (tuple): robot initial position (x, y, heading).
            closed (bool): True if the user closed the last window, False otherwise.
            
        Returns:
            list: list of sensors relative positions (x, y).
            bool: True if the user closed the window, False otherwise.
        """
        
        running = True
        sensors_positions = []
        sensors_relative_positions = []
        counter = 0
        
        sensor_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255),
                        (255, 255, 0), (0, 255, 255), (255, 0, 255),
                        (255, 255, 255), (128, 0, 0), (0, 128, 0),
                        (0, 0, 128)]
        
        while counter < number_of_sensors and running and not(closed):
            
            for event in pygame.event.get():
                
                # Checks if the user closed the window
                if event.type == pygame.QUIT: 
                    running = False
                    closed = True
                
                # Left click: positioning (x,y)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: 
                    
                    # Absolute sensors positions
                    sensor_x, sensor_y = pygame.mouse.get_pos()
                    sensors_positions.append((sensor_x, sensor_y))
                    
                    # Sensors positions relative to the robot (considering its angle)
                    sensor_relative_x = sensor_x - robot_start[0]
                    sensor_relative_y = robot_start[1] - sensor_y
                    sensor_relative = utils.rotate_vector((sensor_relative_x, sensor_relative_y), -robot_start[2])
                    sensors_relative_positions.append(list(sensor_relative))
                    
                    counter += 1
            
            # Draws the map
            self.map.blit(self.map_image, (0, 0))
            
            # Draws the robot at the initial position
            self.draw_robot(robot_start[0], robot_start[1], robot_start[2])
            
            # Writes the robot positioning instructions
            BOX_POSITION = (10, 80)
            BOX_SIZE = (460, 150)
            BOX_COLOR = (0, 0, 0)  # Black for the border
            BOX_BACKGROUND_COLOR = (255, 255, 255)  # White for the background
            BOX_BORDER_WIDTH = 2
            box = pygame.Rect(BOX_POSITION, BOX_SIZE)
            #
            # Draw the box background
            pygame.draw.rect(self.map, BOX_BACKGROUND_COLOR, box)
            #
            # Draw the box border
            pygame.draw.rect(self.map, BOX_COLOR, box, BOX_BORDER_WIDTH)
            #
            # Writes the sensor positioning instructions on the screen
            self.show_text(text="Position the sensors:",
                        position=(20, 100), fontsize=25)
            #
            self.show_text(text="Left click to position each sensor.",
                        position=(40, 150), fontsize=20)
            #
            self.show_text(text=f"Positioned: {counter}/{number_of_sensors}",
                        position=(20, 190), fontsize=25)
            
            # Draws the positioned sensors at the desired position
            for sensor in sensors_positions:
                self.draw_sensor_symbol((sensor[0], sensor[1]), color=sensor_colors[sensors_positions.index(sensor)])
                    
            # Draws the sensor to be positioned at the mouse position 
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if counter < number_of_sensors:
                color_counter = counter
            else:
                color_counter = number_of_sensors - 1
            self.draw_sensor_symbol((mouse_x, mouse_y), color=sensor_colors[color_counter])
            
            # Updates the screen
            pygame.display.update()
            
        return sensors_relative_positions, closed
    
    def draw_robot(self, x, y, heading):
        """Draws the robot on the screen.
        
        Args:
            x (float): robot horizontal position, in meters.
            y (float): robot vertical position, in meters.
            heading (float): robot angle, in radians.
        """
        
        # Applies the rotation to the robot image according to the "heading" angle
        rotated_robot = pygame.transform.rotozoom(self.robot_image, np.degrees(heading), 1)
        
        # Creates a rectangle with the robot image size and positions it at the center of the robot
        rect = rotated_robot.get_rect(center=(x, y))
        
        # Draws the robot on the screen at the rectangle position
        self.map.blit(rotated_robot, rect)
        
    def draw_sensor(self, sensor, color=(255, 0, 0)):
        """Draws a sensor on the screen.
        
        Args:
            sensor (Sensor): sensor to be drawn.
        """
        
        # Draws a red circle at the sensor position
        position = (int(sensor.x), int(sensor.y))
        self.draw_sensor_symbol(position, color)
        
    def draw_sensor_symbol(self, position, color=(255, 0, 0)):
        """Draws a sensor on the screen.
        
        Args:
            position (tuple): sensor position (x, y), in pixels.
        """
        
        # Draws a circle with a black border at the sensor position
        pygame.draw.circle(self.map, (0, 0, 0), (position[0], position[1]), 6)
        pygame.draw.circle(self.map, color, (position[0], position[1]), 5)
        
    def show_sensors_data(self, sensors, sensor_colors):
        """Displays the sensor data on the screen.
        
        Args:
            sensores (list): list of sensors.
            
        """
        
        # Creates a font
        font = pygame.font.SysFont("Arial", 20)
        
        # Creates a text with the sensor data
        text = []
        text_counter = 0
        for sensor in sensors:
            text.append(font.render(f"{text_counter}  = "+ str(sensor.data), True, (0, 0, 0)))
            text_counter += 1
        
        # Draws a box around the text
        BOX_POSITION = (10, 35)
        BOX_SIZE = (100, 30 + 20*len(text))
        BOX_COLOR = (0, 0, 0)
        BOX_BACKGROUND_COLOR = (255, 255, 255)
        BOX_BORDER_WIDTH = 2
        box = pygame.Rect(BOX_POSITION, BOX_SIZE)
        #
        # Draw the box background
        pygame.draw.rect(self.map, BOX_BACKGROUND_COLOR, box)
        #
        # Draw the box border
        pygame.draw.rect(self.map, BOX_COLOR, box, BOX_BORDER_WIDTH)
        
        # Draws the text and sensor symbol on the screen
        text_number = len(text)
        for idx in range(text_number):
            self.draw_sensor_symbol((30, 58 + 20*idx), color=sensor_colors[idx])
            self.map.blit(text[idx], (40, 50 + 20*idx))
            
    def is_out_of_bounds(self, object):
        """Checks if the object is out of bounds.
        
        Args:
            object (Robot or Sensor): object to be checked.
        
        Returns:
            bool: True if the object is out of bounds, False otherwise.
        """
        
        # Checks if the robot is within the arena limits
        if (object.x < 0 or
            object.x > self.map.get_width() or
            object.y < 0 or
            object.y > self.map.get_height()):
            return True
        else:
            return False
        
    def show_important_message(self, message):
        """Displays an important message on the screen (centered, with a box around).
        
        Args:
            message (str): message to be displayed.
        """

        font = pygame.font.SysFont("Arial", 30)
        text = font.render(message, True, (0, 0, 0))

        # Calculates the x and y position to center the text
        text_rect = text.get_rect(center=(self.map.get_width()/2, self.map.get_height()/2))

        # Draws a black rectangle slightly larger than the text to create the border
        border_rect = pygame.Rect(text_rect.left - 15, text_rect.top - 15, text_rect.width + 30, text_rect.height + 30)
        pygame.draw.rect(self.map, (0, 0, 0), border_rect)

        # Draws a white rectangle slightly larger than the text to be the background
        pygame.draw.rect(self.map, (255, 255, 255), (text_rect.left - 12, text_rect.top - 12, text_rect.width + 24, text_rect.height + 24))

        self.map.blit(text, text_rect)
        
    def show_text(self, text, position, fontsize=30, color=(0, 0, 0)):
        """Displays a text on the screen.
        
        Args:
            text (str): text to be displayed.
            position (tuple): text position (x, y), in pixels.
        """
        
        font = pygame.font.SysFont("Arial", fontsize)
        text = font.render(text, True, color)
        self.map.blit(text, position)
        