import random

import config
import formas

def gerar_forma_aleatoria():
    x = random.randint(100, config.LARGURA - 100)
    y = random.randint(100, config.ALTURA - 100)
    cor = random.choice(list(config.CORES.values()))
    tipo = random.choice([formas.Circulo, formas.Quadrado, formas.Triangulo])
    return tipo(x, y, cor)

def gerar_posicao():
    x = random.randint(100, config.LARGURA - 100)
    y = random.randint(100, config.ALTURA - 100)
    return x, y

def gerar_cor():
    return random.choice(list(config.CORES.values()))
