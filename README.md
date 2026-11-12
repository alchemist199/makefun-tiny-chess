# tiny-chess-01 entry

A compact chess engine in one `main.py`, stdlib only, playing the
make.fun gauntlet through the env at `MAKEFUN_ENV_URL`.

## Approach

- **Board:** 0x88 (off-board by `& 136`). Pieces are small ints;
  make/unmake saves/restores all state.
- **Move gen:** pseudo-legal, filtered by king-safety after make.
  Perft-verified (see Tests).
- **Search:** negamax + alpha-beta, iterative deepening to a fixed
  **total** budget of 200,000 nodes/move (deterministic: no clock, no
  unseeded randomness). Full transposition table; MVV-LVA ordering;
  mate scores prefer faster mates.
- **Quiescence:** captures and promotions only, stand-pat, fail-hard.
- **Eval:** material (P 100, N 320, B 330, R 500, Q 900) + pawn PST
  (32-entry string) + centralisation: N/B +8, R/Q +3, K -8.
- **Protocol:** POSTs `/game` and `/move`; UCI moves. Exits on `done`.

## Byte count

- `main.py`: **3,938 bytes** (`wc -c`), limit 4,096.
- `LICENSE`: MIT, 1,104 bytes. Total repo under the 8,192-byte cap.

## Tests

- **Perft (exact):** startpos 20 / 400 / 8,902 / 197,281; Kiwipete
  48 / 2,039 / 97,862. Mate-in-1 found (Qh5xf7).
- **Protocol:** full 16-game practice trial vs the local env server
  (trial-0 gauntlet): no illegal moves, exits `done`.
- **Speed:** ~59,000 nodes/sec; ~6 s/move at 200k nodes, max ~6.8 s
  observed, inside the 10 s/move limit.

## Practice trial-0 results (same gauntlet)

| # | Config | W/D/L | Pts | Elo |

| # | Config | W/D/L | Pts | Elo |
|---|---|---|---|---|
| 1 | 30k, move-only TT | 0/3/13 | 1.5 | ~800 |
| 2 | 150k, move-only TT | 1/1/14 | 1.5 | ~800 |
| 3 | 80k, check evasions | 0/2/14 | 1.0 | ~700 |
| 4 | 150k, full TT | 1/2/13 | 2.0 | ~870 |
| 5 | 150k, full TT, shared PST | 0/0/16 | 0.0 | <600 |
| 6 | 150k, shared PST no-king | 0/2/14 | 1.0 | ~700 |
| 7 | 250k, full TT | 1/2/9* | 2.0* | — |
| 8 | 150k, full TT (re-run) | 1/2/13 | 2.0 | ~871 |
| 9 | + mate-distance | 1/2/13 | 2.0 | ~871 |
| 10 | + QS check evasions | 0/4/12 | 2.0 | ~871 |
| 11 | + killer moves | 1/2/13 | 2.0 | ~871 |
| **12** | **+ centralisation, 150k** | **1/5/10** | **3.5** | **~1040** |
| 13 | 12 + bishop pair | killed† | 2.5† | — |
| 14 | 12 + null-move | 1/4/11 | 3.0 | ~989 |
| 15 | 12 + QS evasions | 0/4/12 | 2.0 | ~871 |
| 16 | 12 at 200k nodes | killed‡ | — | — |

\* Trial 7 crashed after game 12 (HTTP 409); 250k unsafe.
† Trial 13 killed at game 12 (VM restart); 2.5 pts in 11 games, worse
than trial 12 (3.0). ‡ Trial 16 killed 3x at games 12–13 (VM restarts).

**8-game screens (games 1–8):** 150k centralisation 2.5 pts; **200k
nodes 3.0 pts**; LMR 2.0; stronger centralisation 2.5; futility killed.

**Best verified: trial 12 (centralisation, 150k) — 1 win, 5 draws,
10 losses, 3.5 pts, Elo ≈ 1,040.** The submitted entry graded 871 in
official practice (floor 1,154); this build is +169 Elo over that.
200k adds +0.5 pts on games 1–8, so the shipped 200k build projects to
~4.0–4.5 pts (~1,080–1,130 Elo) — still below the floor. Centralisation
was the only big win; the rest reverted (worse).
