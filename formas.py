from abc import ABC, abstractmethod
import pygame as pg
from pygame.math import Vector2
from typing import Sequence, Optional
from math import pi, cos, sin, radians, tan


def reta_corta_segmento(p1: Vector2, p2: Vector2, p0: Vector2, v0: Vector2) -> Optional[tuple[Vector2, float, float]]:
    """
    Verifica se um segmento (p1->p2) intersecta uma reta (p0 + t*v0).
    
    Returns:
        tuple[Vector2, float, float] | None: (ponto_intersecao, t_segmento, t_reta) ou None
        - t_segmento: parâmetro do segmento [0,1]
        - t_reta: parâmetro da reta
    """
    seg_dir = p2 - p1  # Direção do segmento
    
    # Verifica se as linhas são paralelas
    denominador = seg_dir.cross(v0)
    if abs(denominador) < 1e-10:
        return None  # Paralelas ou colineares
    
    # Calcula os parâmetros
    diff = p0 - p1
    t_seg = diff.cross(v0) / denominador
    t_reta = diff.cross(seg_dir) / denominador
    
    # Verifica se a intersecção está dentro do segmento
    if not (0 <= t_seg <= 1):
        return None
    
    # Calcula o ponto de intersecção
    ponto_intersecao = p1 + t_seg * seg_dir
    
    return ponto_intersecao, t_seg, t_reta

class Forma(ABC):
    def __init__(self, cor, tipo: str, gravidade: float = 50):
        self.cor: tuple[int, int, int] = cor
        self.gravidade: float = gravidade
        self.posicao: Vector2 = Vector2(0, 0)
        self.velocidade: Vector2 = Vector2(0, 0)
        self.rotacao: float = 0.0
        self.velocidade_rotacao: float = 0.0
        self.tipo: str = tipo

    @abstractmethod
    def colide_com_ponto(self, ponto: Vector2 | Sequence[float]) -> bool:
        """Verifica se a forma colide com um ponto."""
        pass

    @abstractmethod
    def colide_com_segmento(self, p1: Vector2 | Sequence[float], v: Vector2 | Sequence[float]) -> bool:
        """Verifica se a forma colide com um segmento de reta definido por um ponto e um vetor."""
        pass

    @abstractmethod
    def desenhar(self, tela: pg.Surface) -> None:
        """Desenha a forma na tela.
        Se cor for None, usa a cor da forma.
        Se pos for None, usa a posição atual da forma.
        """
        pass

    @abstractmethod
    def desenhar_com_sombra(self, tela: pg.Surface, deslocamento_sombra: Vector2 = Vector2(5, 5)) -> None:
        """Desenha a forma com uma sombra"""
        pass

    @abstractmethod
    def cortar(self, ponto: Vector2 | Sequence[float | int], v: Vector2 | Sequence[float | int]) -> list['Forma']:
        """Particiona a forma em duas partes a partir de um ponto e um vetor.
        Este método deve ser implementado por subclasses que suportam partição.
        Args:
            ponto (Vector2 | Sequence[float]): Ponto onde a forma será particionada.
            v (Vector2 | Sequence[float]): Vetor que define a direção da partição.
        """
        pass


    def atualizar(self, delta_time: float) -> None:
        """Atualiza a posição da forma com base na gravidade."""
        self.velocidade.y += self.gravidade * delta_time
        self.posicao += self.velocidade * delta_time
        if self.posicao.y < 0:
            self.posicao.y = 0
        
        self.rotacao += self.velocidade_rotacao * delta_time

    def set_posicao(self, x: float, y: float) -> 'Forma':
        """Define a posição da forma."""
        self.posicao.x = x
        self.posicao.y = y
        return self

    def set_velocidade(self, vx: float, vy: float) -> 'Forma':
        """Define a velocidade da forma."""
        self.velocidade.x = vx
        self.velocidade.y = vy
        return self
    
    def set_rotacao(self, angulo: float) -> 'Forma':
        """Define a rotação da forma."""
        self.rotacao = angulo % 360
        return self

    def set_velocidade_rotacao(self, velocidade: float) -> 'Forma':
        """Define a velocidade de rotação da forma. (positivo para sentido horário, negativo para anti-horário)
        Args:
            velocidade (float): Velocidade de rotação em graus por segundo.
        """
        self.velocidade_rotacao = velocidade
        return self

def _baricentro(vertices: Sequence[Vector2]) -> Vector2:
    """Calcula o baricentro (centroide) de área de um polígono usando a fórmula da área com coordenadas."""
    if len(vertices) < 3:
        return Vector2(0, 0)
        
    area = 0.0
    cx = 0.0
    cy = 0.0
    n = len(vertices)

    for i in range(n):
        j = (i + 1) % n
        cross_product = vertices[i].x * vertices[j].y - vertices[j].x * vertices[i].y
        area += cross_product
        cx += (vertices[i].x + vertices[j].x) * cross_product
        cy += (vertices[i].y + vertices[j].y) * cross_product

    area *= 0.5
    if abs(area) < 1e-10:  # Evita divisão por zero para polígonos degenerados
        # Fallback para centroide simples
        x_sum = sum(v.x for v in vertices)
        y_sum = sum(v.y for v in vertices)
        return Vector2(x_sum / n, y_sum / n)

    cx /= (6.0 * area)
    cy /= (6.0 * area)

    return Vector2(cx, cy)

def _sequence_to_vector2(seq: Sequence[float] | Vector2) -> Vector2:
    if isinstance(seq, Vector2):
        return seq
    if len(seq) != 2:
        raise ValueError("Sequência deve ter exatamente duas coordenadas.")
    return Vector2(seq[0], seq[1])

class Poligono(Forma):
    def __init__(self, vertices: Sequence[Vector2], cor: tuple[int, int, int], gravidade: float = 50, tipo: str = "Polígono"):
        super().__init__(cor, tipo, gravidade)
        baricentro = _baricentro(vertices)
        self.vertices = [v - baricentro for v in vertices]

        downscale_factor = 2
        self.lado = max(max(abs(v.x), abs(v.y)) for v in self.vertices) * 2 * downscale_factor + 4
        self.surface = pg.Surface((self.lado, self.lado), pg.SRCALPHA)
        points_in_texture = [v*downscale_factor + Vector2(self.lado/2, self.lado/2) for v in self.vertices]
        pg.draw.polygon(self.surface, cor, points_in_texture)
        pg.draw.lines(self.surface, (0, 0, 0), True, points_in_texture, width=3)
        self.surface=pg.transform.smoothscale_by(self.surface, 1/downscale_factor)
        self.sombra = pg.Surface((self.lado, self.lado), pg.SRCALPHA)
        pg.draw.polygon(self.sombra, (cor[0]//3, cor[1]//3, cor[2]//3, 180), points_in_texture)
        self.sombra = pg.transform.smoothscale_by(self.sombra, 1/downscale_factor)

    def colide_com_ponto(self, ponto: Vector2 | Sequence[float]) -> bool:
        ponto = _sequence_to_vector2(ponto)  # Garante que ponto é um Vector2

        ponto = self.global_to_local(ponto)
        px, py = ponto.x, ponto.y

        dentro = False
        n = len(self.vertices)
        j = n - 1
        
        for i in range(n):
            if ((self.vertices[i][1] > py) != (self.vertices[j][1] > py)) and \
            (px < self.vertices[i][0] + (self.vertices[j][0] - self.vertices[i][0]) * (py - self.vertices[i][1]) / (self.vertices[j][1] - self.vertices[i][1])):
                dentro = not dentro
            j = i
    
        return dentro
    
    def colide_com_segmento(self, p1: Vector2 | Sequence[float], v: Vector2 | Sequence[float]) -> bool:
        p1 = _sequence_to_vector2(p1)
        v = _sequence_to_vector2(v)
        p1 = self.global_to_local(p1)
        v = v.rotate(-self.rotacao)  # Rotaciona o vetor para o sistema local
        for i in range(len(self.vertices)):
            p3 = self.vertices[i]
            if i == len(self.vertices) - 1:
                p4 = self.vertices[0]
            else:
                p4 = self.vertices[i + 1]

            result = reta_corta_segmento(p3, p4, p1, v)
            if result:
                intersecao, t, k = result
                if 0 <= t <= 1 and 0 <= k <= 1:
                    return True
        return False

    def global_to_local(self, ponto: Vector2) -> Vector2:
        return (ponto - self.posicao).rotate(-self.rotacao)
    
    def local_to_global(self, ponto: Vector2, deslocamento: Vector2 = Vector2(0, 0)) -> Vector2:
        return ponto.rotate(self.rotacao) + self.posicao + deslocamento

    def cortar(self, ponto: Vector2 | Sequence[float | int], v: Vector2 | Sequence[float | int], vel_separacao:float=60) -> list['Poligono']:
        """
        Corta o polígono usando uma linha definida por um ponto e um vetor.

        Args:
            ponto: Ponto por onde passa a linha de corte
            v: Vetor que define a direção da linha de corte

        Returns:
            Tupla com os dois polígonos resultantes do corte (ou None se inválido)
        """
        ponto = _sequence_to_vector2(ponto)  # Garante que ponto é um Vector2
        v = _sequence_to_vector2(v)  # Garante que v é um Vector2

        v_rel = (v - self.velocidade).rotate(-self.rotacao)
        ponto = self.global_to_local(ponto)
        poligonos = [[]]
        ks = [[]]
        for i in range(len(self.vertices)):
            p1 = self.vertices[i]
            if i == len(self.vertices) - 1:
                p2 = self.vertices[0]
            else:
                p2 = self.vertices[i+1]

            result = reta_corta_segmento(p1, p2, ponto, v_rel)
            if result:
                intersecao, t, k = result
                poligonos[-1] += [p1, intersecao]
                poligonos.append([intersecao])
                ks[-1].append(k)
                ks.append([k])
            else:
                poligonos[-1].append(p1)

        poligonos[0] = poligonos[-1] + poligonos[0]
        ks[0] += ks[-1]
        poligonos.pop(-1)
        ks.pop(-1)

        new_poligonos = []
        used_indices = set()
        for start in [0, 1]:
            for i in range(start, len(poligonos), 2):
                for j in range(i+2, len(poligonos), 2):
                    k_i_min = min(ks[i])
                    k_j_min = min(ks[j])
                    k_i_max = max(ks[i])
                    k_j_max = max(ks[j])

                    if (k_i_min < k_j_min and k_i_max > k_j_max) or (k_j_min < k_i_min and k_j_max > k_i_max):
                        new_poligonos.append(poligonos[i] + poligonos[j])
                        used_indices.add(i)
                        used_indices.add(j)

        for i in range(len(poligonos)):
            if i not in used_indices:
                new_poligonos.append(poligonos[i])
        
        out = []
        for vertices in new_poligonos:
            poligono = Poligono(vertices, (self.cor[0] // 3, self.cor[1] // 3, self.cor[2] // 3), self.gravidade, self.tipo)
            baricentro = _baricentro(vertices)
            poligono.posicao = self.local_to_global(baricentro)
            poligono.rotacao = self.rotacao
            poligono.velocidade_rotacao = self.velocidade_rotacao
            poligono.velocidade = self.velocidade + v*0.1

            if (baricentro - ponto).cross(v_rel) < 0:       # Verifica se o poligono esta do lado direito ou do lado esquerdo do corte
                poligono.velocidade += v.rotate(90).normalize() * vel_separacao
                poligono.velocidade_rotacao -= 60
            else:
                poligono.velocidade += v.rotate(270).normalize() * vel_separacao
                poligono.velocidade_rotacao += 60

            out.append(poligono)

        return out
    


    def desenhar(self, tela: pg.Surface) -> None:
        """Desenha o polígono na tela."""
        rotacionada = pg.transform.rotozoom(self.surface, -self.rotacao, 1)
        lado = rotacionada.get_width()
        tela.blit(rotacionada, (self.posicao.x - lado / 2, self.posicao.y - lado / 2))

    def desenhar_com_sombra(self, tela: pg.Surface, deslocamento_sombra: Vector2 = Vector2(5, 5)) -> None:
        """Desenha o polígono com uma sombra."""
        rotacionada = pg.transform.rotozoom(self.sombra, -self.rotacao, 1)
        lado = rotacionada.get_width()
        tela.blit(rotacionada, (self.posicao.x - lado / 2 + deslocamento_sombra.x, self.posicao.y - lado / 2 + deslocamento_sombra.y))
        self.desenhar(tela)

    
def _get_points_from_lengths_and_angles(lengths: Sequence[float], angles: Sequence[float]) -> list[Vector2]:
    """Calcula os pontos de um polígono a partir de comprimentos e ângulos.
    O desenho começa na origem (0, 0) e os ângulos são relativos ao lado anterior.
    O primeiro ângulo é relativo ao eixo x positivo.

    Args:
        lengths (Sequence[float]): Lista de comprimentos dos lados do polígono.
        angles (Sequence[float]): Lista de ângulos em graus.
    """
    assert len(lengths) == len(angles), "Comprimentos e ângulos devem ter o mesmo tamanho."
    pontos = [Vector2(0, 0)]

    angulo = 0
    for i in range(0, len(lengths)):
        angulo += angles[i]
        x = pontos[-1].x + lengths[i] * cos(radians(angulo))
        y = pontos[-1].y - lengths[i] * sin(radians(angulo))
        pontos.append(Vector2(x, y))

    return pontos


class Circulo(Poligono):
    def __init__(self, raio: float, cor: tuple[int, int, int], gravidade: float = 50, tipo: str = "Círculo"):
        self.raio = raio
        vertices = []
        num_vertices = 30
        for i in range(num_vertices):
            angulo = 2 * pi * i / num_vertices
            x = raio * cos(angulo)
            y = raio * sin(angulo)
            vertices.append(Vector2(x, y))
        self.vertices = vertices
        super().__init__(vertices, cor, gravidade, tipo)

class Triangulo(Poligono):
    def __init__(self, p1: Vector2, p2: Vector2, p3: Vector2, cor: tuple[int, int, int], gravidade: float = 50, tipo: str = "Triângulo"):
        super().__init__([p1, p2, p3], cor, gravidade, tipo)

class Retangulo(Poligono):
    def __init__(self, largura: float, altura: float, cor: tuple[int, int, int], gravidade: float = 50, tipo: str = "Retângulo"):
        p1 = Vector2(0, 0)
        p2 = Vector2(largura, 0)
        p3 = Vector2(largura, altura)
        p4 = Vector2(0, altura)
        super().__init__([p1, p2, p3, p4], cor, gravidade, tipo)
        self.largura = largura
        self.altura = altura

class Quadrado(Retangulo):
    def __init__(self, lado: float, cor: tuple[int, int, int], gravidade: float = 50):
        super().__init__(lado, lado, cor, gravidade, "Quadrado")

class TrianguloEquilatero(Triangulo):
    def __init__(self, lado: float, cor: tuple[int, int, int], gravidade: float = 50):
        altura = (lado * (3 ** 0.5)) / 2
        p1 = Vector2(0, -altura / 3)
        p2 = Vector2(-lado / 2, altura * 2 / 3)
        p3 = Vector2(lado / 2, altura * 2 / 3)
        super().__init__(p1, p2, p3, cor, gravidade, "Triângulo Equilátero")
        #self.lado = lado

class TrianguloIsoceles(Triangulo):
    def __init__(self, lado: float, base: float, cor: tuple[int, int, int], gravidade: float = 50):
        altura = (lado ** 2 - (base ** 2) / 4) ** (1/2)
        p1 = Vector2(0, altura)
        p2 = Vector2(-base / 2, 0)
        p3 = Vector2(base / 2, 0)
        super().__init__(p1, p2, p3, cor, gravidade, "Triângulo Isóceles")

class TrianguloRetangulo(Triangulo):
    def __init__(self, altura: float, base: float, cor: tuple[int, int, int], gravidade: float = 50):
        p1 = Vector2(0, altura)
        p2 = Vector2(0, 0)
        p3 = Vector2(base, 0)
        super().__init__(p1, p2, p3, cor, gravidade, "Triângulo Retângulo")


class Estrela(Poligono):
    def __init__(self, tamanho: float, cor: tuple[int, int, int], gravidade: float = 50):
        pontos = []
        for i in range(5):
            angulo = i * (2 * pi / 5) - pi / 2
            x = tamanho * cos(angulo)
            y = tamanho * sin(angulo)
            x2 = (tamanho / 3) * cos(angulo + pi / 5)
            y2 = (tamanho / 3) * sin(angulo + pi / 5)
            pontos.append(Vector2(x, y))
            pontos.append(Vector2(x2, y2))
        super().__init__(pontos, cor, gravidade, "Estrela")

class Angulo(Poligono):
    def __init__(self, tamanho: float, espessura: float, angulo: float, cor: tuple[int, int, int], gravidade: float = 50):
        tamanho_costa = tamanho + espessura * tan(radians(90-angulo/2))
        pontos = _get_points_from_lengths_and_angles(
            [tamanho, espessura, tamanho_costa, tamanho_costa, espessura],
            [180-angulo, -90, -90, -180+angulo, -90]
        )
        super().__init__(pontos, cor, gravidade, "Ângulo")
        self.tamanho = tamanho
        self.angulo = angulo
