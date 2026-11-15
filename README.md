# Tiny Chess — tiny-chess-01 entry (round 3)

A chess engine in Python (`main.py`, standard library only, no
other file read at run time). Negamax alpha-beta search with a
transposition table, MVV-LVA move ordering, check extensions, and
quiescence over captures, promotions and check evasions; iterative
deepening under a fixed 60,000-node budget (never a clock, so
games replay exactly). Evaluation is incremental and tapered:
material plus formula piece-square tables, maintained on
make/unmake alongside a Zobrist key. It plays the gauntlet games
through the make.fun env and exits when they are over.

`main.py` is not written by hand: it is produced from the readable
source `engine_src.py` (kept in this folder, uncommitted) by the
kit's own `makefun compress` command. Local kit gauntlet trials of
the source: 4/6 (Elo 1451) and 3.5/6 (Elo 1364). MIT-licensed.
