import numpy as np
import pygame

# +===========================================================================+
# |                              Classe Robot                                 |
# +===========================================================================+

class Robot:
    """Modelo de robô diferencial."""
    
    def __init__(self, initial_position, width, 
                 initial_speed=0.01, min_speed=0.01, max_speed=0.02):
        """Construtor da classe Robot. Inicializa a posição e velocidade do robô.

        Args:
            initial_position (tuple): posição inicial do robô (x, y, heading), sendo "x" e "y" \
                as coordenadas do robô em metros e "heading" o ângulo em radianos.
            width (float): largura do robô, em metros.
            initial_speed (float, optional): velocidade inicial do robô, em metros por segundo. \
                Defaults to 0.01.
            min_speed (float, optional): velocidade mínima do robô, em metros por segundo. \
                Defaults to 0.01.
            max_speed (float, optional): velocidade máxima do robô, em metros por segundo. \
                Defaults to 0.02.
        """
        
        # Fator de escala de metros para pixels
        self.meters_to_pixels = 3779.52
        
        # Dimensões do robô
        self.width = width
        
        # Posição inicial do robô
        self.x = initial_position[0]
        self.y = initial_position[1]
        self.heading = initial_position[2]
        
        # Velocidade inicial do robô (1 cm/s)
        self.left_wheel_speed = initial_speed*self.meters_to_pixels
        self.right_wheel_speed = initial_speed*self.meters_to_pixels
        
        # Velocidade mínima e máxima do robô (1 cm/s, 2 cm/s)
        self.min_speed = min_speed*self.meters_to_pixels
        self.max_speed = max_speed*self.meters_to_pixels
        
    def move_forward(self):
        """Move o robô para frente com velocidade máxima."""
        self.left_wheel_speed = self.max_speed
        self.right_wheel_speed = self.max_speed
    
    def move_backward(self):
        """Move o robô para trás com velocidade máxima."""
        self.left_wheel_speed = -self.max_speed
        self.right_wheel_speed = -self.max_speed
    
    def turn_left(self):
        """Gira robô pra esquerda com velocidade máxima."""
        self.left_wheel_speed = self.max_speed/2
        self.right_wheel_speed = self.max_speed
    
    def turn_right(self):
        """Gira robô pra direita com velocidade máxima."""
        self.left_wheel_speed = self.max_speed
        self.right_wheel_speed = self.max_speed/2
    
    def stop(self):
        """Para o robô."""
        self.left_wheel_speed = 0
        self.right_wheel_speed = 0
        
    def update_position(self, dt):
        """Atualiza a posição do robô de acordo com a velocidade das rodas.
        
        Args:
            dt (float): tempo decorrido desde a última iteração, em segundos."""
        
        # Movimentação diferencial
        #
        # Velocidade de movimentação horizontal, vertical e angular
        x_speed = (self.left_wheel_speed + self.right_wheel_speed)*np.cos(self.heading)/2
        y_speed = (self.left_wheel_speed + self.right_wheel_speed)*np.sin(self.heading)/2
        heading_speed = (self.right_wheel_speed - self.left_wheel_speed)/self.width
        #
        # Atualização da posição e ângulo de acordo com o tempo decorrido
        self.x += x_speed*dt
        self.y -= y_speed*dt # Eixo y aumenta pra baixo
        self.heading += heading_speed*dt
        
        # Ajusta o ângulo para o intervalo [-2pi, 2pi]
        if (self.heading > 2*np.pi) or (self.heading < -2*np.pi):
            self.heading = 0


# +===========================================================================+
# |                             Classe Sensor                                 |
# +===========================================================================+

def rotate_vector(vector, angle):
    """Rotaciona um vetor em um ângulo.
    
    Args:
        vector (tuple): vetor a ser rotacionado (x, y).
        angle (float): ângulo de rotação, em radianos.
        
    Returns:
        tuple: vetor rotacionado (x, y).
    """
    
    # Matriz de rotação
    rotation_matrix = np.array([[np.cos(angle), -np.sin(angle)],
                                [np.sin(angle), np.cos(angle)]])
    
    # Multiplica o vetor pela matriz de rotação
    rotated_vector = rotation_matrix.dot(vector)
    
    return rotated_vector

def is_darker(color1, color2):
    """Verifica se a cor1 é mais escura que a cor2.
    
    Args:
        color1, color2 (tuple): Cores no formato RGB (R, G, B).
        
    Returns:
        bool: True se a cor1 for mais escura que a cor2, False caso contrário.
    """
    # Calcula a média dos valores RGB de cada cor (escala de cinza)
    gray1 = sum(color1) / len(color1)
    gray2 = sum(color2) / len(color2)
    
    return gray1 < gray2


class Sensor:
    """Sensor de linha."""
    
    def __init__(self, sensor_relative_position, robot_initial_position):
        """Construtor da classe Sensor. Posiciona sensor em relação à posição inicial do robô.
        
        Args:
            sensor_relative_position (tuple): posição do sensor (x, y) em relação ao robô, em metros.
            robot_initial_position (tuple): posição inicial do robô (x, y, heading), em metros e radianos.
        """
        
        # Rotaciona vetor de posição do sensor de acordo com o ângulo do robô
        sensor_position_rotated = rotate_vector(sensor_relative_position, robot_initial_position[2])
        
        # Adiciona o vetor de posição relativa (rotacionado) à posição inicial do robô
        self.x = robot_initial_position[0] + sensor_position_rotated[0] 
        self.y = robot_initial_position[1] - sensor_position_rotated[1] # Subtrai pois o eixo y aumenta pra baixo
        
    def update_position(self, sensor_relative_position, robot_position):
        """Atualiza a posição do sensor de acordo com a posição do robô.
        
        Args:
            robot_position (tuple): posição atual do robô (x, y, heading), em metros e radianos.
        """
        # Rotaciona vetor de posição relativa do sensor de acordo com o ângulo do robô
        sensor_position_rotated = rotate_vector(sensor_relative_position, robot_position[2])
        
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
        self.data = 1 if is_darker(color, (255/2, 255/2, 255/2)) else 0


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
        pygame.draw.circle(self.map, (255, 0, 0), (sensor.x, sensor.y), 5)
        
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