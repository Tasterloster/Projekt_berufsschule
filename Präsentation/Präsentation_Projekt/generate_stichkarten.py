from reportlab.lib.pagesizes import A5
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER

OUTPUT = "HHBKTendo_Stichkarten.pdf"

BG = colors.HexColor("#0D0D1A")
PINK = colors.HexColor("#E94560")
PURPLE = colors.HexColor("#6C3FC5")
CYAN = colors.HexColor("#00D4FF")
WHITE = colors.HexColor("#FFFFFF")
LIGHT = colors.HexColor("#C0C0D0")
CARD_BG = colors.HexColor("#161638")

W, H = A5

doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=A5,
    leftMargin=12*mm,
    rightMargin=12*mm,
    topMargin=10*mm,
    bottomMargin=10*mm,
)

title_style = ParagraphStyle(
    "CardTitle",
    fontName="Helvetica-Bold",
    fontSize=13,
    textColor=PINK,
    spaceAfter=4,
    leading=16,
)
subtitle_style = ParagraphStyle(
    "CardSubtitle",
    fontName="Helvetica-Oblique",
    fontSize=9,
    textColor=CYAN,
    spaceAfter=6,
    leading=12,
)
bullet_style = ParagraphStyle(
    "Bullet",
    fontName="Helvetica",
    fontSize=10,
    textColor=WHITE,
    leftIndent=10,
    spaceAfter=4,
    leading=14,
    bulletIndent=0,
)
sub_bullet_style = ParagraphStyle(
    "SubBullet",
    fontName="Helvetica",
    fontSize=9,
    textColor=LIGHT,
    leftIndent=20,
    spaceAfter=3,
    leading=12,
)
slide_num_style = ParagraphStyle(
    "SlideNum",
    fontName="Helvetica",
    fontSize=8,
    textColor=PURPLE,
    alignment=TA_CENTER,
    spaceBefore=6,
)
section_style = ParagraphStyle(
    "Section",
    fontName="Helvetica-Bold",
    fontSize=10,
    textColor=CYAN,
    spaceAfter=3,
    spaceBefore=6,
    leading=13,
)

def B(text):
    return Paragraph(f"▸  {text}", bullet_style)

def SB(text):
    return Paragraph(f"· {text}", sub_bullet_style)

def S(text):
    return Paragraph(text, section_style)

def HR():
    return HRFlowable(width="100%", thickness=0.5, color=PURPLE, spaceAfter=6, spaceBefore=2)

def card_header(slide_num, title, subtitle=""):
    items = []
    items.append(Paragraph(f"Folie {slide_num}", slide_num_style))
    items.append(Spacer(1, 2*mm))
    items.append(Paragraph(title, title_style))
    if subtitle:
        items.append(Paragraph(subtitle, subtitle_style))
    items.append(HR())
    return items

cards = []

# --- Folie 1: Titelfolie ---
cards += card_header(1, "HHBKTendo – Spielesammlung", "HHBK Düsseldorf · Lernfeld 5 · 2026")
cards += [
    B("Strategiespiele mit MiniMax-KI"),
    B("Bauernschach & Tic-Tac-Toe (4 gewinnt)"),
    B("Tech-Stack: Python 3.10+ · SQLite · tkinter"),
]

# --- Folie 2: Projektüberblick ---
cards.append(Spacer(1, 6*mm))
cards += card_header(2, "Projektüberblick")
cards += [
    S("🎮 Spielesammlung"),
    B("2 Spiele auf je 6×6-Feld"),
    S("🤖 KI-Gegner"),
    B("MiniMax + Alpha-Beta-Pruning"),
    B("Kein Code-Duplikat für beide Spiele"),
    S("👤 Benutzerverwaltung"),
    B("Login / Registrierung · SHA-256-Hashing · Gast-Modus"),
    S("📊 Bestenliste"),
    B("SQLite · Rangliste nach Schwierigkeitsgrad"),
]

# --- Folie 3: Projektstruktur ---
cards.append(Spacer(1, 6*mm))
cards += card_header(3, "Projektstruktur")
cards += [
    B("main.py  → GUI, Screens, app_state"),
    B("minimax.py  → generischer MiniMax + Alpha-Beta"),
    B("pawn_chess.py  → Bauernschach Züge & Bewertung"),
    B("tictactoe.py  → Tic-Tac-Toe Züge & Bewertung"),
    B("auth.py  → Login & Registrierung (SHA-256 + Salt)"),
    B("database.py  → SQLite CRUD (User & Ergebnisse)"),
    B("test_all.py  → 15 Unittests (TC-01 bis TC-15)"),
    B("games.db  → wird automatisch erstellt"),
]

# --- Folie 4: Benutzerverwaltung & DB ---
cards.append(Spacer(1, 6*mm))
cards += card_header(4, "Benutzerverwaltung & Datenbank", "auth.py · database.py")
cards += [
    S("auth.py – Kernfunktionen"),
    B("register() → Validierung + SHA-256 + Salt"),
    B("login() → Passwort-Hash-Vergleich"),
    B("save/load_session() → session.json für Auto-Login"),
    B("logout() → Session löschen"),
    B("is_guest() → Gast = keine Statistiken"),
    S("SQLite-Tabellen"),
    B("users: id, username, password_hash, language, created_at"),
    B("results: id, user_id (FK), game, difficulty, won, played_at"),
]

# --- Folie 5: row_factory & SQL-Injection ---
cards.append(Spacer(1, 6*mm))
cards += card_header(5, "DB-Techniken", "row_factory · Schema-Migration · SQL-Injection-Schutz")
cards += [
    B("sqlite3.Row  →  Spaltenzugriff per Name: row['username']"),
    B("dict(row)  →  einfache Konvertierung für die App"),
    B("?-Platzhalter  →  schützt vor SQL-Injection"),
    B("try/except bei ALTER TABLE  →  DB bleibt kompatibel"),
]

# --- Folie 6: Passwort-Sicherheit ---
cards.append(Spacer(1, 6*mm))
cards += card_header(6, "Sichere Passwortspeicherung", "SHA-256 + Salt")
cards += [
    B("Kein Klartext – nur 'salt:hash' in der DB"),
    B("os.urandom(16)  →  16 kryptografisch zufällige Bytes"),
    B("Salt macht Rainbow-Tables wirkungslos"),
    B("Gleiche Passwörter  →  verschiedene Hashes"),
    B("SHA-256 ist Einweg-Funktion"),
]

# --- Folie 7: MiniMax-Algorithmus ---
cards.append(Spacer(1, 6*mm))
cards += card_header(7, "MiniMax-Algorithmus", "mit Alpha-Beta-Pruning")
cards += [
    B("Rekursive Spielbaumsuche bis zur Tiefe N"),
    B("KI = Maximizer · Mensch = Minimizer"),
    B("Alpha-Beta: irrelevante Äste werden abgeschnitten"),
    S("Schwierigkeitsgrade  →  Suchtiefe"),
    SB("1 Leicht = Tiefe 1   |   2 Mittel = Tiefe 2"),
    SB("3 Schwer = Tiefe 3   |   4 Experte = Tiefe 4"),
    SB("5 Meister = Tiefe 5  (sehr stark, mehrere Sekunden)"),
]

# --- Folie 8: Callback-Design ---
cards.append(Spacer(1, 6*mm))
cards += card_header(8, "Callback-basiertes MiniMax-Design")
cards += [
    B("get_best_move() erhält Callbacks als Parameter:"),
    SB("get_moves_fn  → welche Züge gibt es?"),
    SB("apply_move_fn → Zug ausführen"),
    SB("evaluate_fn   → Bewertung des Zustands"),
    B("Kein Code-Duplikat: ein MiniMax für beide Spiele"),
    B("Single Responsibility: KI- & Spiellogik getrennt"),
    B("Einfach erweiterbar: drittes Spiel = neue Callbacks"),
]

# --- Folie 9: Bauernschach ---
cards.append(Spacer(1, 6*mm))
cards += card_header(9, "Bauernschach", "6×6 · Weiß (Mensch) vs. Schwarz (KI)")
cards += [
    S("Spielfeld"),
    B("6×6 Felder, nur Bauern  ·  Weiß Reihe 6, Schwarz Reihe 1"),
    S("Zugregeln"),
    B("Vorwärts 1 Feld (wenn frei)"),
    B("Diagonal schlagen möglich  ·  Kein Doppelschritt"),
    S("Gewinnbedingungen"),
    B("Gegnerische Grundlinie erreichen"),
    B("Alle Figuren des Gegners schlagen"),
    B("Gegner kann nicht mehr ziehen"),
    S("Bewertungsfunktion"),
    B("Figurenzahl + Fortschritt + Zentrumskontrolle"),
]

# --- Folie 10: Heuristik Bauernschach ---
cards.append(Spacer(1, 6*mm))
cards += card_header(10, "Bewertungsfunktion Bauernschach", "Heuristik: Figurenzahl · Fortschritt · Zentrum")
cards += [
    B("Figurenzahl: +10 pro eigener Bauer, -10 pro Gegner"),
    B("Fortschritt: +row×2 → KI wird für Vorwärtsbewegung belohnt"),
    B("Zentrum: +0 bis +3 (Zentralposition strategisch wertvoller)"),
    B("Positiv = gut für KI (Schwarz)  ·  Negativ = gut für Mensch"),
    B("CENTER_BONUS-Matrix definiert Feldwertigkeit"),
]

# --- Folie 11: Tic-Tac-Toe ---
cards.append(Spacer(1, 6*mm))
cards += card_header(11, "Tic-Tac-Toe (4 gewinnt)", "6×6 · Mensch (X) vs. KI (O)")
cards += [
    S("Spielregeln"),
    B("Abwechselnd Stein setzen · Mensch (X) beginnt"),
    B("4 in einer Reihe gewinnt (H/V/Diagonal)"),
    B("Unentschieden bei vollem Feld"),
    S("KI-Optimierungen"),
    B("Kandidatenzüge: nur Nachbarfelder (36 → 8–15 Züge)"),
    B("Center-Sorting: Zentrumsnähe für Alpha-Beta"),
    S("Bewertungsfunktion"),
    B("Dreier-Reihe: +50 / -50  ·  Zweier-Reihe: +10 / -10"),
    B("Mittelfeld-Bonus"),
]

# --- Folie 12: Optimierungen TTT ---
cards.append(Spacer(1, 6*mm))
cards += card_header(12, "TTT Optimierungen", "Kandidatenzüge · Center-Sorting · shallow copy")
cards += [
    B("Nur Nachbarfelder besetzter Felder als Kandidaten"),
    B("Center-Sorting → Alpha-Beta findet früh gute Äste"),
    B("[row[:] for row in board] statt deepcopy → ~5× schneller"),
]

# --- Folie 13: GUI & Threading ---
cards.append(Spacer(1, 6*mm))
cards += card_header(13, "GUI & Threading", "daemon Thread · after(0, ...) · app_state")
cards += [
    B("app_state{} als globaler Zustand (prozedural, kein OOP)"),
    SB("board, ai_thinking, difficulty, current_user, ..."),
    B("KI-Zug in separatem Thread → GUI bleibt reaktionsfähig"),
    B("daemon=True → Thread endet mit Fenster"),
    B("after(0, fn) → UI-Updates sicher in tkinter-Hauptthread"),
    B("tkinter ist nicht thread-safe → NIE Widgets aus Thread ändern"),
]

# --- Folie 14: Unittests ---
cards.append(Spacer(1, 6*mm))
cards += card_header(14, "Unittests", "TC-01 bis TC-15 · test_all.py · pytest-kompatibel")
cards += [
    B("TC-01–03: Passwort-Hashing (Generierung, Verifikation, Salt)"),
    B("TC-04–06: Benutzer-DB (Registrierung, Duplikat, Abfrage)"),
    B("TC-07–08: Spielergebnisse (Speichern, Bestenliste)"),
    B("TC-09–10: Bauernschach (Züge, Anwenden, Gewinner)"),
    B("TC-11–12: Tic-Tac-Toe (4-in-Reihe, Kandidatenzüge)"),
    B("TC-13–15: MiniMax (offens. Zug, Gewinn erkennen, Blockieren)"),
]

# --- Folie 15: Test-Techniken ---
cards.append(Spacer(1, 6*mm))
cards += card_header(15, "Test-Infrastruktur", "unittest · Temp-DB-Isolation · Mocking")
cards += [
    B("DBTestCase: jeder Test bekommt frische Temp-DB"),
    B("tempfile.mkstemp('.db') → isolierte Datenbankdatei"),
    B("patch.object(database, 'DB_PATH') → keine Produktions-DB"),
    B("assertEqual testet 4-in-Reihe-Erkennung direkt"),
]

# --- Folie 16: Zusammenfassung ---
cards.append(Spacer(1, 6*mm))
cards += card_header(16, "Zusammenfassung")
cards += [
    B("✅ Zwei vollständige Strategiespiele auf 6×6-Feld"),
    B("🤖 Wiederverwendbarer MiniMax + Alpha-Beta-Pruning"),
    B("🔒 Sichere Authentifizierung: SHA-256 + Salt"),
    B("📦 SQLite: keine externen Abhängigkeiten"),
    B("🖥️ tkinter-GUI: Windows / macOS / Linux"),
    B("🧪 15 Unittests sichern Kernfunktionen ab"),
]

# --- Folie 17: SOLL/IST Features ---
cards.append(Spacer(1, 6*mm))
cards += card_header(17, "SOLL/IST Feature-Vergleich", "Lastenheft → Pflichtenheft → Umsetzung → Test")
cards += [
    S("MUSS-Ziele: 12/12 ✅"),
    B("2 Spiele · 6×6 Brett · 5 Schwierigkeitsgrade"),
    B("Login · Registrierung · Gastmodus · Spielabbruch · Regelanzeige"),
    B("Bestenliste · SHA-256-Hashing · MiniMax-KI · Unittests"),
    S("SOLL-Ziele: 2/2 ✅"),
    B("Alpha-Beta-Pruning · SQL-Bestenliste"),
    S("KANN-Ziele: 2/4 ⚠"),
    B("✅ Sprachwechsel EN/DE · Sprachpräferenz in DB"),
    B("❌ Dame (drittes Spiel) · Alt-KI-Schnittstelle (zeitbedingt)"),
]

# --- Folie 18: Projektplanung ---
cards.append(Spacer(1, 6*mm))
cards += card_header(18, "SOLL/IST Projektplanung", "Wasserfallmodell · 2 Meetings · Discord & WhatsApp")
cards += [
    B("Analysephase (Woche 1: 20.04.–24.04.) ✅ plangemäß"),
    B("Implementierung (27.04.–04.05.) ⚠ +1 Tag (01.05. Feiertag)"),
    B("Test & Doku: parallel zur Impl. statt sequenziell ⚠"),
    B("Abschluss (Woche 3) ✅ plangemäß"),
    B("Discord-Channel statt Kanban-Board"),
    B("2 Team-Meetings: 27.04. & 29.04. je 10:00 Uhr"),
]

# --- Folie 19: GUI ---
cards.append(Spacer(1, 6*mm))
cards += card_header(19, "Benutzeroberfläche (GUI)", "tkinter · HHBKTendo Design System · Dark Theme")
cards += [
    S("Screen-Flow"),
    B("① Login → Login / Register / Als Gast spielen"),
    B("② Hauptmenü → Spiel · Schwierigkeit · Play · Bestenliste"),
    B("③ Spielscreen → 6×6 Brett · Züge per Klick"),
    S("Design-System (Farben)"),
    SB("#0D0D1A Deep Navy (BG)  ·  #E94560 Hot Pink (Primär)"),
    SB("#6C3FC5 Royal Purple  ·  #00D4FF Cyber Cyan (Akzent)"),
    S("tkinter-Besonderheiten"),
    B("Buttons als tk.Label + Bindings (macOS-Bug: bg/fg)"),
    B("KI in separatem Thread · after(0, cb) für GUI-Rückkehr"),
]

# --- Folie 20: Quellen ---
cards.append(Spacer(1, 6*mm))
cards += card_header(20, "Quellen & Werkzeuge")
cards += [
    S("Entwicklungsumgebungen"),
    B("PyCharm (JetBrains)  ·  Visual Studio Code (Microsoft)"),
    S("KI-Assistenten"),
    B("Claude (Anthropic)  ·  ChatGPT (OpenAI)"),
    S("Python-Bibliotheken (alle stdlib außer Pillow)"),
    B("tkinter · sqlite3 · hashlib · threading · Pillow (GIF)"),
    S("Quellen"),
    B("Wikipedia: MiniMax · Alpha-Beta-Pruning"),
    B("HHBK Lernfeld 5 – Unterrichtsmaterial"),
    B("docs.python.org – Python-Dokumentation"),
]

# --- Folie 21: Fazit ---
cards.append(Spacer(1, 6*mm))
cards += card_header(21, "Fazit – Projektverlauf")
cards += [
    S("Team & Rollen"),
    B("Lucas – Projektleitung, auth.py, Testing"),
    B("Jesse – database.py, Pitch, Testing"),
    B("Arda – database.py, Testing"),
    B("Uilliam – GUI (main.py), Design"),
    B("Jakub – pawn_chess.py  ·  Niklas – minimax.py"),
    S("Highlights"),
    B("Spielunabhängige MiniMax-Schnittstelle"),
    B("Reibungslose Teamarbeit dank klarem Pflichtenheft"),
    S("Lessons Learnt"),
    B("Kanban-Board früher einsetzen"),
    B("Schnittstellen detaillierter im Pflichtenheft definieren"),
    S("Ausblick"),
    B("Dame als drittes Spiel · Sprach-Auswahl ausbauen"),
]

# Build PDF with background
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate
from reportlab.lib.units import mm

class DarkDoc(BaseDocTemplate):
    def __init__(self, filename, **kwargs):
        super().__init__(filename, **kwargs)
        frame = Frame(
            self.leftMargin, self.bottomMargin,
            self.width, self.height,
            id="normal"
        )
        template = PageTemplate(id="dark", frames=frame, onPage=self._draw_bg)
        self.addPageTemplates([template])

    def _draw_bg(self, canvas, doc):
        canvas.saveState()
        canvas.setFillColor(BG)
        canvas.rect(0, 0, W, H, fill=1, stroke=0)
        canvas.restoreState()

doc2 = DarkDoc(
    OUTPUT,
    pagesize=A5,
    leftMargin=12*mm,
    rightMargin=12*mm,
    topMargin=10*mm,
    bottomMargin=10*mm,
)
doc2.build(cards)
print(f"PDF erstellt: {OUTPUT}")
