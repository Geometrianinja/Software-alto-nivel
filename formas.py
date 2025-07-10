from abc import ABC, abstractmethod
import pygame as pg
from pygame.math import Vector2
from typing import Sequence, Optional
from math import pi, cos, sin, radians, tan, atan2
from enum import Enum
from typing import List
from typing import Dict
from typing import Tuple

def angulo_anti_horario(v1: Vector2, v2: Vector2) -> float:
    """
    Calcula o ângulo entre dois vetores no sentido anti-horário.
    
    Args:
        v1: Primeiro vetor
        v2: Segundo vetor
    
    Returns:
        Ângulo em graus (0 a 360) no sentido anti-horário de v1 para v2
    """
    cross = v1.cross(v2)
    dot = v1.dot(v2)
    return atan2(cross, dot) * (180 / pi) % 360


def reta_corta_segmento(p1: Vector2, p2: Vector2, p0: Vector2, v0: Vector2) -> Optional[Tuple[Vector2, float, float]]:
    """
    Verifica se um segmento (p1->p2) intersecta uma reta (p0 + t*v0).
    
    Returns:
        Tuple[Vector2, float, float] | None: (ponto_intersecao, t_segmento, t_reta) ou None
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

class TipoForma(Enum):
    FORMA = -1
    POLIGONO = 0
    CIRCULO = 1
    RETANGULO = 2
    QUADRADO = 3
    TRIANGULO = 4
    TRIANGULO_EQUILATERO = 5
    TRIANGULO_ISOCELES = 6
    TRIANGULO_RETANGULO = 7
    ESTRELA = 8
    ANGULO = 9
    PARALELOGRAMO = 10
    LOSANGO = 11
    TRAPEZIO = 12

class Forma(ABC):
    def __init__(self, cor, gravidade: float = 50):
        self.cor: Tuple[int, int, int] = cor
        self.gravidade: float = gravidade
        self.posicao: Vector2 = Vector2(0, 0)
        self.velocidade: Vector2 = Vector2(0, 0)
        self.rotacao: float = 0.0
        self.velocidade_rotacao: float = 0.0
        self.tipos: List[TipoForma] = [TipoForma.FORMA]

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
    def cortar(self, ponto: Vector2 | Sequence[float | int], v: Vector2 | Sequence[float | int]) -> List['Forma']:
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
    
    def is_tipo(self, tipo: TipoForma) -> bool:
        """Verifica se a forma é do tipo especificado."""
        return tipo in self.tipos

    def get_tipo_especifico(self):
        return self.tipos[-1]

def _baricentro(vertices: Sequence[Vector2]) -> Vector2:
    """Calcula o baricentro (centroide) de um polígono usando a fórmula da área com coordenadas."""
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
    def __init__(self, vertices: Sequence[Vector2], cor: tuple[int, int, int], gravidade: float = 50, iguais:List[List[int]]=[], angulos_iguais:List[List[int]]=[], angulos_retos:List[int]=[]):
        """
            iguais: lista de listas de indices de lados iguais
            vertices: lista de vetores representando os vértices do polígono no sentido horario
        """
        super().__init__(cor, gravidade)
        self.tipos.append(TipoForma.POLIGONO)
        baricentro = _baricentro(vertices)
        self.vertices = [v - baricentro for v in vertices]

        downscale_factor = 2
        self.lado = max(max(abs(v.x), abs(v.y)) for v in self.vertices) * 2 * downscale_factor + 4
        tamanho_marca = self.lado*0.06
        self.lado += int(tamanho_marca * 2)  # Garante que a superfície seja grande o suficiente para as marcas
        self.surface = pg.Surface((self.lado, self.lado), pg.SRCALPHA)
        points_in_texture = [v*downscale_factor + Vector2(self.lado/2, self.lado/2) for v in self.vertices]
        pg.draw.polygon(self.surface, cor, points_in_texture)
        pg.draw.lines(self.surface, (0, 0, 0), True, points_in_texture, width=3)

        Poligono.put_ticks_on_surface(self.surface, points_in_texture, iguais, tamanho_marca, tamanho_marca/2)
        Poligono.put_right_angles_on_surface(self.surface, points_in_texture, angulos_retos, tamanho_marca*1.5)
        Poligono.put_equal_angles_on_surface(self.surface, points_in_texture, angulos_iguais, tamanho_marca*1.5)

        self.surface=pg.transform.smoothscale_by(self.surface, 1/downscale_factor)
        self.sombra = pg.Surface((self.lado, self.lado), pg.SRCALPHA)
        pg.draw.polygon(self.sombra, (cor[0]//3, cor[1]//3, cor[2]//3, 180), points_in_texture)
        self.sombra = pg.transform.smoothscale_by(self.sombra, 1/downscale_factor)

    @classmethod
    def put_ticks_on_surface(cls, surface, points: List[Vector2], iguais: List[List[int]], length, separation):
        for idx, vertices_idxs in enumerate(iguais):
            ds = [-idx*separation/2 + n*separation for n in range(idx+1)]
            for vertice_id in vertices_idxs:
                v1 = points[vertice_id]
                v2 = points[(vertice_id+1) % len(points)]
                middle = v1.lerp(v2, 0.5)
                u = (v2-v1).normalize()
                up = u.rotate(90) * length/2
                down = u.rotate(-90) * length/2
                for d in ds:
                    pg.draw.line(surface, (0, 0, 0), middle+u*d+up, middle+u*d+down, width=4)

    @classmethod
    def put_equal_angles_on_surface(cls, surface, points: List[Vector2], angulos_iguais: List[List[int]], radius, separation_angle = 15):
        for idx, vertices_idxs in enumerate(angulos_iguais):
            angs_ticks = [-idx*separation_angle/2 + n*separation_angle for n in range(idx+1)]
            for vertice_id in vertices_idxs:
                v1 = points[vertice_id-1]
                v2 = points[(vertice_id)]
                v3 = points[(vertice_id+1) % len(points)]
                angulo = angulo_anti_horario(v1 - v2, v3-v2)
                angs = [i/20 * angulo for i in range(20+1)]
                w0 = (v1-v2).normalize() * radius
                ws = [w0.rotate(ang) for ang in angs]
                pg.draw.lines(surface, (0, 0, 0), False, [v2 + w for w in ws], width=4)
                for ang in angs_ticks:
                    w1 = w0.rotate(angulo/2+ang)
                    pg.draw.line(surface, (0, 0, 0), v2 + w1*0.6, v2 + w1 * 1.4, width=4)


    @classmethod
    def put_right_angles_on_surface(cls, surface, points: List[Vector2], angulos_retos: List[int], length):
        for idx, vertice_id in enumerate(angulos_retos):
            v1 = points[vertice_id-1]
            v2 = points[vertice_id]
            v3 = points[(vertice_id+1) % len(points)]
            u1 = (v1 - v2).normalize()
            u2 = (v3 - v2).normalize()
            w1 = u1* length
            w2 = u2 * length
            pg.draw.lines(surface, (0, 0, 0), False, [v2+w1, v2+w1+w2, v2+w2], width=4)
            pg.draw.circle(surface, (0, 0, 0), v2 + w1/2 + w2/2, 3)
            

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

    def cortar(self, ponto: Vector2 | Sequence[float | int], v: Vector2 | Sequence[float | int], vel_separacao:float=60) -> List['Poligono']:
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
            poligono = Poligono(vertices, (self.cor[0] // 3, self.cor[1] // 3, self.cor[2] // 3), self.gravidade)
            baricentro = _baricentro(vertices)
            poligono.posicao = self.local_to_global(baricentro)
            poligono.rotacao = self.rotacao
            poligono.velocidade_rotacao = self.velocidade_rotacao
            poligono.velocidade = self.velocidade + v*0.1

            if (baricentro - ponto).cross(v_rel) < 0:  # Verifica se o poligono esta do lado direito ou do lado esquerdo do corte
                v_rot = v.rotate(90)
                if v_rot.length() != 0:
                    poligono.velocidade += v_rot.normalize() * vel_separacao
                else:
                    poligono.velocidade += Vector2(vel_separacao, 0)
                poligono.velocidade_rotacao -= 60
            else:
                v_rot = v.rotate(270)
                if v_rot.length() != 0:
                    poligono.velocidade += v_rot.normalize() * vel_separacao
                else:
                    poligono.velocidade += Vector2(vel_separacao, 0)
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

    
def _get_points_from_lengths_and_angles(lengths: Sequence[float], angles: Sequence[float]) -> List[Vector2]:
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
    def __init__(self, raio: float, cor: tuple[int, int, int], gravidade: float = 50):
        self.raio = raio
        vertices = []
        num_vertices = 30
        for i in range(num_vertices):
            angulo = 2 * pi * i / num_vertices
            x = raio * cos(angulo)
            y = raio * sin(angulo)
            vertices.append(Vector2(x, y))
        self.vertices = vertices
        super().__init__(vertices, cor, gravidade)
        self.tipos.append(TipoForma.CIRCULO)

class Retangulo(Poligono):
    def __init__(self, largura: float, altura: float, cor: tuple[int, int, int], gravidade: float = 50, **kwargs):
        p1 = Vector2(0, 0)
        p2 = Vector2(largura, 0)
        p3 = Vector2(largura, altura)
        p4 = Vector2(0, altura)
        
        # Set default values, but allow kwargs to override them
        default_kwargs = {
            'iguais': [[0, 2], [1, 3]], 
            'angulos_retos': [0, 1, 2, 3]
        }
        default_kwargs.update(kwargs)
        
        super().__init__([p1, p2, p3, p4], cor, gravidade, **default_kwargs)
        self.tipos.append(TipoForma.RETANGULO)
        self.largura = largura
        self.altura = altura

class Quadrado(Retangulo):
    def __init__(self, lado: float, cor: tuple[int, int, int], gravidade: float = 50, **kwargs):
        super().__init__(lado, lado, cor, gravidade, iguais=[[0, 1, 2, 3]], **kwargs)
        self.tipos.append(TipoForma.LOSANGO)
        self.tipos.append(TipoForma.QUADRADO)

class Paralelogramo(Poligono):
    def __init__(self, lado1: float, lado2: float, angulo: float, cor: tuple[int, int, int], gravidade: float = 50):
        pontos = _get_points_from_lengths_and_angles([lado1, lado2, lado1], [angulo, 180 - angulo, angulo])
        super().__init__(pontos, cor, gravidade, iguais=[[0, 2], [1, 3]], angulos_iguais=[[0, 2], [1, 3]])
        self.tipos.append(TipoForma.PARALELOGRAMO)

class Losango(Poligono):
    def __init__(self, lado: float, angulo: float, cor: tuple[int, int, int], gravidade: float = 50):
        pontos = _get_points_from_lengths_and_angles([lado, lado, lado], [angulo, 180 - angulo, angulo])
        super().__init__(pontos, cor, gravidade, iguais=[[0, 1, 2, 3]], angulos_iguais=[[0, 1], [2, 3]])
        self.tipos.append(TipoForma.PARALELOGRAMO)
        self.tipos.append(TipoForma.LOSANGO)


class Triangulo(Poligono):
    def __init__(self, p1: Vector2, p2: Vector2, p3: Vector2, cor: tuple[int, int, int], gravidade: float = 50, **kwargs):
        super().__init__([p1, p2, p3], cor, gravidade, **kwargs)
        self.tipos.append(TipoForma.TRIANGULO)

class TrianguloEquilatero(Triangulo):
    def __init__(self, lado: float, cor: tuple[int, int, int], gravidade: float = 50):
        altura = (lado * (3 ** 0.5)) / 2
        p1 = Vector2(0, -altura / 3)
        p2 = Vector2(-lado / 2, altura * 2 / 3)
        p3 = Vector2(lado / 2, altura * 2 / 3)
        super().__init__(p1, p2, p3, cor, gravidade, iguais=[[0, 1, 2]], angulos_iguais=[[0, 1, 2]])
        self.tipos.append(TipoForma.TRIANGULO_EQUILATERO)

class TrianguloIsoceles(Triangulo):
    def __init__(self, lado: float, base: float, cor: tuple[int, int, int], gravidade: float = 50):
        altura = (lado ** 2 - (base ** 2) / 4) ** (1/2)
        p1 = Vector2(0, altura)
        p2 = Vector2(-base / 2, 0)
        p3 = Vector2(base / 2, 0)
        super().__init__(p1, p2, p3, cor, gravidade, iguais=[[0, 2]])
        self.tipos.append(TipoForma.TRIANGULO_ISOCELES)

class TrianguloRetangulo(Triangulo):
    def __init__(self, altura: float, base: float, cor: tuple[int, int, int], gravidade: float = 50):
        p1 = Vector2(0, altura)
        p2 = Vector2(0, 0)
        p3 = Vector2(base, 0)
        super().__init__(p1, p2, p3, cor, gravidade, angulos_retos=[1])
        self.tipos.append(TipoForma.TRIANGULO_RETANGULO)


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
        super().__init__(pontos, cor, gravidade)
        self.tipos.append(TipoForma.ESTRELA)

class Angulo(Poligono):
    def __init__(self, tamanho: float, espessura: float, angulo: float, cor: tuple[int, int, int], gravidade: float = 50):
        tamanho_costa = tamanho + espessura * tan(radians(90-angulo/2))
        pontos = _get_points_from_lengths_and_angles(
            [tamanho, espessura, tamanho_costa, tamanho_costa, espessura],
            [180-angulo, -90, -90, -180+angulo, -90]
        )
        super().__init__(pontos, cor, gravidade)
        self.tipos.append(TipoForma.ANGULO)
        self.tamanho = tamanho
        self.angulo = angulo