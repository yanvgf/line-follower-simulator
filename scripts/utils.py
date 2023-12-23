import numpy as np

def PID(kp, ki, kd, I,
        error, last_error, dt):
    """Cálculo do controle PID.

    Args:
        kp (float): ganho proporcional.
        ki (float): ganho integral.
        kd (float): ganho derivativo.
        I (float): valor anterior da parte integral.
        error (float): erro atual do sistema.
        last_error (float): erro anterior do sistema.
        dt (float): tempo decorrido desde a última iteração.

    Returns:
        float: valor do controle PID.
        float: novo valor da parte integral.
    """
    
    # Evita erro no cálculo do PID na primeira iteração
    if dt == 0:
        dt+=1e-5
    
    P = kp*error
    D = kd*(error - last_error)/dt
    I += ki*error*dt
 
    return P + D + I, I

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
