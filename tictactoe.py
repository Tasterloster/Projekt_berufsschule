"""
tictactoe.py - Tic-Tac-Toe / 4-gewinnt Spiellogik auf 6x6 Spielfeld
Spieler: HUMAN = 1, AI = -1
Gewinnt, wer zuerst 4 in Reihe hat (horizontal, vertikal, diagonal)
"""

import copy
from minimax import SCORE_WIN, SCORE_LOSS, SCORE_DRAW

BOARD_SIZE = 6
EMPTY = 0
HUMAN = 1
AI = -1
WIN_LENGTH = 4  # 4 in einer Reihe


def create_board():
    """Erstellt ein leeres 6x6 Spielfeld."""
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


def _check_four_in_a_row(board, player):
    """Prüft ob der gegebene Spieler 4 in einer Reihe hat."""
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
    if _check_four_in_a_row(board, AI):
        return True, SCORE_WIN
    if _check_four_in_a_row(board, HUMAN):
        return True, SCORE_LOSS

    # Unentschieden wenn alle Felder belegt
    if all(board[r][c] != EMPTY for r in range(BOARD_SIZE) for c in range(BOARD_SIZE)):
        return True, SCORE_DRAW

    return False, 0


def _count_lines(board, player, length):
    """Zählt Linien der gegebenen Länge für Bewertungsfunktion."""
    count = 0
    opponent = HUMAN if player == AI else AI

    # Horizontal
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE - WIN_LENGTH + 1):
            window = [board[row][col + k] for k in range(WIN_LENGTH)]
            if window.count(player) == length and window.count(opponent) == 0:
                count += 1

    # Vertikal
    for row in range(BOARD_SIZE - WIN_LENGTH + 1):
        for col in range(BOARD_SIZE):
            window = [board[row + k][col] for k in range(WIN_LENGTH)]
            if window.count(player) == length and window.count(opponent) == 0:
                count += 1

    # Diagonal (\)
    for row in range(BOARD_SIZE - WIN_LENGTH + 1):
        for col in range(BOARD_SIZE - WIN_LENGTH + 1):
            window = [board[row + k][col + k] for k in range(WIN_LENGTH)]
            if window.count(player) == length and window.count(opponent) == 0:
                count += 1

    # Diagonal (/)
    for row in range(BOARD_SIZE - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, BOARD_SIZE):
            window = [board[row + k][col - k] for k in range(WIN_LENGTH)]
            if window.count(player) == length and window.count(opponent) == 0:
                count += 1

    return count


def evaluate(board):
    """
    Bewertet das Spielfeld aus KI-Sicht.
    Längere Linien erhalten höhere Bewertungen.
    """
    score = 0

    # Dreier-Reihen
    score += _count_lines(board, AI, 3) * 50
    score -= _count_lines(board, HUMAN, 3) * 50

    # Zweier-Reihen
    score += _count_lines(board, AI, 2) * 10
    score -= _count_lines(board, HUMAN, 2) * 10

    # Mittelfelder bevorzugen
    center = BOARD_SIZE // 2
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == AI:
                dist = abs(row - center) + abs(col - center)
                score += max(0, 3 - dist)
            elif board[row][col] == HUMAN:
                dist = abs(row - center) + abs(col - center)
                score -= max(0, 3 - dist)

    return score


def check_winner(board):
    """
    Gibt den Gewinner zurück.
    Rückgabe: 'human' | 'ai' | 'draw' | None
    """
    if _check_four_in_a_row(board, AI):
        return 'ai'
    if _check_four_in_a_row(board, HUMAN):
        return 'human'
    if all(board[r][c] != EMPTY for r in range(BOARD_SIZE) for c in range(BOARD_SIZE)):
        return 'draw'
    return None


RULES_EN = """TIC-TAC-TOE (4 in a Row) - Rules

Played on a 6x6 board.
You play X, the AI plays O.

HOW TO PLAY:
- Take turns placing your piece on any empty square.
- You go first.

WIN CONDITION:
- The first player to get 4 of their pieces in a row
  (horizontal, vertical, or diagonal) wins.

DRAW:
- If the board is full with no winner, the game is a draw."""

RULES_DE = """TIC-TAC-TOE (4 gewinnt) - Regeln

Gespielt auf einem 6x6 Spielfeld.
Du spielst X, die KI spielt O.

SPIELWEISE:
- Spieler setzen abwechselnd einen Stein auf ein freies Feld.
- Du beginnst.

GEWINNBEDINGUNG:
- Wer zuerst 4 Steine in einer Reihe (horizontal, vertikal
  oder diagonal) hat, gewinnt.

UNENTSCHIEDEN:
- Wenn alle Felder belegt sind ohne Gewinner, ist es unentschieden."""
