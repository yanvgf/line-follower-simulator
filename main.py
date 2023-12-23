import numpy as np
import pygame

from SIMULATOR import Robot, Sensor, Graphics

# Inicializa o mapa
MAP_DIMENSIONS = (1300, 660) # 1360x768
gfx = Graphics(MAP_DIMENSIONS, 'robot.png', 'map.png')

# Inicializa o robô
ROBOT_START = (865, 600, np.pi/2)
ROBOT_WIDTH = 0.01*3779.52
robot = Robot(ROBOT_START, width=ROBOT_WIDTH, initial_speed=0, max_speed=0.01)

# Inicializa sensores
SENSORS_POSITIONS = [(40, -45),
                    (40, -20),
                    (40, 0),
                    (40, 20),
                    (40, 45)]
sensors = [Sensor(position, ROBOT_START) for position in SENSORS_POSITIONS]

dt = 0
last_time = pygame.time.get_ticks()

running = True

it = 0

while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                robot.move_forward()
            elif event.key == pygame.K_LEFT:
                robot.turn_left()
            elif event.key == pygame.K_DOWN:
                robot.move_backward()
            elif event.key == pygame.K_RIGHT:
                robot.turn_right()
            elif event.key == pygame.K_SPACE:
                robot.stop()
    
    # Calcula o tempo decorrido desde a última iteração
    current_time = pygame.time.get_ticks()
    dt = (current_time - last_time)/1000
    last_time = current_time
    
    gfx.map.blit(gfx.map_image, (0, 0))
        
    # Atualiza a posição do robô 
    robot.update_position(dt)
    
    # Atualiza os sensores
    for idx in range(len(sensors)):
        sensors[idx].update_position(robot_position=(robot.x, robot.y, robot.heading),
                               sensor_relative_position=SENSORS_POSITIONS[idx])
    
    # Lê os sensores
    for idx in range(len(sensors)):
        sensors[idx].read_data(gfx.map_image)

    # Escreve dados dos sensores na tela
    gfx.show_sensors_data(sensors)
    
    # Desenha o robô
    gfx.draw_robot(robot.x, robot.y, robot.heading)
    
    # Desenha os sensores
    for sensor in sensors:
        gfx.draw_sensor(sensor)
    
    it += 1
    
    pygame.display.update()