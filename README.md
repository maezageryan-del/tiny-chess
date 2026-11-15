# Tiny Chess — tiny-chess-01 entry

A chess engine in 4,067 bytes of Python (`main.py`, standard
library only, no other file read at run time). Negamax search with
alpha-beta pruning, iterative deepening, quiescence on captures,
piece-square tables and a compact material/mobility evaluation,
packed to fit the 4 KB cap. It plays the trial's eight gauntlet
games through the make.fun env and exits when they are over.
Local kit trials: 3.5/6 in a partial run, Elo 1364. MIT-licensed.
