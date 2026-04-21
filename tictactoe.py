"""
tictactoe.py - Tic-Tac-Toe Spiellogik auf 3x3 Spielfeld
Spieler: HUMAN = 1, AI = -1
Gewinnt, wer zuerst 3 in einer Reihe hat (horizontal, vertikal, diagonal)
"""

import copy
from minimax import SCORE_WIN, SCORE_LOSS, SCORE_DRAW

BOARD_SIZE = 3
EMPTY = 0
HUMAN = 1
AI = -1
WIN_LENGTH = 3  # 3 in einer Reihe


def create_board():
    """Erstellt ein leeres 3x3 Spielfeld."""
    return [[EMPTY] * BOARD_SIZE for _ in range(BOARD_SIZE)]


def get_valid_moves(board, is_maximizing):
    """
    Gibt alle freien Felder als mögliche Züge zurück.
    Zug-Format: (row, col)
    """
    moves = []
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == EMPTY:
                moves.append((row, col))
    return moves


def apply_move(board, move, is_maximizing):
    """
    Wendet einen Zug auf das Spielfeld an und gibt eine Kopie zurück.
    """
    new_board = copy.deepcopy(board)
    row, col = move
    new_board[row][col] = AI if is_maximizing else HUMAN
    return new_board


def _check_three_in_a_row(board, player):
    """Prüft ob der gegebene Spieler 3 in einer Reihe hat."""
    # Horizontal
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE - WIN_LENGTH + 1):
            if all(board[row][col + k] == player for k in range(WIN_LENGTH)):
                return True

    # Vertikal
    for row in range(BOARD_SIZE - WIN_LENGTH + 1):
        for col in range(BOARD_SIZE):
            if all(board[row + k][col] == player for k in range(WIN_LENGTH)):
                return True

    # Diagonal (oben-links nach unten-rechts)
    for row in range(BOARD_SIZE - WIN_LENGTH + 1):
        for col in range(BOARD_SIZE - WIN_LENGTH + 1):
            if all(board[row + k][col + k] == player for k in range(WIN_LENGTH)):
                return True

    # Diagonal (oben-rechts nach unten-links)
    for row in range(BOARD_SIZE - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, BOARD_SIZE):
            if all(board[row + k][col - k] == player for k in range(WIN_LENGTH)):
                return True

    return False


def is_terminal(board):
    """
    Prüft ob das Spiel beendet ist.
    Rückgabe: (terminal: bool, score: int)
    """
    if _check_three_in_a_row(board, AI):
        return True, SCORE_WIN
    if _check_three_in_a_row(board, HUMAN):
        return True, SCORE_LOSS

    # Unentschieden wenn alle Felder belegt
    if all(board[r][c] != EMPTY for r in range(BOARD_SIZE) for c in range(BOARD_SIZE)):
        return True, SCORE_DRAW

    return False, 0


def evaluate(board):
    """
    Bewertet das Spielfeld aus KI-Sicht.
    Auf 3x3 ist Minimax bereits perfekt; Mittelfeld leicht bevorzugen.
    """
    score = 0
    center = BOARD_SIZE // 2
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == AI:
                dist = abs(row - center) + abs(col - center)
                score += max(0, 2 - dist)
            elif board[row][col] == HUMAN:
                dist = abs(row - center) + abs(col - center)
                score -= max(0, 2 - dist)
    return score


def check_winner(board):
    """
    Gibt den Gewinner zurück.
    Rückgabe: 'human' | 'ai' | 'draw' | None
    """
    if _check_three_in_a_row(board, AI):
        return 'ai'
    if _check_three_in_a_row(board, HUMAN):
        return 'human'
    if all(board[r][c] != EMPTY for r in range(BOARD_SIZE) for c in range(BOARD_SIZE)):
        return 'draw'
    return None


RULES_EN = """TIC-TAC-TOE - Rules

Played on a 3x3 board.
You play X, the AI plays O.

HOW TO PLAY:
- Take turns placing your piece on any empty square.
- You go first.

WIN CONDITION:
- The first player to get 3 of their pieces in a row
  (horizontal, vertical, or diagonal) wins.

DRAW:
- If all 9 squares are filled with no winner,
  the game is a draw."""

RULES_DE = """TIC-TAC-TOE - Regeln

Gespielt auf einem 3x3 Spielfeld.
Du spielst X, die KI spielt O.

SPIELWEISE:
- Spieler setzen abwechselnd einen Stein auf ein freies Feld.
- Du beginnst.

GEWINNBEDINGUNG:
- Wer zuerst 3 Steine in einer Reihe (horizontal, vertikal
  oder diagonal) hat, gewinnt.

UNENTSCHIEDEN:
- Wenn alle 9 Felder belegt sind ohne Gewinner,
  ist es unentschieden."""
