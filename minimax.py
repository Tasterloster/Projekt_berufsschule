"""
minimax.py - Generischer MiniMax-Algorithmus mit Alpha-Beta-Pruning
Wiederverwendbar für alle Spiele (LF4030, LF4120, LN5040)

Der Algorithmus arbeitet rekursiv und verwendet Callback-Funktionen,
um spielspezifische Logik einzubinden.
"""

import math

# Konstanten für Bewertungen
SCORE_WIN = 1000000
SCORE_LOSS = -1000000
SCORE_DRAW = 0


def minimax(board, depth, is_maximizing, alpha, beta,
            get_moves_fn, apply_move_fn, evaluate_fn, is_terminal_fn):
    """
    Generischer MiniMax-Algorithmus mit Alpha-Beta-Pruning (LF4120).

    Parameter:
        board         - Aktuelle Spielfelddarstellung (unveränderlich, wird kopiert)
        depth         - Verbleibende Suchtiefe (Spielstärke)
        is_maximizing - True wenn KI (Maximizer), False wenn Mensch (Minimizer)
        alpha         - Alpha-Wert für Pruning (initialisiert mit -inf)
        beta          - Beta-Wert für Pruning (initialisiert mit +inf)
        get_moves_fn  - fn(board, is_maximizing) -> Liste möglicher Züge
        apply_move_fn - fn(board, move, is_maximizing) -> neues Board (Kopie)
        evaluate_fn   - fn(board) -> numerischer Wert (positiv = gut für KI)
        is_terminal_fn- fn(board) -> (terminal: bool, score: int oder None)

    Rückgabe:
        Numerischer Bewertungswert des besten Zugs
    """
    # Terminalbedingung prüfen
    terminal, score = is_terminal_fn(board)
    if terminal:
        return score

    if depth == 0:
        return evaluate_fn(board)

    moves = get_moves_fn(board, is_maximizing)

    # Keine Züge mehr möglich -> Niederlage für den aktuellen Spieler
    if not moves:
        if is_maximizing:
            return SCORE_LOSS
        else:
            return SCORE_WIN

    if is_maximizing:
        best_score = -math.inf
        for move in moves:
            new_board = apply_move_fn(board, move, is_maximizing)
            score = minimax(new_board, depth - 1, False, alpha, beta,
                            get_moves_fn, apply_move_fn, evaluate_fn, is_terminal_fn)
            best_score = max(best_score, score)
            alpha = max(alpha, score)
            if beta <= alpha:
                break  # Beta-Pruning
        return best_score
    else:
        best_score = math.inf
        for move in moves:
            new_board = apply_move_fn(board, move, is_maximizing)
            score = minimax(new_board, depth - 1, True, alpha, beta,
                            get_moves_fn, apply_move_fn, evaluate_fn, is_terminal_fn)
            best_score = min(best_score, score)
            beta = min(beta, score)
            if beta <= alpha:
                break  # Alpha-Pruning
        return best_score


def get_best_move(board, depth, get_moves_fn, apply_move_fn,
                  evaluate_fn, is_terminal_fn):
    """
    Findet den besten Zug für die KI (Maximizer) mit MiniMax.

    Rückgabe:
        Bester Zug oder None wenn keine Züge möglich
    """
    best_score = -math.inf
    best_move = None
    alpha = -math.inf
    beta = math.inf

    moves = get_moves_fn(board, True)
    if not moves:
        return None

    for move in moves:
        new_board = apply_move_fn(board, move, True)
        score = minimax(new_board, depth - 1, False, alpha, beta,
                        get_moves_fn, apply_move_fn, evaluate_fn, is_terminal_fn)
        if score > best_score:
            best_score = score
            best_move = move
        alpha = max(alpha, score)

    return best_move
