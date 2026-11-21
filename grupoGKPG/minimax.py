"""Minimax con poda alfa-beta para ajedrez. Grupo GKPG.

Es la primera parte de la guía. Cada función con
    raise NotImplementedError
es un hueco. Cuando rellenéis el del paso A1, A2 o A3, comprobadlo con
    python comprobar.py a1
(o, en VS Code, "Comprobar paso…" en Ejecutar y depurar).
"""
import math
import random

import chess

from ajedrez import VALOR, material

MATE = 1000     # más que todo el material junto: un mate vale más que cualquier ventaja

# ---------------------------------------------------------------- paso A1
def evaluar(tablero, color):
    if tablero.is_checkmate():
        return -MATE if tablero.turn == color else MATE
    if tablero.is_stalemate() or tablero.is_insufficient_material():
        return 0
    return material(tablero, color)


# ---------------------------------------------------------------- paso A2
def minimax(tablero, profundidad, color, evaluar=evaluar):
    if profundidad == 0 or tablero.is_game_over():
        return evaluar(tablero, color)
    valores = []
    for jugada in tablero.legal_moves:
        tablero.push(jugada)
        valores.append(minimax(tablero, profundidad - 1, color, evaluar))
        tablero.pop()
    return max(valores) if tablero.turn == color else min(valores)


# ---------------------------------------------------------------- paso A3
def alfabeta(tablero, profundidad, color, alfa=-math.inf, beta=math.inf, evaluar=evaluar, quieta=False):
    if tablero.is_game_over():
        return evaluar(tablero, color)
    if profundidad == 0:
        if quieta:                                     # reto 9
            return quietud(tablero, color, alfa, beta, evaluar)
        return evaluar(tablero, color)
    if tablero.turn == color:                        # MAX
        mejor = -math.inf
        for jugada in ordenar(tablero, list(tablero.legal_moves)):
            tablero.push(jugada)
            mejor = max(mejor, alfabeta(tablero, profundidad - 1, color, alfa, beta, evaluar, quieta))
            tablero.pop()
            alfa = max(alfa, mejor)
            if alfa >= beta:
                break
        return mejor
    mejor = math.inf                                   # MIN
    for jugada in ordenar(tablero, list(tablero.legal_moves)):
        tablero.push(jugada)
        mejor = min(mejor, alfabeta(tablero, profundidad - 1, color, alfa, beta, evaluar, quieta))
        tablero.pop()
        beta = min(beta, mejor)
        if alfa >= beta:
            break
    return mejor


# ---------------------------------------------------------------- reto 9: búsqueda de quietud
def quietud(tablero, color, alfa=-math.inf, beta=math.inf, evaluar=evaluar):
    """Sigue mirando sólo capturas hasta que no quede ninguna.
    Parte de evaluar, porque no está obligado a capturar."""
    mejor = evaluar(tablero, color)                    # lo que vale si no captura
    if tablero.turn == color:                        # MAX
        alfa = max(alfa, mejor)
        if alfa >= beta:
            return mejor
        for jugada in capturas_ordenadas(tablero):
            tablero.push(jugada)
            mejor = max(mejor, quietud(tablero, color, alfa, beta, evaluar))
            tablero.pop()
            alfa = max(alfa, mejor)
            if alfa >= beta:
                break
        return mejor
    beta = min(beta, mejor)                            # MIN
    if alfa >= beta:
        return mejor
    for jugada in capturas_ordenadas(tablero):
        tablero.push(jugada)
        mejor = min(mejor, quietud(tablero, color, alfa, beta, evaluar))
        tablero.pop()
        beta = min(beta, mejor)
        if alfa >= beta:
            break
    return mejor


def capturas_ordenadas(tablero):
    """Las capturas: primero la víctima más valiosa y, a igual víctima, el atacante más barato."""
    capturas = []
    for jugada in tablero.legal_moves:
        if tablero.is_capture(jugada):
            capturas.append(jugada)

    def puntos(captura):
        if tablero.is_en_passant(captura):
            victima = 1                                # al paso: se come un peón
        else:
            victima = VALOR[tablero.piece_at(captura.to_square).piece_type]
        atacante = VALOR[tablero.piece_at(captura.from_square).piece_type]
        return 10 * victima - atacante

    return sorted(capturas, key=puntos, reverse=True)


# ---------------------------------------------------------------- hecho: el orden y el jugador
def ordenar(tablero, jugadas):
    """Las capturas primero, y entre ellas las de la pieza más valiosa: así la poda corta antes."""
    def valor_capturado(j):
        pieza = tablero.piece_at(j.to_square)
        return VALOR[pieza.piece_type] if pieza else (1 if tablero.is_en_passant(j) else 0)
    return sorted(jugadas, key=valor_capturado, reverse=True)


class Minimax:
    """El jugador. `profundidad` son las medias jugadas que mira, contando la suya; con
    `poda=False` usa minimax a secas (para comparar lo que tardan); `evaluar` es la heurística;
    `quieta=True` usa la búsqueda de quietud (reto 9)."""

    def __init__(self, nombre="grupoGKPG-ab", profundidad=2, poda=True, evaluar=evaluar, quieta=False):
        self.nombre = nombre
        self.profundidad = profundidad
        self.poda = poda
        self.quieta = quieta
        self.evaluar = evaluar      # la heurística: otra función con la misma forma, para probar la vuestra

    def valor(self, tablero, color, alfa=-math.inf):
        """El valor de la posición después de una jugada: lo que diga la búsqueda que toque."""
        if self.poda:
            return alfabeta(tablero, self.profundidad - 1, color, alfa=alfa,
                            evaluar=self.evaluar, quieta=self.quieta)
        return minimax(tablero, self.profundidad - 1, color, evaluar=self.evaluar)

    def elegir(self, tablero, tiempo):
        color = tablero.turn
        mejor, mejores = -math.inf, []
        for jugada in ordenar(tablero, list(tablero.legal_moves)):
            tablero.push(jugada)
            # poda con la mejor hasta ahora; el -1e-6 es para no perder los empates
            v = self.valor(tablero, color, alfa=mejor - 1e-6)
            tablero.pop()
            if v > mejor:
                mejor, mejores = v, [jugada]
            elif v == mejor:
                mejores.append(jugada)
        self.mejor_valor = mejor
        return random.choice(mejores)       # entre las que empatan, una al azar: así no juega siempre igual
