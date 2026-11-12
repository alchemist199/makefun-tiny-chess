# tiny-chess-01 entry

A compact chess engine in one `main.py` (4,082 bytes), stdlib only.
It plays the make.fun gauntlet through the env at `MAKEFUN_ENV_URL`.

## Approach

- **Board:** 0x88 (off-board by `& 136`). Pieces are small ints
  (white 1..6, black -1..-6). King squares, castling, en-passant are
  globals saved/restored by make/unmake.
- **Move gen:** pseudo-legal, filtered by a king-safety test after make.
  Pawns (push, double push, captures, en passant, all promotions),
  sliders/leapers from one direction table, table-driven castling.
- **Search:** negamax + alpha-beta, iterative deepening to a fixed
  **total** node budget of 150,000 nodes/move (deterministic: no clock,
  no unseeded randomness). A **full** transposition table (depth, score,
  bound flag, best move) gives score cutoffs and ordering; captures
  ordered by MVV-LVA.
- **Quiescence:** captures and promotions only, stand-pat, fail-hard.
- **Eval:** material (P 100, N 320, B 330, R 500, Q 900) + a pawn
  piece-square table (32-entry string, files mirrored). Mate is a flat
  -9990; no mate-distance bonus.
- **Protocol:** POSTs `/game` and `/move` via `urlopen(url, data)`.
  UCI moves; castling is the king's move. Exits on `done`.

## Tests

- **Perft (exact):** startpos 20 / 400 / 8,902 / 197,281; Kiwipete
  48 / 2,039 / 97,862. Cross-checked vs python-chess (depths 0–2).
  Mate-in-1 found (Qh5xf7).
- **Protocol:** full 16-game practice trial vs the local env server
  (trial-0 gauntlet): no illegal moves, exits `done`.
- **Speed:** ~59,000 nodes/sec; ~2.5 s/move at 150k nodes, inside the
  10 s/move limit. A full trial takes ~26 min.

## Practice trial-0 results (same gauntlet, 7 builds)

| Trial | Config | W/D/L | Pts | Elo |
|---|---|---|---|---|
| 1 | 30k/iter, move-only TT | 0/3/13 | 1.5 | ~800 |
| 2 | 150k, move-only TT | 1/1/14 | 1.5 | ~800 |
| 3 | 80k, check evasions | 0/2/14 | 1.0 | ~700 |
| **4** | **150k, full TT** | **1/2/13** | **2.0** | **~870** |
| 5 | 150k, full TT, shared PST | 0/0/16 | 0.0 | <600 |
| 6 | 150k, full TT, shared PST no-king | 0/2/14 | 1.0 | ~700 |
| 7 | 250k, full TT | 1/2/9* | 2.0* | — |

\* Trial 7 crashed after game 12 (HTTP 409); games 1 and 12 lost on
time, 13–16 unplayed. 250k is unsafe — reverted to 150k.

**Best: trial 4 — 1 win (vs depth-2, by checkmate), 2 draws, 13 losses,
2.0 pts, Elo ≈ 870.** Sunfish baseline ~1,360 Elo, so ~490 below it.
Full TT was the only clear win (+70 Elo). Sharing the pawn PST hurt
(trial 5: 0 pts — it centralises the king).

## Trade-offs

Omitted for 4,096 bytes: N/B/R/Q/K PSTs, bishop-pair bonus, killer
ordering, quiescence check evasions, mate-distance scoring.
