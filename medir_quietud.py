"""Reto 9: prueba la quietud en una posición trampa y mide lo que tarda."""
import time

import chess

from grupoGKPG.minimax import Minimax

# La dama puede comerse el peón de c6, pero b7 lo defiende.
TRAMPA = "4k3/1p6/2p5/8/8/8/8/2Q1K3 w - - 0 1"

# Posiciones de medio juego para medir el tiempo.
POSICIONES = [
    "r1bqk1nr/pppp1ppp/2n5/2b1p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 4 4",
    "r1bq1rk1/ppp2ppp/2np1n2/2b1p3/2B1P3/2NP1N2/PPP2PPP/R1BQ1RK1 w - - 0 7",
    "rnbqkb1r/pp2pppp/3p1n2/8/3NP3/8/PPP2PPP/RNBQKB1R w KQkq - 1 5",
    "r2qkb1r/ppp2ppp/2n1bn2/3pp3/3PP3/2N1BN2/PPP2PPP/R2QKB1R w KQkq - 0 6",
]


def trampa():
    print("Posición trampa: ¿se come el peón defendido de c6 con la dama?")
    for profundidad in [1, 2]:
        for quieta in [False, True]:
            jugador = Minimax(profundidad=profundidad, quieta=quieta)
            tablero = chess.Board(TRAMPA)
            jugada = jugador.elegir(tablero, 1)
            print("  profundidad", profundidad, "quietud", quieta,
                  "-> juega", tablero.san(jugada), "y cree que va", jugador.mejor_valor)
    print()


def tiempos():
    print("Segundos por jugada:")
    for profundidad in [1, 2, 3]:
        for quieta in [False, True]:
            segundos = []
            for fen in POSICIONES:
                jugador = Minimax(profundidad=profundidad, quieta=quieta)
                inicio = time.perf_counter()
                jugador.elegir(chess.Board(fen), 1)
                segundos.append(time.perf_counter() - inicio)
            media = sum(segundos) / len(segundos)
            print("  profundidad", profundidad, "quietud", quieta,
                  "-> media", round(media, 3), "máximo", round(max(segundos), 3))


if __name__ == "__main__":
    trampa()
    tiempos()
