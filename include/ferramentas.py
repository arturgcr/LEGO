def constrainpy(valor, minimo, maximo):
    """
    Função constrain lá do Arduino em Python.

    int ou float, int ou float, int ou float -> int ou float
    """
    if valor > maximo:
        valor = maximo
    elif valor < minimo:
        valor = minimo
    
    return valor
