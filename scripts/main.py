import numpy as np
import pygame

from simulator import Robot, Sensor, Graphics
import utils


# +=====================================================================+
# |                         Inicialização                               |
# +=====================================================================+

# Inicializa o mapa
MAP_DIMENSIONS = (1300, 660) # 1360x768
gfx = Graphics(MAP_DIMENSIONS, 'images/robot.png', 'images/map.png')
    
# Inicializa o robô
ROBOT_START = gfx.robot_positioning()
ROBOT_WIDTH = 0.1
INITIAL_MOTOR_SPEED = 10000
MAX_MOTOR_SPEED = 20000
WHEEL_RADIUS = 0.04
robot = Robot(initial_position=ROBOT_START,
              width=ROBOT_WIDTH,
              initial_motor_speed=INITIAL_MOTOR_SPEED,
              max_motor_speed=MAX_MOTOR_SPEED,
              wheel_radius=WHEEL_RADIUS)

# Inicializa sensores
# TODO: permitir ao usuário posicionar os sensores
# TODO: salvar as configurações de posição dos sensores e do robô em um arquivo separado
#       pro usuário não ter que mexer toda hora que for rodar
SENSORS_POSITIONS = [(40, -45),
                    (40, -20),
                    (40, 0),
                    (40, 20),
                    (40, 45)]
sensors = [Sensor(position, ROBOT_START) for position in SENSORS_POSITIONS]



# +=====================================================================+
# |                            Simulação                                |
# +=====================================================================+

last_time = pygame.time.get_ticks()
last_error = 0
I = 0 # PID integral

running = True

while running:
    
    # Verifica se o usuário fechou a janela
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Desenha mapa
    gfx.map.blit(gfx.map_image, (0, 0))
    #
    # Desenha o robô
    gfx.draw_robot(robot.x, robot.y, robot.heading)
    #
    # Desenha os sensores
    for sensor in sensors:
        gfx.draw_sensor(sensor)
       
    # Lê os sensores
    for idx in range(len(sensors)):
        sensors[idx].read_data(gfx.map_image)
    #
    # Escreve dados dos sensores na tela
    gfx.show_sensors_data(sensors)

    # Calcula o tempo decorrido desde a última iteração
    current_time = pygame.time.get_ticks()
    dt = (current_time - last_time)/1000
    last_time = current_time

# +=====================================================================+
# |                         Control logic                               |
# |                                                                     |
    # Calcula o erro e escreve na tela
    error = sensors[1].data - sensors[3].data
    gfx.show_text(text=f"Error: "+ str(error),
                  position=(10, 10 + 130))
    
    # Calcula PID
    pid, I = utils.PID(kp=50, ki=3, kd=0.01, I=I,
                 error=error, last_error=last_error, dt=dt)
    
    # Atualiza o erro anterior
    last_error = error
    
    # Atualiza velocidade dos motores baseado no controlador
    robot.left_motor.set_speed(robot.left_motor.max_motor_speed + pid)
    robot.right_motor.set_speed(robot.right_motor.max_motor_speed - pid)
# |                                                                     |
# |                                                                     |
# +=====================================================================+

    # Atualiza a posição do robô 
    robot.update_position(dt)
    
    # Atualiza a posição dos sensores
    for idx in range(len(sensors)):
        sensors[idx].update_position(robot_position=(robot.x, robot.y, robot.heading),
                            sensor_relative_position=SENSORS_POSITIONS[idx])

    # Verifica se o robô saiu do mapa
    robot_is_out = gfx.is_out_of_bounds(robot)
    sensor_is_out = bool(np.sum([gfx.is_out_of_bounds(sensor) for sensor in sensors]))
    #
    # Escreve mensagem de erro se robô saiu do mapa
    if robot_is_out or sensor_is_out:
            
            gfx.show_out_of_bounds_error()
            
            # Escreve na tela a mensagem de erro
            pygame.display.update()
            pygame.time.wait(3500)
            running = False
    
    if running:
        pygame.display.update()