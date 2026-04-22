"""
test_all.py – Unittests für HHBKTendo Spielesammlung
Testfälle entsprechen Pflichtenheft TC-01 bis TC-15 (soweit ohne GUI testbar).

Ausführen:
    python3 test_all.py
    python3 -m pytest test_all.py -v  (falls pytest installiert)
"""

import json
import math
import os
import tempfile
import time
import unittest
from unittest.mock import patch

import tictactoe as ttt
import pawn_chess as pc
import minimax as mm
import auth
import database


# ─────────────────────────────────────────────
# Hilfsbasis: temporäre SQLite-Datenbank
# ─────────────────────────────────────────────
class DBTestCase(unittest.TestCase):
    """Basisklasse für Tests mit Datenbankzugriff.
    Erstellt vor jedem Test eine frische Temp-DB und löscht sie danach."""

    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp(suffix=".db")
        self._patch = patch.object(database, "DB_PATH", self.db_path)
        self._patch.start()
        database.init_db()
        auth.logout()

    def tearDown(self):
        self._patch.stop()
        auth.logout()
        try:
            os.close(self.db_fd)
            os.unlink(self.db_path)
        except OSError:
            pass


# ═══════════════════════════════════════════════════════════
# 1  TIC-TAC-TOE / 4-gewinnt  (tictactoe.py)
# ═══════════════════════════════════════════════════════════
class TestTicTacToe(unittest.TestCase):

    # ── Spielfeld erstellen ──────────────────────────────
    def test_create_board_is_6x6(self):
        """Brett hat Größe 6×6."""
        board = ttt.create_board()
        self.assertEqual(len(board), 6)
        for row in board:
            self.assertEqual(len(row), 6)

    def test_create_board_is_empty(self):
        """Alle 36 Felder des neuen Bretts sind leer."""
        for row in ttt.create_board():
            for cell in row:
                self.assertEqual(cell, ttt.EMPTY)

    # ── Gültige Züge ────────────────────────────────────
    def test_get_valid_moves_empty_board(self):
        """Auf leerem Brett werden die 4 Mittelfelder als Startoptionen zurückgegeben."""
        moves = ttt.get_valid_moves(ttt.create_board(), True)
        self.assertEqual(len(moves), 4)
        # Mittelfelder bei einem 6×6-Brett: (2,2), (2,3), (3,2), (3,3)
        for pos in [(2, 2), (2, 3), (3, 2), (3, 3)]:
            self.assertIn(pos, moves)

    def test_get_valid_moves_partial_board(self):
        """Nach gesetzten Steinen werden nur direkt angrenzende freie Felder zurückgegeben."""
        board = ttt.create_board()
        board[0][0] = ttt.HUMAN
        board[1][1] = ttt.AI
        board[2][2] = ttt.HUMAN
        moves = ttt.get_valid_moves(board, True)
        # Besetzte Felder dürfen nicht vorkommen
        self.assertNotIn((0, 0), moves)
        self.assertNotIn((1, 1), moves)
        self.assertNotIn((2, 2), moves)
        # Felder mit keinem Nachbarn dürfen nicht vorkommen
        self.assertNotIn((5, 5), moves)
        self.assertNotIn((0, 5), moves)
        # Alle zurückgegebenen Felder müssen leer und im Brett liegen
        for (r, c) in moves:
            self.assertEqual(board[r][c], ttt.EMPTY)
            self.assertGreaterEqual(r, 0); self.assertLess(r, 6)
            self.assertGreaterEqual(c, 0); self.assertLess(c, 6)

    # ── Zug ausführen ───────────────────────────────────
    def test_apply_move_places_human(self):
        """apply_move setzt HUMAN-Stein an die richtige Position."""
        new_board = ttt.apply_move(ttt.create_board(), (3, 3), False)
        self.assertEqual(new_board[3][3], ttt.HUMAN)

    def test_apply_move_places_ai(self):
        """apply_move setzt AI-Stein an die richtige Position."""
        new_board = ttt.apply_move(ttt.create_board(), (0, 0), True)
        self.assertEqual(new_board[0][0], ttt.AI)

    def test_apply_move_does_not_modify_original(self):
        """apply_move verändert das Ausgangsbrett nicht (Immutabilität)."""
        board = ttt.create_board()
        ttt.apply_move(board, (0, 0), True)
        self.assertEqual(board[0][0], ttt.EMPTY)

    # ── Gewinner prüfen ─────────────────────────────────
    def test_check_winner_none_on_empty(self):
        """Kein Gewinner auf leerem Brett."""
        self.assertIsNone(ttt.check_winner(ttt.create_board()))

    def test_check_winner_human_horizontal(self):
        """TC-09: Mensch gewinnt mit 4 in einer Zeile (horizontal)."""
        board = ttt.create_board()
        for col in range(4):
            board[0][col] = ttt.HUMAN
        self.assertEqual(ttt.check_winner(board), "human")

    def test_check_winner_human_vertical(self):
        """Mensch gewinnt mit 4 in einer Spalte (vertikal)."""
        board = ttt.create_board()
        for row in range(4):
            board[row][0] = ttt.HUMAN
        self.assertEqual(ttt.check_winner(board), "human")

    def test_check_winner_human_diagonal_lr(self):
        """TC-10: Mensch gewinnt diagonal (links → rechts)."""
        board = ttt.create_board()
        for k in range(4):
            board[k][k] = ttt.HUMAN
        self.assertEqual(ttt.check_winner(board), "human")

    def test_check_winner_human_diagonal_rl(self):
        """Mensch gewinnt diagonal (rechts → links)."""
        board = ttt.create_board()
        for k in range(4):
            board[k][3 - k] = ttt.HUMAN
        self.assertEqual(ttt.check_winner(board), "human")

    def test_check_winner_ai(self):
        """KI gewinnt mit 4 in einer Zeile."""
        board = ttt.create_board()
        for col in range(4):
            board[0][col] = ttt.AI
        self.assertEqual(ttt.check_winner(board), "ai")

    def test_check_winner_no_winner_partial(self):
        """Kein Gewinner bei weniger als 4 in einer Reihe."""
        board = ttt.create_board()
        for col in range(3):
            board[0][col] = ttt.HUMAN
        self.assertIsNone(ttt.check_winner(board))

    def test_check_winner_draw(self):
        """TC-11: Volles 6×6-Brett ohne 4 in einer Reihe → Unentschieden."""
        # Muster: keine 4 gleichen in einer Richtung, alle 36 Felder belegt
        H, A = ttt.HUMAN, ttt.AI
        board = [
            [H, A, H, A, H, A],
            [H, A, H, A, H, A],
            [A, H, A, H, A, H],
            [A, H, A, H, A, H],
            [H, A, H, A, H, A],
            [H, A, H, A, H, A],
        ]
        self.assertEqual(ttt.check_winner(board), "draw")

    # ── Terminalbedingung ───────────────────────────────
    def test_is_terminal_human_wins(self):
        """is_terminal → (True, SCORE_LOSS) wenn Mensch 4 in einer Reihe hat."""
        board = ttt.create_board()
        for col in range(4):
            board[0][col] = ttt.HUMAN
        terminal, score = ttt.is_terminal(board)
        self.assertTrue(terminal)
        self.assertEqual(score, mm.SCORE_LOSS)

    def test_is_terminal_ai_wins(self):
        """is_terminal → (True, SCORE_WIN) wenn KI 4 in einer Reihe hat."""
        board = ttt.create_board()
        for col in range(4):
            board[0][col] = ttt.AI
        terminal, score = ttt.is_terminal(board)
        self.assertTrue(terminal)
        self.assertEqual(score, mm.SCORE_WIN)

    def test_is_terminal_draw(self):
        """is_terminal → (True, SCORE_DRAW) bei vollem Brett ohne Gewinner."""
        H, A = ttt.HUMAN, ttt.AI
        board = [
            [H, A, H, A, H, A],
            [H, A, H, A, H, A],
            [A, H, A, H, A, H],
            [A, H, A, H, A, H],
            [H, A, H, A, H, A],
            [H, A, H, A, H, A],
        ]
        terminal, score = ttt.is_terminal(board)
        self.assertTrue(terminal)
        self.assertEqual(score, mm.SCORE_DRAW)

    def test_is_terminal_ongoing(self):
        """is_terminal → (False, 0) auf leerem Brett."""
        terminal, score = ttt.is_terminal(ttt.create_board())
        self.assertFalse(terminal)
        self.assertEqual(score, 0)

    # ── Bewertungsfunktion ──────────────────────────────
    def test_evaluate_favors_ai_three_in_row(self):
        """evaluate > 0 wenn KI eine offene Dreier-Reihe hat."""
        board = ttt.create_board()
        for col in range(3):
            board[0][col] = ttt.AI
        self.assertGreater(ttt.evaluate(board), 0)

    def test_evaluate_favors_human_three_in_row(self):
        """evaluate < 0 wenn Mensch eine offene Dreier-Reihe hat."""
        board = ttt.create_board()
        for col in range(3):
            board[0][col] = ttt.HUMAN
        self.assertLess(ttt.evaluate(board), 0)


# ═══════════════════════════════════════════════════════════
# 2  BAUERNSCHACH  (pawn_chess.py)
# ═══════════════════════════════════════════════════════════
class TestPawnChess(unittest.TestCase):

    # ── Spielfeld erstellen ──────────────────────────────
    def test_create_board_is_6x6(self):
        """Brett hat Größe 6×6."""
        board = pc.create_board()
        self.assertEqual(len(board), 6)
        for row in board:
            self.assertEqual(len(row), 6)

    def test_create_board_white_in_row_5(self):
        """Alle weißen Bauern stehen in Zeile 5."""
        board = pc.create_board()
        for col in range(6):
            self.assertEqual(board[5][col], pc.WHITE)

    def test_create_board_black_in_row_0(self):
        """Alle schwarzen Bauern stehen in Zeile 0."""
        board = pc.create_board()
        for col in range(6):
            self.assertEqual(board[0][col], pc.BLACK)

    def test_create_board_middle_rows_empty(self):
        """Zeilen 1–4 sind leer."""
        board = pc.create_board()
        for row in range(1, 5):
            for col in range(6):
                self.assertEqual(board[row][col], pc.EMPTY)

    # ── Gültige Züge ────────────────────────────────────
    def test_valid_moves_white_initial_count(self):
        """Weiß hat zu Spielbeginn genau 6 Vorwärtszüge."""
        moves = pc.get_valid_moves(pc.create_board(), False)
        self.assertEqual(len(moves), 6)

    def test_valid_moves_white_forward_direction(self):
        """TC-05: Weiß zieht vorwärts (Zeile 5 → Zeile 4), kein Seitwärtszug."""
        for from_row, from_col, to_row, to_col in pc.get_valid_moves(pc.create_board(), False):
            self.assertEqual(from_row, 5)
            self.assertEqual(to_row, 4)
            self.assertEqual(from_col, to_col)

    def test_valid_moves_blocked_by_own_piece(self):
        """TC-06: Vorwärtszug auf eigene Figur ist ungültig."""
        board = pc.create_board()
        board[4][0] = pc.WHITE
        self.assertNotIn((5, 0, 4, 0), pc.get_valid_moves(board, False))

    def test_valid_moves_diagonal_capture(self):
        """TC-07: Weißer Bauer schlägt schwarzen Bauern diagonal."""
        board = pc.create_board()
        board[4][1] = pc.BLACK
        self.assertIn((5, 0, 4, 1), pc.get_valid_moves(board, False))

    def test_valid_moves_no_capture_own_piece(self):
        """Diagonal-Schlagen auf eigene Figur ist ungültig."""
        board = pc.create_board()
        board[4][1] = pc.WHITE
        self.assertNotIn((5, 0, 4, 1), pc.get_valid_moves(board, False))

    # ── Zug ausführen ───────────────────────────────────
    def test_apply_move_moves_piece(self):
        """apply_move setzt die Figur auf das Zielfeld."""
        board = pc.create_board()
        new_board = pc.apply_move(board, (5, 0, 4, 0), False)
        self.assertEqual(new_board[4][0], pc.WHITE)
        self.assertEqual(new_board[5][0], pc.EMPTY)

    def test_apply_move_capture_removes_opponent(self):
        """apply_move entfernt die geschlagene gegnerische Figur."""
        board = pc.create_board()
        board[4][1] = pc.BLACK
        new_board = pc.apply_move(board, (5, 0, 4, 1), False)
        self.assertEqual(new_board[4][1], pc.WHITE)

    def test_apply_move_does_not_modify_original(self):
        """apply_move verändert das Ausgangsbrett nicht."""
        board = pc.create_board()
        pc.apply_move(board, (5, 0, 4, 0), False)
        self.assertEqual(board[5][0], pc.WHITE)
        self.assertEqual(board[4][0], pc.EMPTY)

    # ── Gewinner prüfen ─────────────────────────────────
    def test_check_winner_none_initial(self):
        """Kein Gewinner auf Startbrett."""
        self.assertIsNone(pc.check_winner(pc.create_board()))

    def test_check_winner_white_reaches_baseline(self):
        """TC-08: Weißer Bauer auf Zeile 0 → Mensch gewinnt."""
        board = pc.create_board()
        board[0][3] = pc.WHITE
        self.assertEqual(pc.check_winner(board), "white")

    def test_check_winner_black_reaches_baseline(self):
        """Schwarzer Bauer auf Zeile 5 → KI gewinnt."""
        board = pc.create_board()
        board[5][3] = pc.BLACK
        self.assertEqual(pc.check_winner(board), "black")

    def test_check_winner_no_white_pieces(self):
        """Alle weißen Figuren geschlagen → KI gewinnt."""
        board = [[pc.EMPTY] * 6 for _ in range(6)]
        board[0][0] = pc.BLACK
        self.assertEqual(pc.check_winner(board), "black")

    def test_check_winner_no_black_pieces(self):
        """Alle schwarzen Figuren geschlagen → Mensch gewinnt."""
        board = [[pc.EMPTY] * 6 for _ in range(6)]
        board[5][0] = pc.WHITE
        self.assertEqual(pc.check_winner(board), "white")

    # ── Terminalbedingung & Bewertung ───────────────────
    def test_is_terminal_white_wins(self):
        """is_terminal → SCORE_LOSS wenn Mensch gewinnt."""
        board = [[pc.EMPTY] * 6 for _ in range(6)]
        board[0][0] = pc.WHITE
        terminal, score = pc.is_terminal(board)
        self.assertTrue(terminal)
        self.assertEqual(score, mm.SCORE_LOSS)

    def test_is_terminal_black_wins(self):
        """is_terminal → SCORE_WIN wenn KI gewinnt."""
        board = [[pc.EMPTY] * 6 for _ in range(6)]
        board[5][0] = pc.BLACK
        terminal, score = pc.is_terminal(board)
        self.assertTrue(terminal)
        self.assertEqual(score, mm.SCORE_WIN)

    def test_evaluate_positive_for_black_advantage(self):
        """Bewertung > 0 wenn KI mehr Figuren hat."""
        board = [[pc.EMPTY] * 6 for _ in range(6)]
        board[0][0] = pc.BLACK
        board[0][1] = pc.BLACK
        board[5][0] = pc.WHITE
        self.assertGreater(pc.evaluate(board), 0)

    def test_evaluate_negative_for_white_advantage(self):
        """Bewertung < 0 wenn Mensch mehr Figuren hat."""
        board = [[pc.EMPTY] * 6 for _ in range(6)]
        board[5][0] = pc.WHITE
        board[5][1] = pc.WHITE
        board[0][0] = pc.BLACK
        self.assertLess(pc.evaluate(board), 0)

    def test_evaluate_symmetric_is_zero(self):
        """Bewertung = 0 bei symmetrischem Brett (eine Figur je Seite, gleicher Fortschritt)."""
        board = [[pc.EMPTY] * 6 for _ in range(6)]
        board[0][0] = pc.BLACK   # Fortschritt 0
        board[5][0] = pc.WHITE   # Fortschritt 0
        self.assertEqual(pc.evaluate(board), 0)


# ═══════════════════════════════════════════════════════════
# 3  MINIMAX  (minimax.py)
# ═══════════════════════════════════════════════════════════
class TestMiniMax(unittest.TestCase):

    def _best(self, board, depth):
        return mm.get_best_move(
            board, depth,
            ttt.get_valid_moves, ttt.apply_move,
            ttt.evaluate, ttt.is_terminal,
        )

    def _score(self, board, depth, is_max):
        return mm.minimax(
            board, depth, is_max, -math.inf, math.inf,
            ttt.get_valid_moves, ttt.apply_move,
            ttt.evaluate, ttt.is_terminal,
        )

    def test_ai_takes_winning_move(self):
        """KI spielt sofortigen Gewinnzug (4 in einer Reihe, Tiefe 1)."""
        board = ttt.create_board()
        for col in range(3):
            board[0][col] = ttt.AI      # O O O _  → KI spielt (0,3)
            board[1][col] = ttt.HUMAN
        self.assertEqual(self._best(board, 1), (0, 3))

    def test_ai_blocks_human_win(self):
        """KI blockiert den Gewinnzug des Menschen (Tiefe 3)."""
        board = ttt.create_board()
        for col in range(3):
            board[0][col] = ttt.HUMAN   # X X X _  → Mensch könnte (0,3) gewinnen
        board[1][0] = ttt.AI
        self.assertEqual(self._best(board, 3), (0, 3))

    def test_get_best_move_no_moves_returns_none(self):
        """get_best_move gibt None zurück wenn keine Züge verfügbar."""
        H, A = ttt.HUMAN, ttt.AI
        full_board = [
            [H, A, H, A, H, A],
            [H, A, H, A, H, A],
            [A, H, A, H, A, H],
            [A, H, A, H, A, H],
            [H, A, H, A, H, A],
            [H, A, H, A, H, A],
        ]
        self.assertIsNone(self._best(full_board, 3))

    def test_minimax_returns_score_win_for_ai_victory(self):
        """minimax gibt SCORE_WIN zurück bei abgeschlossener KI-Gewinnstellung."""
        board = ttt.create_board()
        for col in range(4):
            board[0][col] = ttt.AI
        score = self._score(board, 3, False)
        self.assertEqual(score, mm.SCORE_WIN)

    def test_minimax_depth_zero_returns_evaluate(self):
        """Bei Tiefe 0 wird evaluate(board) direkt zurückgegeben."""
        board = ttt.create_board()
        self.assertEqual(self._score(board, 0, True), ttt.evaluate(board))

    def test_get_best_move_within_time_limit(self):
        """TC-12: KI-Zug bei Tiefe 5 endet innerhalb von 45 Sekunden (Mitte des Spiels)."""
        # Realistisches Spielszenario: 12 Steine gesetzt → 24 freie Felder
        # Abwechselndes Muster stellt sicher, dass noch kein Gewinner vorliegt.
        board = ttt.create_board()
        pieces = [
            (0, 0, ttt.HUMAN), (0, 1, ttt.AI),   (0, 2, ttt.HUMAN), (0, 3, ttt.AI),
            (1, 0, ttt.AI),   (1, 1, ttt.HUMAN), (1, 2, ttt.AI),   (1, 3, ttt.HUMAN),
            (2, 0, ttt.HUMAN), (2, 1, ttt.AI),   (2, 2, ttt.HUMAN), (2, 3, ttt.AI),
        ]
        for row, col, player in pieces:
            board[row][col] = player
        start = time.time()
        self._best(board, 5)
        self.assertLess(time.time() - start, 45)


# ═══════════════════════════════════════════════════════════
# 4  AUTH – Passwort-Hashing  (ohne Datenbank)
# ═══════════════════════════════════════════════════════════
class TestAuth(unittest.TestCase):

    def setUp(self):
        auth.logout()

    def tearDown(self):
        auth.logout()

    def test_hash_password_format(self):
        """hash_password gibt 'salt:hash' (genau 1 Doppelpunkt) zurück."""
        self.assertEqual(len(auth.hash_password("geheim").split(":")), 2)

    def test_hash_password_unique_salts(self):
        """Zwei Aufrufe mit gleichem Passwort erzeugen unterschiedliche Hashes."""
        self.assertNotEqual(auth.hash_password("test"), auth.hash_password("test"))

    def test_verify_password_correct(self):
        """verify_password gibt True für das korrekte Passwort zurück."""
        self.assertTrue(auth.verify_password("korrekt", auth.hash_password("korrekt")))

    def test_verify_password_wrong(self):
        """verify_password gibt False für falsches Passwort zurück."""
        self.assertFalse(auth.verify_password("falsch", auth.hash_password("korrekt")))

    def test_verify_password_invalid_format(self):
        """verify_password gibt False für ungültiges Hash-Format zurück."""
        self.assertFalse(auth.verify_password("pw", "kein_doppelpunkt"))

    def test_session_guest_after_logout(self):
        """Nach logout() ist kein Benutzer angemeldet (Gastmodus)."""
        auth.set_current_user({"id": 1, "username": "x"})
        auth.logout()
        self.assertIsNone(auth.get_current_user())
        self.assertTrue(auth.is_guest())
        self.assertFalse(auth.is_logged_in())

    def test_session_set_and_get(self):
        """set_current_user / get_current_user / is_logged_in korrekt."""
        user = {"id": 42, "username": "tester"}
        auth.set_current_user(user)
        self.assertEqual(auth.get_current_user(), user)
        self.assertTrue(auth.is_logged_in())
        self.assertFalse(auth.is_guest())


# ═══════════════════════════════════════════════════════════
# 5  DATENBANK  (database.py)
# ═══════════════════════════════════════════════════════════
class TestDatabase(DBTestCase):

    def test_init_creates_tables(self):
        """init_db legt users- und results-Tabellen an."""
        conn = database.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = {row[0] for row in cursor.fetchall()}
        conn.close()
        self.assertIn("users", tables)
        self.assertIn("results", tables)

    def test_register_user_returns_id(self):
        """register_user gibt eine Integer-ID zurück."""
        uid = database.register_user("alice", "h:abc")
        self.assertIsNotNone(uid)
        self.assertIsInstance(uid, int)

    def test_register_user_duplicate_returns_none(self):
        """register_user gibt None bei doppeltem Benutzernamen zurück."""
        database.register_user("bob", "h:abc")
        self.assertIsNone(database.register_user("bob", "h:xyz"))

    def test_get_user_by_username_found(self):
        """get_user_by_username findet den registrierten Benutzer."""
        database.register_user("carol", "h:abc")
        user = database.get_user_by_username("carol")
        self.assertIsNotNone(user)
        self.assertEqual(user["username"], "carol")

    def test_get_user_by_username_not_found(self):
        """get_user_by_username gibt None zurück für unbekannten Namen."""
        self.assertIsNone(database.get_user_by_username("niemand"))

    def test_save_result_appears_in_leaderboard(self):
        """Gespeichertes Ergebnis erscheint in der Bestenliste."""
        uid = database.register_user("dave", "h:abc")
        database.save_result(uid, "tictactoe", 3, True)
        lb = database.get_leaderboard("tictactoe", 3)
        self.assertEqual(len(lb), 1)
        self.assertEqual(lb[0]["username"], "dave")
        self.assertEqual(lb[0]["wins"], 1)
        self.assertEqual(lb[0]["losses"], 0)

    def test_leaderboard_sorting_by_wins(self):
        """TC-14: Bestenliste ist nach Siegen absteigend sortiert."""
        uid1 = database.register_user("erster", "h:a")
        uid2 = database.register_user("zweiter", "h:b")
        database.save_result(uid1, "tictactoe", 1, True)
        database.save_result(uid2, "tictactoe", 1, True)
        database.save_result(uid2, "tictactoe", 1, True)
        lb = database.get_leaderboard("tictactoe", 1)
        self.assertEqual(lb[0]["username"], "zweiter")
        self.assertEqual(lb[1]["username"], "erster")

    def test_leaderboard_empty(self):
        """Leere Bestenliste gibt leere Liste zurück."""
        self.assertEqual(database.get_leaderboard("tictactoe", 3), [])

    def test_leaderboard_separate_per_difficulty(self):
        """Bestenlisten sind pro Schwierigkeitsgrad getrennt."""
        uid = database.register_user("emma", "h:a")
        database.save_result(uid, "tictactoe", 1, True)
        self.assertEqual(len(database.get_leaderboard("tictactoe", 1)), 1)
        self.assertEqual(len(database.get_leaderboard("tictactoe", 2)), 0)

    def test_update_user_language(self):
        """update_user_language speichert die Spracheinstellung."""
        uid = database.register_user("finn", "h:a")
        database.update_user_language(uid, "de")
        self.assertEqual(database.get_user_by_username("finn")["language"], "de")

    def test_guest_no_result_saved(self):
        """TC-04: Im Gastmodus werden keine Ergebnisse gespeichert."""
        auth.logout()
        user = auth.get_current_user()
        # Simuliert die Bedingung aus main.py: nur speichern wenn user nicht None
        if user:
            database.save_result(user["id"], "tictactoe", 3, True)
        self.assertEqual(database.get_leaderboard("tictactoe", 3), [])


# ═══════════════════════════════════════════════════════════
# 6  AUTH + DATENBANK  (auth.py mit DB-Anbindung)
# ═══════════════════════════════════════════════════════════
class TestAuthWithDB(DBTestCase):

    def test_register_valid_user(self):
        """TC-01: Registrierung mit gültigem Namen/Passwort erfolgreich."""
        ok, result = auth.register("anna", "pass1234")
        self.assertTrue(ok)
        self.assertIsNotNone(result)

    def test_register_duplicate_username(self):
        """TC-02: Registrierung mit bereits vergebenem Namen schlägt fehl."""
        auth.register("anna", "pass1234")
        ok, msg = auth.register("anna", "anderes")
        self.assertFalse(ok)
        self.assertIn("taken", msg.lower())

    def test_register_username_too_short(self):
        """Registrierung mit Benutzernamen unter 3 Zeichen schlägt fehl."""
        ok, msg = auth.register("ab", "pass1234")
        self.assertFalse(ok)
        self.assertIn("3", msg)

    def test_register_password_too_short(self):
        """Registrierung mit Passwort unter 4 Zeichen schlägt fehl."""
        ok, msg = auth.register("gueltig", "abc")
        self.assertFalse(ok)
        self.assertIn("4", msg)

    def test_login_success(self):
        """Anmelden mit korrekten Daten gibt Benutzerdaten zurück."""
        auth.register("ben", "sicher99")
        ok, user = auth.login("ben", "sicher99")
        self.assertTrue(ok)
        self.assertEqual(user["username"], "ben")

    def test_login_wrong_password(self):
        """TC-03: Anmelden mit falschem Passwort schlägt fehl."""
        auth.register("clara", "richtig")
        ok, msg = auth.login("clara", "falsch")
        self.assertFalse(ok)
        self.assertIn("incorrect", msg.lower())

    def test_login_unknown_user(self):
        """Anmelden mit unbekanntem Benutzernamen schlägt fehl."""
        ok, msg = auth.login("geist", "egal")
        self.assertFalse(ok)
        self.assertIn("not found", msg.lower())

    def test_login_empty_credentials(self):
        """Anmelden mit leeren Feldern schlägt fehl."""
        ok, _ = auth.login("", "")
        self.assertFalse(ok)

    def test_register_then_login_sets_session(self):
        """Nach erfolgreicher Anmeldung ist der Benutzer in der Session."""
        auth.register("diana", "pw1234")
        ok, user = auth.login("diana", "pw1234")
        self.assertTrue(ok)
        auth.set_current_user(user)
        self.assertTrue(auth.is_logged_in())
        self.assertEqual(auth.get_current_user()["username"], "diana")


# ═══════════════════════════════════════════════════════════
# 7  SESSION / AUTO-LOGIN  (auth.py – save/load/clear_session)
# ═══════════════════════════════════════════════════════════
class TestSession(DBTestCase):
    """Tests für Session-Persistenz (keep_logged_in, PF-M08)."""

    def setUp(self):
        super().setUp()
        # Eigene Temp-Datei für session.json → kein Seiteneffekt auf Disk
        self._sess_fd, self._sess_path = tempfile.mkstemp(suffix=".json")
        os.close(self._sess_fd)
        os.unlink(self._sess_path)   # Nur Pfad reservieren, Datei noch nicht anlegen
        self._sess_patch = patch.object(auth, "SESSION_FILE", self._sess_path)
        self._sess_patch.start()

    def tearDown(self):
        self._sess_patch.stop()
        try:
            if os.path.exists(self._sess_path):
                os.unlink(self._sess_path)
        except OSError:
            pass
        super().tearDown()

    def test_save_session_creates_file(self):
        """save_session legt eine Session-Datei an."""
        uid = database.register_user("hans", "h:abc")
        auth.save_session(uid)
        self.assertTrue(os.path.exists(self._sess_path))

    def test_save_and_load_session_returns_correct_user(self):
        """Gespeicherte Session laden gibt den richtigen Benutzer zurück."""
        uid = database.register_user("anna", "h:abc")
        auth.save_session(uid)
        loaded = auth.load_session()
        self.assertIsNotNone(loaded)
        self.assertEqual(loaded["id"], uid)
        self.assertEqual(loaded["username"], "anna")

    def test_load_session_no_file_returns_none(self):
        """load_session gibt None zurück wenn keine Session-Datei vorhanden ist."""
        self.assertIsNone(auth.load_session())

    def test_load_session_unknown_user_id_returns_none(self):
        """load_session gibt None zurück wenn die gespeicherte User-ID nicht existiert."""
        with open(self._sess_path, "w") as f:
            json.dump({"user_id": 9999}, f)
        self.assertIsNone(auth.load_session())

    def test_load_session_corrupt_json_returns_none(self):
        """load_session gibt None zurück bei beschädigter Session-Datei."""
        with open(self._sess_path, "w") as f:
            f.write("{kein gültiges json{{")
        self.assertIsNone(auth.load_session())

    def test_load_session_empty_file_returns_none(self):
        """load_session gibt None zurück bei leerer Session-Datei."""
        open(self._sess_path, "w").close()
        self.assertIsNone(auth.load_session())

    def test_clear_session_removes_file(self):
        """clear_session löscht die Session-Datei."""
        uid = database.register_user("berta", "h:abc")
        auth.save_session(uid)
        self.assertTrue(os.path.exists(self._sess_path))
        auth.clear_session()
        self.assertFalse(os.path.exists(self._sess_path))

    def test_clear_session_without_file_does_not_raise(self):
        """clear_session wirft keine Exception wenn keine Session-Datei vorhanden ist."""
        self.assertFalse(os.path.exists(self._sess_path))
        auth.clear_session()  # Darf keinen Fehler werfen

    def test_logout_clears_session_file_and_current_user(self):
        """logout() löscht die Session-Datei und setzt current_user auf None."""
        uid = database.register_user("carla", "h:abc")
        user = database.get_user_by_id(uid)
        auth.set_current_user(user)
        auth.save_session(uid)
        self.assertTrue(os.path.exists(self._sess_path))

        auth.logout()

        self.assertFalse(os.path.exists(self._sess_path))
        self.assertIsNone(auth.get_current_user())

    def test_load_session_after_logout_returns_none(self):
        """Nach logout() liefert load_session() None (Session wurde gelöscht)."""
        uid = database.register_user("dieter", "h:abc")
        auth.set_current_user(database.get_user_by_id(uid))
        auth.save_session(uid)
        auth.logout()
        self.assertIsNone(auth.load_session())

    def test_session_survives_simulated_app_restart(self):
        """Benutzer bleibt nach simuliertem Neustart eingeloggt (Auto-Login)."""
        auth.register("eva", "pass1234")
        ok, user = auth.login("eva", "pass1234")
        self.assertTrue(ok)
        auth.save_session(user["id"])
        # App-Neustart simulieren: current_user zurücksetzen
        auth.set_current_user(None)
        self.assertIsNone(auth.get_current_user())
        # Auto-Login: Session laden
        restored = auth.load_session()
        self.assertIsNotNone(restored)
        auth.set_current_user(restored)
        self.assertTrue(auth.is_logged_in())
        self.assertEqual(auth.get_current_user()["username"], "eva")

    def test_session_contains_user_language(self):
        """Geladene Session enthält die Spracheinstellung des Benutzers."""
        uid = database.register_user("finn", "h:abc", "de")
        auth.save_session(uid)
        loaded = auth.load_session()
        self.assertIsNotNone(loaded)
        self.assertEqual(loaded["language"], "de")


# ═══════════════════════════════════════════════════════════
# 8  SPRACHEINSTELLUNG IN DER DATENBANK  (PF-K01, PF-K02, LD4230)
# ═══════════════════════════════════════════════════════════
class TestLanguage(DBTestCase):

    def test_register_default_language_is_en(self):
        """Neu registrierter Benutzer hat Standardsprache 'en'."""
        database.register_user("greta", "h:abc")
        user = database.get_user_by_username("greta")
        self.assertEqual(user["language"], "en")

    def test_register_with_language_de(self):
        """Benutzer kann mit Sprache 'de' angelegt werden."""
        database.register_user("hugo", "h:abc", language="de")
        user = database.get_user_by_username("hugo")
        self.assertEqual(user["language"], "de")

    def test_update_language_to_de(self):
        """update_user_language speichert 'de' korrekt in der Datenbank."""
        uid = database.register_user("ida", "h:abc")
        database.update_user_language(uid, "de")
        self.assertEqual(database.get_user_by_username("ida")["language"], "de")

    def test_update_language_back_to_en(self):
        """Spracheinstellung kann von 'de' zurück auf 'en' geändert werden."""
        uid = database.register_user("jan", "h:abc", language="de")
        database.update_user_language(uid, "en")
        self.assertEqual(database.get_user_by_username("jan")["language"], "en")

    def test_update_language_does_not_affect_other_users(self):
        """Sprachänderung eines Benutzers beeinflusst andere Benutzer nicht."""
        uid1 = database.register_user("karl", "h:a", language="en")
        uid2 = database.register_user("lisa", "h:b", language="en")
        database.update_user_language(uid1, "de")
        self.assertEqual(database.get_user_by_username("lisa")["language"], "en")

    def test_login_user_dict_contains_language_field(self):
        """Nach dem Login enthält das zurückgegebene User-Dict das 'language'-Feld."""
        auth.register("max", "pass1234")
        ok, user = auth.login("max", "pass1234")
        self.assertTrue(ok)
        self.assertIn("language", user)

    def test_login_returns_correct_default_language(self):
        """Neu registrierter Benutzer hat nach Login Sprache 'en'."""
        auth.register("nina", "pass1234")
        _, user = auth.login("nina", "pass1234")
        self.assertEqual(user["language"], "en")

    def test_language_change_visible_after_relogin(self):
        """Geänderte Sprache bleibt nach erneutem Login erhalten."""
        auth.register("otto", "pass1234")
        _, user = auth.login("otto", "pass1234")
        database.update_user_language(user["id"], "de")
        # Erneuter Login simuliert App-Neustart
        ok, user2 = auth.login("otto", "pass1234")
        self.assertTrue(ok)
        self.assertEqual(user2["language"], "de")

    def test_auth_register_passes_language_to_db(self):
        """auth.register speichert die Sprache in der Datenbank."""
        auth.register("paula", "pass1234", language="de")
        _, user = auth.login("paula", "pass1234")
        self.assertEqual(user["language"], "de")

    def test_get_user_by_id_contains_language(self):
        """get_user_by_id gibt ebenfalls das 'language'-Feld zurück."""
        uid = database.register_user("rudi", "h:abc", language="de")
        user = database.get_user_by_id(uid)
        self.assertIsNotNone(user)
        self.assertEqual(user["language"], "de")


# ─────────────────────────────────────────────
if __name__ == "__main__":
    unittest.main(verbosity=2)
