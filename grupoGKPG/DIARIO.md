Diario de GKPG · Práctica 5

Integrantes: ZhuoKai Zhu, Gonzalo Laso, Peng Gonzalo, Gabriel Barroso.
Juego: ajedrez (python-chess). Alfa-beta y MCTS.
Rivales: los de referencia (Aleatorio, Voraz, AlfaBeta2). 16 partidas por rival (8 aperturas x 2 colores),
TIEMPO 1 s por jugada en comparar.py.

21/11 -> Reto 9: búsqueda de quietud (dorado, alfa-beta)
- quietud() en minimax.py: en profundidad 0 sigue mirando solo capturas (ordenadas por MVV-LVA) hasta que
  no queda ninguna, partiendo de evaluar. Se activa con Minimax(profundidad=..., quieta=True).
- Para que quepa en el tiempo, elegir pasa como alfa el valor de la mejor jugada de la raíz (mismas jugadas,
  ab3-quietud de 2,46 s a 0,48 s por jugada).
- Comprobado en medir_quietud.py: sin quietud ab1 se come con la dama un peón defendido; con quietud no.

-RESULTADOS -> comparar.py (TIEMPO 1 s, 16 partidas por rival)
                          Aleatorio                 Voraz             AlfaBeta2         TOTAL
ab1                100% ±0 (16-0-0)       44% ±18 (3-8-5)        0% ±0 (0-0-16)       48% ±13
ab1-quietud        100% ±0 (16-0-0)      100% ±0 (16-0-0)       59% ±16 (5-9-2)        86% ±8
ab2                100% ±0 (16-0-0)      100% ±0 (16-0-0)       53% ±21 (6-5-5)        84% ±9
ab2-quietud        100% ±0 (16-0-0)      100% ±0 (16-0-0)      88% ±11 (12-4-0)        96% ±4
ab3                 97% ±6 (15-1-0)      100% ±0 (16-0-0)       97% ±6 (15-1-0)        98% ±3
ab3-quietud        100% ±0 (16-0-0)      100% ±0 (16-0-0)       97% ±6 (15-1-0)        99% ±2

- Como vemos, la quietud mejora mucho a igual profundidad (contra AlfaBeta2: ab1 0% -> 59%, ab2 53% -> 88%),
  y con un nivel menos ab2-quietud (96%) iguala a ab3 (98%), dentro del margen.
- ab3-quietud no vale: 36 de 1283 jugadas pasan de 1,5 s (pierde por tiempo en partida estricta).
  Nos quedamos con ab2-quietud (máximo 0,55 s).
