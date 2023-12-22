import numpy as np
import pygame

from SIMULATOR import Robot, Sensor, Graphics

# Inicializa o mapa
MAP_DIMENSIONS = (1300, 660) # 1360x768
gfx = Graphics(MAP_DIMENSIONS, 'robot.png', 'map.png')

# Inicializa o robô
ROBOT_START = (100, 100, 0)
ROBOT_WIDTH = 0.01*3779.52
robot = Robot(ROBOT_START, width=ROBOT_WIDTH, max_speed=0.01)

# Inicializa sensores
SENSORS_POSITIONS = [(40, 0),
                    (40, -20),
                    (40, 20)]
sensors = [Sensor(position, ROBOT_START) for position in SENSORS_POSITIONS]

dt = 0
last_time = pygame.time.get_ticks()

running = True

it = 0

while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Calcula o tempo decorrido desde a última iteração
    current_time = pygame.time.get_ticks()
    dt = (current_time - last_time)/1000
    last_time = current_time
    
    gfx.map.blit(gfx.map_image, (0, 0))
    
    if it < 700:
        robot.move_forward()
        
    if it >= 700 and it < 800:
        robot.turn_left()
    
    if it >= 800 and it < 1000:
        robot.stop()
    
        
    # Atualiza a posição do robô 
    robot.update_position(dt)
    
    # Atualiza os sensores
    for idx in range(len(sensors)):
        sensors[idx].update_position(robot_position=(robot.x, robot.y, robot.heading),
                               sensor_relative_position=SENSORS_POSITIONS[idx])
    
    # Lê os sensores
    for idx in range(len(sensors)):
        sensors[idx].read_data(gfx.map_image)

    # Coloca na tela os valores dos sensores
    # Crie uma fonte
    font = pygame.font.Font(None, 36)

    # Crie uma Surface de texto
    text1 = font.render(str(sensors[0].data), True, (0, 0, 0))
    text2 = font.render(str(sensors[1].data), True, (0, 0, 0))
    text3 = font.render(str(sensors[2].data), True, (0, 0, 0))

    # Desenhe a Surface de texto na tela
    gfx.map.blit(text1, (200, 220))
    gfx.map.blit(text2, (200, 200))
    gfx.map.blit(text3, (200, 180))
    
    # Desenha o robô
    gfx.draw_robot(robot.x, robot.y, robot.heading)
    
    # Desenha os sensores
    for sensor in sensors:
        gfx.draw_sensor(sensor)
    
    it += 1
    
    pygame.display.update()