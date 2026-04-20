"""
pawn_chess.py - Bauernschach Spiellogik auf 6x6 Spielfeld
Spieler: WHITE = 1 (Mensch, unten), BLACK = -1 (KI, oben)
Leer  = 0
"""

import copy
from minimax import SCORE_WIN, SCORE_LOSS

BOARD_SIZE = 6
EMPTY = 0
WHITE = 1   # Mensch - zieht von Reihe 5 nach oben (Reihe 0)
BLACK = -1  # KI    - zieht von Reihe 0 nach unten (Reihe 5)

# Grundlinien
WHITE_BASELINE = 0  # Weiß muss hierhin (gegnerische Grundlinie)
BLACK_BASELINE = 5  # Schwarz muss hierhin


def create_board():
    """
    Erstellt das initiale 6x6 Bauernschach-Spielfeld.
    Weiße Bauern stehen in Reihe 5 (unten), schwarze in Reihe 0 (oben).
    """
    board = [[EMPTY] * BOARD_SIZE for _ in range(BOARD_SIZE)]
    for col in range(BOARD_SIZE):
        board[0][col] = BLACK
        board[5][col] = WHITE
    return board


def get_valid_moves(board, is_maximizing):
    """
    Gibt alle gültigen Züge für den aktuellen Spieler zurück.
    is_maximizing=True -> KI (BLACK), False -> Mensch (WHITE)
    Zug-Format: (from_row, from_col, to_row, to_col)
    """
    player = BLACK if is_maximizing else WHITE
    direction = 1 if player == BLACK else -1  # BLACK zieht nach unten (+1), WHITE nach oben (-1)
    moves = []

    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] != player:
                continue
            new_row = row + direction

            # Vorwärtszug (nur wenn Feld frei)
            if 0 <= new_row < BOARD_SIZE:
                if board[new_row][col] == EMPTY:
                    moves.append((row, col, new_row, col))

                # Diagonales Schlagen (links und rechts)
                for dc in [-1, 1]:
                    new_col = col + dc
                    if 0 <= new_col < BOARD_SIZE:
                        target = board[new_row][new_col]
                        if target != EMPTY and target != player:
                            moves.append((row, col, new_row, new_col))

    return moves


def apply_move(board, move, is_maximizing):
    """
    Wendet einen Zug auf das Spielfeld an und gibt eine Kopie zurück.
    Zug-Format: (from_row, from_col, to_row, to_col)
    """
    new_board = copy.deepcopy(board)
    from_row, from_col, to_row, to_col = move
    new_board[to_row][to_col] = new_board[from_row][from_col]
    new_board[from_row][from_col] = EMPTY
    return new_board


def is_terminal(board):
    """
    Prüft ob das Spiel beendet ist.
    Rückgabe: (terminal: bool, score: int)
    score: SCORE_WIN = KI gewinnt, SCORE_LOSS = KI verliert
    """
    # Prüfe ob Weiß die schwarze Grundlinie erreicht hat
    for col in range(BOARD_SIZE):
        if board[WHITE_BASELINE][col] == WHITE:
            return True, SCORE_LOSS  # Mensch gewinnt -> schlecht für KI

    # Prüfe ob Schwarz die weiße Grundlinie erreicht hat
    for col in range(BOARD_SIZE):
        if board[BLACK_BASELINE][col] == BLACK:
            return True, SCORE_WIN  # KI gewinnt

    # Prüfe ob Weiß noch Figuren hat
    white_pieces = sum(1 for r in board for c in r if c == WHITE)
    black_pieces = sum(1 for r in board for c in r if c == BLACK)

    if white_pieces == 0:
        return True, SCORE_WIN  # Kein Weiß mehr -> KI gewinnt
    if black_pieces == 0:
        return True, SCORE_LOSS  # Kein Schwarz mehr -> Mensch gewinnt

    # Prüfe ob Weiß noch Züge hat
    if not get_valid_moves(board, False):
        return True, SCORE_WIN  # Weiß kann nicht ziehen -> KI gewinnt
    # Prüfe ob Schwarz noch Züge hat
    if not get_valid_moves(board, True):
        return True, SCORE_LOSS  # Schwarz kann nicht ziehen -> Mensch gewinnt

    return False, 0


def evaluate(board):
    """
    Bewertet das Spielfeld aus KI-Sicht (BLACK = positiv).
    Bewertungskriterien:
    - Anzahl Figuren pro Spieler
    - Fortschritt der Figuren (wie weit sind sie vorgerückt)
    - Zentrale Positionen bevorzugt
    """
    score = 0

    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            piece = board[row][col]
            if piece == EMPTY:
                continue

            # Grundwert pro Figur
            piece_value = 10

            # Fortschritt: Wie weit ist die Figur vorgerückt?
            if piece == BLACK:
                progress = row  # Schwarz will hohe Zeilennummer
                center_bonus = 1 if 1 <= col <= 4 else 0
                score += piece_value + progress * 2 + center_bonus
            else:  # WHITE
                progress = BOARD_SIZE - 1 - row  # Weiß will niedrige Zeilennummer
                center_bonus = 1 if 1 <= col <= 4 else 0
                score -= piece_value + progress * 2 + center_bonus

    return score


def check_winner(board):
    """
    Prüft ob das Spiel gewonnen ist.
    Rückgabe: 'white' | 'black' | 'draw' | None
    """
    # Weiß erreicht obere Grundlinie
    for col in range(BOARD_SIZE):
        if board[WHITE_BASELINE][col] == WHITE:
            return 'white'

    # Schwarz erreicht untere Grundlinie
    for col in range(BOARD_SIZE):
        if board[BLACK_BASELINE][col] == BLACK:
            return 'black'

    white_count = sum(1 for r in board for c in r if c == WHITE)
    black_count = sum(1 for r in board for c in r if c == BLACK)

    if white_count == 0:
        return 'black'
    if black_count == 0:
        return 'white'

    if not get_valid_moves(board, False):
        return 'black'
    if not get_valid_moves(board, True):
        return 'white'

    return None


RULES_EN = """PAWN CHESS - Rules

Played on a 6x6 board with pawns only.
White (you) starts at the bottom, Black (AI) at the top.

MOVES:
- Move forward one square if it's empty.
- Capture diagonally forward onto an opponent's square.

WIN CONDITIONS:
- Reach the opponent's baseline (row 1 for you).
- Opponent has no pieces or no valid moves.

No draws possible in this variant."""

RULES_DE = """BAUERNSCHACH - Regeln

Gespielt auf einem 6x6 Spielfeld nur mit Bauern.
Weiß (du) startet unten, Schwarz (KI) oben.

ZÜGE:
- Vorwärts ein Feld ziehen, wenn es frei ist.
- Diagonal vorwärts schlagen auf ein Feld mit gegnerischem Bauern.

GEWINNBEDINGUNGEN:
- Einen Bauern auf die gegnerische Grundlinie (Reihe 1) bringen.
- Der Gegner hat keine Figuren oder keine Züge mehr.

Unentschieden ist in dieser Variante nicht möglich."""
