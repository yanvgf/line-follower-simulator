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
