import numpy as np
import pygame
import utils

# +===========================================================================+
# |                      Classes Robot, Motor e Sensor                        |
# +===========================================================================+
class Motor:
    """Motor do robô. Compõe a classe Robot."""
    
    def __init__(self, max_motor_speed, wheel_radius):
        """Construtor da classe Motor. Determina a velocidade máxima e o raio da roda.
        
        Args:
            max_motor_speed (float): velocidade máxima do motor, em rpm.
            wheel_radius (float): raio da roda, em metros.
        """
    
        self.max_motor_speed = max_motor_speed
        self.wheel_radius = wheel_radius
    
    def set_speed(self, speed):
        """Define a velocidade do motor.
        
        Args:
            speed (float): velocidade do motor, em rpm.
        """
        
        self.speed = speed

class Robot:
    """Modelo de robô diferencial."""
    
    def __init__(self, initial_position, width, 
                 initial_motor_speed=500, max_motor_speed=1000, wheel_radius=0.04):
        """Construtor da classe Robot. Inicializa a posição e velocidade do robô.

        Args:
            initial_position (tuple): posição inicial do robô (x, y, heading), sendo "x" e "y" \
                as coordenadas do robô em metros e "heading" o ângulo em radianos.
            width (float): largura do robô, em metros.
            initial_motor_speed (float, optional): velocidade inicial dos motores, em rpm. \
                Defaults to 500.
            max_motor_speed (float, optional): velocidade máxima dos motores, em rpm. \
                Defaults to 1000.
            wheel_radius (float, optional): raio da roda, em metros. Defaults to 0.04.
        """
        
        # Fator de escala de metros para pixels
        self.meters_to_pixels = 3779.52
        
        # Dimensões do robô
        self.width = width
        
        # Posição inicial do robô
        self.x = initial_position[0]
        self.y = initial_position[1]
        self.heading = initial_position[2]
        
        # Construção dos motores
        self.left_motor = Motor(max_motor_speed, wheel_radius)
        self.right_motor = Motor(max_motor_speed, wheel_radius)
        
        # Velocidade inicial dos motores
        self.left_motor.set_speed(initial_motor_speed)
        self.right_motor.set_speed(initial_motor_speed)
        
    def update_position(self, dt):
        """Atualiza a posição do robô de acordo com a velocidade das rodas.
        
        Args:
            dt (float): tempo decorrido desde a última iteração, em segundos."""
        
        # Velocidade linear das rodas
        left_wheel_linear_speed = 2*np.pi*self.left_motor.wheel_radius*self.left_motor.speed/60
        right_wheel_linear_speed = 2*np.pi*self.right_motor.wheel_radius*self.right_motor.speed/60
        
        # Movimentação diferencial
        #
        # Velocidade de movimentação horizontal, vertical e angular
        x_speed = (left_wheel_linear_speed + right_wheel_linear_speed)*np.cos(self.heading)/2
        y_speed = (left_wheel_linear_speed + right_wheel_linear_speed)*np.sin(self.heading)/2
        heading_speed = (right_wheel_linear_speed - left_wheel_linear_speed)/self.width
        #
        # Atualização da posição e ângulo de acordo com o tempo decorrido
        self.x += x_speed*dt
        self.y -= y_speed*dt # Eixo y aumenta pra baixo
        self.heading += heading_speed*dt
        
        # Ajusta o ângulo para o intervalo [-2pi, 2pi]
        if (self.heading > 2*np.pi) or (self.heading < -2*np.pi):
            self.heading = 0

    def move_forward(self):
        """Move o robô para frente com velocidade máxima."""
        self.left_motor.set_speed(self.left_motor.max_motor_speed)
        self.right_motor.set_speed(self.right_motor.max_motor_speed)
    
    def move_backward(self):
        """Move o robô para trás com velocidade máxima."""
        self.left_motor.set_speed(-self.left_motor.max_motor_speed)
        self.right_motor.set_speed(-self.right_motor.max_motor_speed)
    
    def turn_left(self):
        """Gira robô pra esquerda com velocidade máxima."""
        self.left_motor.set_speed(-self.left_motor.max_motor_speed)
        self.right_motor.set_speed(self.right_motor.max_motor_speed)
    
    def turn_right(self):
        """Gira robô pra direita com velocidade máxima."""
        self.left_motor.set_speed(self.left_motor.max_motor_speed)
        self.right_motor.set_speed(-self.right_motor.max_motor_speed)
    
    def stop(self):
        """Para o robô."""
        self.left_motor.set_speed(0)
        self.right_motor.set_speed(0)

    
# +===========================================================================+
# |                             Classe Sensor                                 |
# +===========================================================================+
class Sensor:
    """Sensor de linha."""
    
    def __init__(self, sensor_relative_position, robot_initial_position):
        """Construtor da classe Sensor. Posiciona sensor em relação à posição inicial do robô.
        
        Args:
            sensor_relative_position (tuple): posição do sensor (x, y) em relação ao robô, em metros.
            robot_initial_position (tuple): posição inicial do robô (x, y, heading), em metros e radianos.
        """
        
        # Rotaciona vetor de posição do sensor de acordo com o ângulo do robô
        sensor_position_rotated = utils.rotate_vector(sensor_relative_position, robot_initial_position[2])
        
        # Adiciona o vetor de posição relativa (rotacionado) à posição inicial do robô
        self.x = robot_initial_position[0] + sensor_position_rotated[0] 
        self.y = robot_initial_position[1] - sensor_position_rotated[1] # Subtrai pois o eixo y aumenta pra baixo
        
    def update_position(self, sensor_relative_position, robot_position):
        """Atualiza a posição do sensor de acordo com a posição do robô.
        
        Args:
            robot_position (tuple): posição atual do robô (x, y, heading), em metros e radianos.
        """
        # Rotaciona vetor de posição relativa do sensor de acordo com o ângulo do robô
        sensor_position_rotated = utils.rotate_vector(sensor_relative_position, robot_position[2])
        
        # Adiciona o vetor de posição relativa à posição do robô pra obter a posição real do sensor
        self.x = robot_position[0] + sensor_position_rotated[0] 
        self.y = robot_position[1] - sensor_position_rotated[1] # Subtrai pois o eixo y aumenta pra baixo        
    
    def read_data(self, map_image):
        """Lê os dados do sensor. O sensor retorna 1 se lê uma cor escuta e 0 se lê uma cor clara.
        
        Args:
            map_image (pygame.Surface): imagem da arena.
        """
        
        # Sensor lê a cor do pixel da arena na posição do sensor
        color = map_image.get_at((int(self.x), int(self.y)))[:-1]
        
        # Retorna 0 se a cor for mais clara que o cinza médio e 1 caso contrário.
        self.data = 1 if utils.is_darker(color, (255/2, 255/2, 255/2)) else 0


# +===========================================================================+
# |                            Classe Graphics                                |
# +===========================================================================+

class Graphics:
    """Exibição gráfica do robô e da arena."""
    
    def __init__(self, screen_dimensions, robot_image_path, map_imape_path):
        """Construtor da classe Graphics. Inicializa a janela e carrega as imagens necessárias.
        
        Args:
            screen_dimensions (tuple): dimensões da janela (largura, altura), em pixels.
            robot_image_path (str): caminho para a imagem do robô.
            map_imape_path (str): caminho para a imagem da arena.
        """
        
        pygame.init()
        
        # Carrega as imagens e ajusta mapa ao tamanho da tela
        self.robot_image = pygame.image.load(robot_image_path)
        self.map_image = pygame.transform.scale(pygame.image.load(map_imape_path), screen_dimensions)
    
        # Cria a janela 
        pygame.display.set_caption("Line Follower Simulator")
        self.map = pygame.display.set_mode(screen_dimensions)
    
        # Desenha a arena
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
                
                # Verifica se o usuário fechou a janela
                if event.type == pygame.QUIT: 
                    running = False
                    closed = True
                
                # Left click: posicionamento (x,y)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: 
                    robot_start_x, robot_start_y = pygame.mouse.get_pos()
                    xy_positioned = True
                    xy_marker = filled_box
                
                # Mouse wheel: posicionamento angular
                if event.type == pygame.MOUSEBUTTONDOWN and event.button in [4, 5]:
                    if event.button == 4:  # Roda do mouse girada para cima
                        direction = 1
                    elif event.button == 5:  # Roda do mouse girada para baixo
                        direction = -1
                    robot_start_heading += direction*np.pi/6 # Gira robô 30 graus        
                    robot_start_heading = robot_start_heading % (2*np.pi) # Converte p/ intervalo [0, 2pi]
                    heading_positioned = True
                    heading_marker = filled_box
                
                # Confirmação
                if (event.type == pygame.KEYDOWN and 
                    xy_positioned and
                    heading_positioned):
                    running = False
            
            # Desenha mapa
            self.map.blit(self.map_image, (0, 0))
            
            # Escreve na tela a mensagem de posicionamento do robô
            self.show_text(text="Position the robot:",
                        position=(20, 100), fontsize=25)
            self.show_text(text=f"{heading_marker} Scroll the mouse wheel to rotate the robot.",
                        position=(40, 150), fontsize=20)
            self.show_text(text=f"{xy_marker} Left click to position the robot.",
                        position=(40, 190), fontsize=20)
            if xy_positioned and heading_positioned:
                self.show_text(text="Press any key to continue.",
                            position=(20, 240), fontsize=25)
            
            # Desenha o robô na posição do mouse se ainda não tiver sido posicionado
            if not(xy_positioned):
                mouse_x, mouse_y = pygame.mouse.get_pos()
                self.draw_robot(mouse_x, mouse_y, robot_start_heading)
            else:
                self.draw_robot(robot_start_x, robot_start_y, robot_start_heading)
            
            # Atualiza a tela
            pygame.display.update()
            
        return (robot_start_x, robot_start_y, robot_start_heading), closed
    
    def sensors_positioning(self, robot_start, closed):
        """Positions the sensors according to the user's mouse click.
        
        Args:
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
        
        while counter < 5 and running and not(closed):
            
            for event in pygame.event.get():
                
                # Verifica se o usuário fechou a janela
                if event.type == pygame.QUIT: 
                    running = False
                    closed = True
                
                # Left click: posicionamento (x,y)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: 
                    
                    # Posição absoluta dos sensores
                    sensor_x, sensor_y = pygame.mouse.get_pos()
                    sensors_positions.append((sensor_x, sensor_y))
                    
                    # Posição dos sensores em relação ao robô (considerando o seu ângulo)
                    sensor_relative_x = sensor_x - robot_start[0]
                    sensor_relative_y = robot_start[1] - sensor_y # Subtrai pois o eixo y aumenta pra baixo
                    sensor_relative = utils.rotate_vector((sensor_relative_x, sensor_relative_y), -robot_start[2])
                    sensors_relative_positions.append(sensor_relative)
                    
                    counter += 1
            
            # Desenha mapa
            self.map.blit(self.map_image, (0, 0))
            
            # Desenha o robô na posição inicial
            self.draw_robot(robot_start[0], robot_start[1], robot_start[2])
            
            # Escreve na tela a mensagem de posicionamento dos sensores
            self.show_text(text="Position the sensors:",
                        position=(20, 100), fontsize=25)
            self.show_text(text="Left click to position each sensor.",
                        position=(40, 150), fontsize=20)
            self.show_text(text=f"Positioned: {counter}/5",
                        position=(20, 190), fontsize=25)
        
            # Desenha na posição desejada os sensores já posicionados
            for sensor in sensors_positions:
                self.draw_sensor_symbol((sensor[0], sensor[1]))
                    
            # Desenha na posição do mouse o sensor a ser posicionado 
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.draw_sensor_symbol((mouse_x, mouse_y))
            
            # Atualiza a tela
            pygame.display.update()
            
        return sensors_relative_positions, closed
    
    def draw_robot(self, x, y, heading):
        """Desenha o robô na tela.
        
        Args:
            x (float): posição horizontal do robô, em metros.
            y (float): posição vertical do robô, em metros.
            heading (float): ângulo do robô, em radianos.
        """
        
        # Aplica a rotação na imagem do robô de acordo com o ângulo "heading"
        rotated_robot = pygame.transform.rotozoom(self.robot_image, np.degrees(heading), 1)
        
        # Cria um retângulo com o tamanho da imagem do robô e o posiciona no centro do robô
        rect = rotated_robot.get_rect(center=(x, y))
        
        # Desenha o robô na tela na posição do retângulo criado
        self.map.blit(rotated_robot, rect)    

    def draw_sensor(self, sensor):
        """Desenha um sensor na tela.
        
        Args:
            sensor (Sensor): sensor a ser desenhado.
        """
        
        # Desenha um círculo vermelho na posição do sensor
        position = (int(sensor.x), int(sensor.y))
        self.draw_sensor_symbol(position)
        
    def draw_sensor_symbol(self, position):
        """Desenha um sensor na tela.
        
        Args:
            position (tuple): posição (x,y) do sensor, em pixels.
        """
        
        # Desenha um círculo vermelho na posição do sensor
        pygame.draw.circle(self.map, (255, 0, 0), (position[0], position[1]), 5)
        
    def show_sensors_data(self, sensors):
        """Exibe os dados dos sensores na tela.
        
        Args:
            sensores (list): lista com os sensores.
        """
        
        # Cria uma fonte
        font = pygame.font.SysFont("Arial", 20)
        
        # Cria um texto com os dados do sensor
        text = []
        text_counter = 0
        for sensor in sensors:
            text.append(font.render(f"Sensor {text_counter}: "+ str(sensor.data), True, (0, 0, 0)))
            text_counter += 1
        
        # Desenha o texto na tela
        text_number = len(text)
        for idx in range(text_number):
            self.map.blit(text[idx], (10, 10 + 20*idx))
            
    def is_out_of_bounds(self, object):
        """Verifica se objeto saiu dos limites da arena.
        
        Args:
            object (Robot ou Sensor): objeto que queremos verificar.
        
        Returns:
            bool: True se o objeto saiu dos limites da arena, False caso contrário.
        """
        
        # Verifica se o robô está dentro dos limites da arena
        if (object.x < 0 or
            object.x > self.map.get_width() or
            object.y < 0 or
            object.y > self.map.get_height()):
            return True
        else:
            return False    
    
    def show_out_of_bounds_error(self):
        """Exibe mensagem de erro na tela quando o robô sai do mapa."""

        font = pygame.font.SysFont("Arial", 30)
        text = font.render("The robot went off the map!", True, (0, 0, 0))

        # Calcula a posição x e y para centralizar o texto
        text_rect = text.get_rect(center=(self.map.get_width()/2, self.map.get_height()/2))

        # Desenha um retângulo preto um pouco maior que o texto para criar a borda
        border_rect = pygame.Rect(text_rect.left - 15, text_rect.top - 15, text_rect.width + 30, text_rect.height + 30)
        pygame.draw.rect(self.map, (0, 0, 0), border_rect)

        # Desenha um retângulo branco um pouco maior que o texto para ser o fundo
        pygame.draw.rect(self.map, (255, 255, 255), (text_rect.left - 12, text_rect.top - 12, text_rect.width + 24, text_rect.height + 24))

        self.map.blit(text, text_rect)
        
    def show_text(self, text, position, fontsize=30, color=(0, 0, 0)):
        """Exibe um texto na tela.
        
        Args:
            text (str): texto a ser exibido.
            position (tuple): posição do texto (x, y), em pixels.
        """
        
        font = pygame.font.SysFont("Arial", fontsize)
        text = font.render(text, True, color)
        self.map.blit(text, position)
