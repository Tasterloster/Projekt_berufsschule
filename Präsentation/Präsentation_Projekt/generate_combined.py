from reportlab.lib.pagesizes import A5
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    Paragraph, Spacer, HRFlowable, PageBreak,
    BaseDocTemplate, Frame, PageTemplate,
)

OUTPUT = "HHBKTendo_Komplett.pdf"

BG     = colors.HexColor("#0D0D1A")
PINK   = colors.HexColor("#E94560")
PURPLE = colors.HexColor("#6C3FC5")
CYAN   = colors.HexColor("#00D4FF")
WHITE  = colors.HexColor("#FFFFFF")
LIGHT  = colors.HexColor("#C8C8DC")
YELLOW = colors.HexColor("#FFD700")
GREEN  = colors.HexColor("#00C853")

W, H = A5

# ── Styles ────────────────────────────────────────────────────────────────────

_sn  = ParagraphStyle("SN",  fontName="Helvetica",        fontSize=8,  textColor=PURPLE, alignment=TA_CENTER, spaceAfter=1)
_ttl = ParagraphStyle("TTL", fontName="Helvetica-Bold",   fontSize=13, textColor=PINK,   spaceAfter=3,  leading=16)
_sub = ParagraphStyle("SUB", fontName="Helvetica-Oblique",fontSize=9,  textColor=CYAN,   spaceAfter=5,  leading=12)
_bdy = ParagraphStyle("BDY", fontName="Helvetica",        fontSize=10, textColor=WHITE,  spaceAfter=6,  leading=15, alignment=TA_JUSTIFY)
_sec = ParagraphStyle("SEC", fontName="Helvetica-Bold",   fontSize=10, textColor=CYAN,   spaceAfter=3,  spaceBefore=7, leading=13)
_bul = ParagraphStyle("BUL", fontName="Helvetica",        fontSize=10, textColor=WHITE,  leftIndent=12, spaceAfter=4,  leading=14)
_sbul= ParagraphStyle("SBL", fontName="Helvetica",        fontSize=9,  textColor=LIGHT,  leftIndent=22, spaceAfter=3,  leading=12)
_tip = ParagraphStyle("TIP", fontName="Helvetica-Bold",   fontSize=9,  textColor=YELLOW, spaceAfter=4,  leading=13)
_lbl = ParagraphStyle("LBL", fontName="Helvetica-Bold",   fontSize=7,  textColor=BG,     alignment=TA_CENTER, leading=9)

def P(t):   return Paragraph(t, _bdy)
def SEC(t): return Paragraph(t, _sec)
def B(t):   return Paragraph(f"▸  {t}", _bul)
def SB(t):  return Paragraph(f"·  {t}", _sbul)
def TIP(t): return Paragraph(f"💡 {t}", _tip)
def HR():   return HRFlowable(width="100%", thickness=0.5, color=PURPLE, spaceAfter=5, spaceBefore=2)
def SP(h=4):return Spacer(1, h*mm)

def _badge(text, bg):
    """Coloured pill label rendered as a mini table-like paragraph."""
    style = ParagraphStyle("badge", fontName="Helvetica-Bold", fontSize=7,
        textColor=BG, backColor=bg, alignment=TA_CENTER,
        borderPad=2, leading=9, spaceAfter=3)
    return Paragraph(f"  {text}  ", style)

def stich_header(num, title, subtitle=""):
    return [
        _badge(f"FOLIE {num}  ·  STICHWORTE", PINK),
        Paragraph(title, _ttl),
        *([ Paragraph(subtitle, _sub) ] if subtitle else []),
        HR(),
    ]

def detail_header(num, title, subtitle=""):
    return [
        _badge(f"FOLIE {num}  ·  VOLLTEXT", GREEN),
        Paragraph(title, _ttl),
        *([ Paragraph(subtitle, _sub) ] if subtitle else []),
        HR(),
    ]

# ── Dark background ────────────────────────────────────────────────────────────

class DarkDoc(BaseDocTemplate):
    def __init__(self, fn, **kw):
        super().__init__(fn, **kw)
        frame = Frame(self.leftMargin, self.bottomMargin, self.width, self.height, id="n")
        self.addPageTemplates([PageTemplate(id="dark", frames=frame, onPage=self._bg)])

    def _bg(self, canvas, doc):
        canvas.saveState()
        canvas.setFillColor(BG)
        canvas.rect(0, 0, W, H, fill=1, stroke=0)
        canvas.restoreState()

# ── Slides ─────────────────────────────────────────────────────────────────────
# Each entry: (stichkarte_content, sprechernotizen_content)
# Both are lists of Flowables (NO PageBreak inside – added automatically).

slides = []

# ── Folie 1 ───────────────────────────────────────────────────────────────────
slides.append((
    stich_header(1, "HHBKTendo – Spielesammlung", "HHBK Düsseldorf · Lernfeld 5 · 2026") + [
        B("Strategiespiele mit MiniMax-KI"),
        B("Bauernschach & Tic-Tac-Toe (4 gewinnt)"),
        B("Tech-Stack: Python 3.10+ · SQLite · tkinter"),
    ],
    detail_header(1, "HHBKTendo – Spielesammlung", "Eröffnung") + [
        P("Guten Tag, wir präsentieren heute <b>HHBKTendo</b> – eine Spielesammlung, die im Rahmen von Lernfeld 5 an der HHBK Düsseldorf entwickelt wurde."),
        P("Das Projekt besteht aus zwei Strategiespielen – <b>Bauernschach</b> und <b>Tic-Tac-Toe (4 gewinnt)</b> – jeweils auf einem 6×6-Spielfeld, gegen eine KI die auf dem MiniMax-Algorithmus basiert."),
        P("Technisch setzt das Projekt auf <b>Python 3.10+</b>, eine <b>SQLite-Datenbank</b> und eine <b>tkinter-Oberfläche</b> – alles ohne externe Abhängigkeiten außer Pillow für Animationen."),
        TIP("Kurze Vorstellung des Teams vor dem Start, dann direkt in den Überblick."),
    ],
))

# ── Folie 2 ───────────────────────────────────────────────────────────────────
slides.append((
    stich_header(2, "Projektüberblick") + [
        SEC("🎮 Spielesammlung"),
        B("2 Spiele auf je 6×6-Feld"),
        SEC("🤖 KI-Gegner"),
        B("MiniMax + Alpha-Beta-Pruning"),
        B("Kein Code-Duplikat für beide Spiele"),
        SEC("👤 Benutzerverwaltung"),
        B("Login / Registrierung · SHA-256-Hashing · Gast-Modus"),
        SEC("📊 Bestenliste"),
        B("SQLite · Rangliste nach Schwierigkeitsgrad"),
    ],
    detail_header(2, "Projektüberblick") + [
        P("Das Projekt hat vier Kernbereiche:"),
        B("<b>Spielesammlung:</b> Zwei vollständige Strategiespiele auf einem 6×6-Feld, komplett spielbar gegen eine KI."),
        B("<b>KI-Gegner:</b> Ein einziger, wiederverwendbarer MiniMax-Algorithmus mit Alpha-Beta-Pruning für beide Spiele – kein duplizierter Code."),
        B("<b>Benutzerverwaltung:</b> Registrierung und Login mit SHA-256-Hashing und Salt. Alternativ: Gast-Modus ohne Konto."),
        B("<b>Bestenliste:</b> Alle Spielergebnisse werden in SQLite gespeichert und können nach Spiel und Schwierigkeitsgrad abgerufen werden."),
        TIP("Überblick-Folie – ruhig etwas langsamer sprechen, damit alle folgen können."),
    ],
))

# ── Folie 3 ───────────────────────────────────────────────────────────────────
slides.append((
    stich_header(3, "Projektstruktur") + [
        B("main.py  → GUI, Screens, app_state"),
        B("minimax.py  → generischer MiniMax + Alpha-Beta"),
        B("pawn_chess.py  → Bauernschach Züge & Bewertung"),
        B("tictactoe.py  → Tic-Tac-Toe Züge & Bewertung"),
        B("auth.py  → Login & Registrierung (SHA-256 + Salt)"),
        B("database.py  → SQLite CRUD (User & Ergebnisse)"),
        B("test_all.py  → 15 Unittests (TC-01 bis TC-15)"),
        B("games.db  → wird automatisch erstellt"),
    ],
    detail_header(3, "Projektstruktur", "Modularer Aufbau") + [
        P("Das Projekt ist in sieben Python-Dateien aufgeteilt, jede mit einer klar definierten Aufgabe:"),
        B("<b>main.py</b> – Der GUI-Einstiegspunkt. Verwaltet alle Screens und den globalen Zustand über das app_state-Dictionary."),
        B("<b>minimax.py</b> – Die KI-Engine. Generischer MiniMax mit Alpha-Beta-Pruning, nutzbar für jedes Spiel per Callbacks."),
        B("<b>pawn_chess.py / tictactoe.py</b> – Die eigentliche Spiellogik: erlaubte Züge, Anwenden, Gewinner, Bewertung."),
        B("<b>auth.py</b> – Registrierung und Login mit SHA-256-Hashing und Salt."),
        B("<b>database.py</b> – Alle Datenbankoperationen: Nutzer anlegen, Ergebnisse speichern, Bestenliste abfragen."),
        B("<b>test_all.py</b> – 15 Unittests (TC-01 bis TC-15), pytest-kompatibel."),
        TIP("Auf die klare Trennung der Zuständigkeiten hinweisen – jede Datei hat genau eine Aufgabe."),
    ],
))

# ── Folie 4 ───────────────────────────────────────────────────────────────────
slides.append((
    stich_header(4, "Benutzerverwaltung & Datenbank", "auth.py · database.py") + [
        SEC("auth.py – Kernfunktionen"),
        B("register() → Validierung + SHA-256 + Salt"),
        B("login() → Passwort-Hash-Vergleich"),
        B("save/load_session() → session.json für Auto-Login"),
        B("logout() → Session löschen"),
        B("is_guest() → Gast = keine Statistiken"),
        SEC("SQLite-Tabellen"),
        B("users: id, username, password_hash, language, created_at"),
        B("results: id, user_id (FK), game, difficulty, won, played_at"),
    ],
    detail_header(4, "Benutzerverwaltung & Datenbank", "auth.py · database.py") + [
        SEC("auth.py – Funktionen"),
        B("<b>register()</b>: Prüft ob der Username schon vergeben ist, hasht das Passwort mit SHA-256 + Salt und speichert den neuen Nutzer in der DB."),
        B("<b>login()</b>: Lädt den gespeicherten Hash aus der DB, wendet denselben Salt an und vergleicht das Ergebnis."),
        B("<b>save_session() / load_session()</b>: Schreiben bzw. lesen die user_id in eine session.json – so bleibt man beim nächsten Start eingeloggt."),
        B("<b>logout()</b>: Löscht die session.json und setzt den app_state zurück."),
        B("<b>is_guest()</b>: Gibt True zurück wenn kein Nutzer eingeloggt ist – Gäste sehen keine Statistiken."),
        SEC("SQLite-Tabellen"),
        B("<b>users:</b> id, username, password_hash, language, created_at"),
        B("<b>results:</b> id, user_id (Fremdschlüssel), game, difficulty, won, played_at"),
        TIP("Kurz erwähnen dass die DB automatisch erstellt wird wenn sie noch nicht existiert."),
    ],
))

# ── Folie 5 ───────────────────────────────────────────────────────────────────
slides.append((
    stich_header(5, "DB-Techniken", "row_factory · Schema-Migration · SQL-Injection-Schutz") + [
        B("sqlite3.Row  →  Spaltenzugriff per Name: row['username']"),
        B("dict(row)  →  einfache Konvertierung für die App"),
        B("?-Platzhalter  →  schützt vor SQL-Injection"),
        B("try/except bei ALTER TABLE  →  DB bleibt kompatibel"),
    ],
    detail_header(5, "Datenbank-Techniken", "row_factory · Migration · SQL-Injection-Schutz") + [
        P("Wir nutzen drei wichtige Techniken für eine robuste Datenbankanbindung:"),
        SEC("sqlite3.Row als row_factory"),
        P("Statt Spalten per Index anzusprechen (row[1]) kann man sie per Name abrufen: row['username']. Das macht den Code lesbarer und weniger fehleranfällig. Mit dict(row) lässt sich das Ergebnis einfach in ein Dictionary umwandeln."),
        SEC("SQL-Injection-Schutz"),
        P("Alle SQL-Abfragen verwenden <b>?-Platzhalter</b> statt String-Konkatenation. SQLite ersetzt die Platzhalter sicher und verhindert so, dass Nutzereingaben als SQL-Code interpretiert werden."),
        SEC("Schema-Migration"),
        P("ALTER TABLE läuft in einem try/except-Block. Falls die Spalte schon existiert, wird der Fehler ignoriert – so bleibt die DB abwärtskompatibel."),
        TIP("Gutes Beispiel für defensives Programmieren – kurz den Sicherheitsaspekt betonen."),
    ],
))

# ── Folie 6 ───────────────────────────────────────────────────────────────────
slides.append((
    stich_header(6, "Sichere Passwortspeicherung", "SHA-256 + Salt") + [
        B("Kein Klartext – nur 'salt:hash' in der DB"),
        B("os.urandom(16)  →  16 kryptografisch zufällige Bytes"),
        B("Salt macht Rainbow-Tables wirkungslos"),
        B("Gleiche Passwörter  →  verschiedene Hashes"),
        B("SHA-256 ist Einweg-Funktion"),
    ],
    detail_header(6, "Sichere Passwortspeicherung", "SHA-256 + Salt") + [
        P("Passwörter werden niemals im Klartext gespeichert. Stattdessen wird ein <b>kryptografischer Hash</b> mit einem zufälligen Salt erzeugt:"),
        B("<b>os.urandom(16)</b> erzeugt 16 kryptografisch zufällige Bytes als Salt. Ein zufälliger Salt sorgt dafür, dass zwei gleiche Passwörter unterschiedliche Hashes erzeugen."),
        B("<b>Rainbow-Tables</b> sind vorberechnete Tabellen mit Passwort-Hash-Paaren. Durch den einzigartigen Salt wird diese Angriffsmethode wirkungslos."),
        B("<b>SHA-256</b> ist eine Einweg-Hashfunktion – aus dem Hash lässt sich das ursprüngliche Passwort nicht zurückberechnen."),
        B("In der Datenbank wird nur <b>'salt:hash'</b> gespeichert – niemals das Passwort selbst."),
        P("Beim Login wird der gespeicherte Salt verwendet, das eingegebene Passwort erneut gehasht und das Ergebnis verglichen."),
        TIP("Falls jemand fragt: SHA-256 ist für dieses Schulprojekt ausreichend. Produktive Systeme würden bcrypt oder argon2 verwenden."),
    ],
))

# ── Folie 7 ───────────────────────────────────────────────────────────────────
slides.append((
    stich_header(7, "MiniMax-Algorithmus", "mit Alpha-Beta-Pruning") + [
        B("Rekursive Spielbaumsuche bis zur Tiefe N"),
        B("KI = Maximizer · Mensch = Minimizer"),
        B("Alpha-Beta: irrelevante Äste werden abgeschnitten"),
        SEC("Schwierigkeitsgrade  →  Suchtiefe"),
        SB("1 Leicht = Tiefe 1   |   2 Mittel = Tiefe 2"),
        SB("3 Schwer = Tiefe 3   |   4 Experte = Tiefe 4"),
        SB("5 Meister = Tiefe 5  (sehr stark, mehrere Sekunden)"),
    ],
    detail_header(7, "MiniMax-Algorithmus", "mit Alpha-Beta-Pruning") + [
        P("Der MiniMax-Algorithmus ist die KI-Grundlage beider Spiele. Er funktioniert wie folgt:"),
        B("Der Algorithmus baut einen <b>Spielbaum</b> auf – er simuliert alle möglichen Züge bis zu einer festgelegten Tiefe und bewertet jeden Endzustand."),
        B("Es gibt zwei Spieler: den <b>Maximizer</b> (die KI, die einen möglichst hohen Score will) und den <b>Minimizer</b> (der Mensch, der den Score möglichst niedrig halten will). Beide spielen optimal."),
        B("<b>Alpha-Beta-Pruning</b> ist eine Optimierung: Äste des Spielbaums, die das Ergebnis nicht mehr beeinflussen können, werden abgeschnitten. Das spart Rechenzeit deutlich."),
        SEC("Schwierigkeitsgrade = Suchtiefe"),
        B("Tiefe 1 (Leicht) – kaum strategisch   |   Tiefe 3 (Schwer) – Standard"),
        B("Tiefe 5 (Meister) – sehr stark, kann mehrere Sekunden dauern"),
        TIP("Visualisierung: Spielbaum mit Max/Min-Ebenen kurz erklären, dann auf Alpha-Beta eingehen."),
    ],
))

# ── Folie 8 ───────────────────────────────────────────────────────────────────
slides.append((
    stich_header(8, "Callback-basiertes MiniMax-Design") + [
        B("get_best_move() erhält Callbacks als Parameter:"),
        SB("get_moves_fn  → welche Züge gibt es?"),
        SB("apply_move_fn → Zug ausführen"),
        SB("evaluate_fn   → Bewertung des Zustands"),
        B("Kein Code-Duplikat: ein MiniMax für beide Spiele"),
        B("Single Responsibility: KI- & Spiellogik getrennt"),
        B("Einfach erweiterbar: drittes Spiel = neue Callbacks"),
    ],
    detail_header(8, "Callback-basiertes MiniMax-Design", "Eine KI-Engine für alle Spiele") + [
        P("Das Herzstück des Designs: Die MiniMax-Funktion get_best_move() kennt kein spezifisches Spiel. Stattdessen bekommt sie drei Callback-Funktionen übergeben:"),
        B("<b>get_moves_fn</b> – gibt die Liste aller gültigen Züge für den aktuellen Spielzustand zurück."),
        B("<b>apply_move_fn</b> – wendet einen Zug auf das Spielfeld an und gibt den neuen Zustand zurück."),
        B("<b>evaluate_fn</b> – bewertet einen Spielzustand mit einem numerischen Score."),
        P("Diese drei Funktionen werden für jedes Spiel separat implementiert. Der MiniMax-Code selbst muss dafür nicht verändert werden."),
        SEC("Vorteile"),
        B("Kein duplizierter Code – dieselbe KI-Logik für beide Spiele."),
        B("Single Responsibility – KI und Spiellogik vollständig getrennt."),
        B("Einfach erweiterbar – ein drittes Spiel braucht nur neue Callbacks."),
        TIP("Gutes Beispiel für Clean Code und das Open/Closed Principle."),
    ],
))

# ── Folie 9 ───────────────────────────────────────────────────────────────────
slides.append((
    stich_header(9, "Bauernschach", "6×6 · Weiß (Mensch) vs. Schwarz (KI)") + [
        SEC("Spielfeld"),
        B("6×6 Felder, nur Bauern  ·  Weiß Reihe 6, Schwarz Reihe 1"),
        SEC("Zugregeln"),
        B("Vorwärts 1 Feld (wenn frei)"),
        B("Diagonal schlagen möglich  ·  Kein Doppelschritt"),
        SEC("Gewinnbedingungen"),
        B("Gegnerische Grundlinie erreichen"),
        B("Alle Figuren des Gegners schlagen"),
        B("Gegner kann nicht mehr ziehen"),
        SEC("Bewertungsfunktion"),
        B("Figurenzahl + Fortschritt + Zentrumskontrolle"),
    ],
    detail_header(9, "Bauernschach", "6×6 · Weiß (Mensch) vs. Schwarz (KI)") + [
        P("Bauernschach ist eine vereinfachte Schachvariante, bei der nur Bauern auf einem 6×6-Feld gespielt werden."),
        SEC("Aufbau"),
        B("Weiß (Mensch) startet in Reihe 6, Schwarz (KI) in Reihe 1. Beide Seiten haben je sechs Bauern."),
        SEC("Zugregeln"),
        B("Ein Bauer kann <b>ein Feld vorwärts</b> ziehen, wenn das Zielfeld frei ist."),
        B("<b>Diagonal schlagen</b>: Ein Bauer kann diagonal nach vorne ziehen, wenn dort ein gegnerischer Bauer steht."),
        B("Kein Doppelschritt – anders als im echten Schach."),
        SEC("Gewinnbedingungen"),
        B("Die gegnerische <b>Grundlinie erreichen</b> (Umwandlung)."),
        B("<b>Alle Figuren</b> des Gegners schlagen."),
        B("Der Gegner kann <b>keinen Zug mehr</b> machen."),
        TIP("Kurz zeigen wie das Spiel aussieht (Screenshot auf der Folie)."),
    ],
))

# ── Folie 10 ──────────────────────────────────────────────────────────────────
slides.append((
    stich_header(10, "Bewertungsfunktion Bauernschach", "Figurenzahl · Fortschritt · Zentrum") + [
        B("Figurenzahl: +10 pro eigener Bauer, -10 pro Gegner"),
        B("Fortschritt: +row×2 → KI wird für Vorwärtsbewegung belohnt"),
        B("Zentrum: +0 bis +3 (Zentralposition strategisch wertvoller)"),
        B("Positiv = gut für KI (Schwarz)  ·  Negativ = gut für Mensch"),
        B("CENTER_BONUS-Matrix definiert Feldwertigkeit"),
    ],
    detail_header(10, "Bewertungsfunktion Bauernschach", "Heuristik: Figurenzahl · Fortschritt · Zentrum") + [
        P("Die Bewertungsfunktion gibt der KI einen numerischen Score für jede Spielposition. Ein <b>positiver Wert</b> bedeutet, die KI steht gut; ein negativer, dass der Mensch im Vorteil ist."),
        B("<b>Figurenzahl (+10 pro eigener Bauer):</b> Jeder eigene Bauer zählt +10, jeder gegnerische -10. Wer mehr Figuren hat, steht besser."),
        B("<b>Fortschritt (+row×2):</b> Je weiter ein Bauer der KI nach vorne gerückt ist, desto mehr Punkte bekommt er. Das motiviert die KI, vorwärtszuspielen."),
        B("<b>Zentrumskontrolle (+0 bis +3):</b> Felder in der Mitte des Bretts sind strategisch wertvoller. Die CENTER_BONUS-Matrix vergibt Boni von 0 (Rand) bis 3 (Zentrum)."),
        TIP("Kurz erklären warum eine gute Heuristik wichtiger ist als eine höhere Suchtiefe."),
    ],
))

# ── Folie 11 ──────────────────────────────────────────────────────────────────
slides.append((
    stich_header(11, "Tic-Tac-Toe (4 gewinnt)", "6×6 · Mensch (X) vs. KI (O)") + [
        SEC("Spielregeln"),
        B("Abwechselnd Stein setzen · Mensch (X) beginnt"),
        B("4 in einer Reihe gewinnt (H/V/Diagonal)"),
        B("Unentschieden bei vollem Feld"),
        SEC("KI-Optimierungen"),
        B("Kandidatenzüge: nur Nachbarfelder (36 → 8–15 Züge)"),
        B("Center-Sorting: Zentrumsnähe für Alpha-Beta"),
        SEC("Bewertungsfunktion"),
        B("Dreier-Reihe: +50 / -50  ·  Zweier-Reihe: +10 / -10"),
        B("Mittelfeld-Bonus"),
    ],
    detail_header(11, "Tic-Tac-Toe (4 gewinnt)", "6×6 · Mensch (X) vs. KI (O)") + [
        P("Die zweite Spielvariante: Vier in einer Reihe auf einem 6×6-Feld – eine Erweiterung des klassischen Tic-Tac-Toe."),
        SEC("Spielregeln"),
        B("Mensch (X) und KI (O) setzen abwechselnd Steine, der Mensch beginnt."),
        B("Wer zuerst <b>vier Steine in einer Reihe</b> hat – horizontal, vertikal oder diagonal – gewinnt."),
        B("Bei vollem Feld ohne Gewinner: <b>Unentschieden</b>."),
        SEC("KI-Optimierungen"),
        B("<b>Kandidatenzüge:</b> Statt alle 36 Felder zu prüfen, betrachtet die KI nur Nachbarfelder besetzter Felder. Das reduziert die Züge auf 8–15."),
        B("<b>Center-Sorting:</b> Kandidaten werden nach Zentrumsnähe sortiert. Alpha-Beta findet dadurch früher gute Äste und schneidet mehr ab."),
        SEC("Bewertungsfunktion"),
        B("Dreier-Reihe: +50 / -50  ·  Zweier-Reihe: +10 / -10  ·  Mittelfeld-Bonus"),
        TIP("Unentschieden kommt selten vor – erwähnen falls jemand fragt."),
    ],
))

# ── Folie 12 ──────────────────────────────────────────────────────────────────
slides.append((
    stich_header(12, "TTT Optimierungen", "Kandidatenzüge · Center-Sorting · shallow copy") + [
        B("Nur Nachbarfelder besetzter Felder als Kandidaten"),
        B("Center-Sorting → Alpha-Beta findet früh gute Äste"),
        B("[row[:] for row in board] statt deepcopy → ~5× schneller"),
    ],
    detail_header(12, "TTT Optimierungen im Detail", "Kandidatenzüge · Center-Sorting · shallow copy") + [
        SEC("Kandidatenzüge"),
        P("In einem 6×6-Feld gibt es anfangs 36 mögliche Züge. Die KI schränkt das auf Felder ein, die direkt neben einem bereits besetzten Feld liegen. Ein Stein ohne Nachbarn ist strategisch fast wertlos. Dadurch sinkt die Anzahl der zu prüfenden Züge auf typischerweise 8–15."),
        SEC("Center-Sorting"),
        P("Kandidaten werden vor der Auswertung nach Entfernung zum Mittelpunkt sortiert. Da Alpha-Beta bessere Züge zuerst sehen und mehr Äste abschneiden kann, beschleunigt das die Suche erheblich."),
        SEC("shallow copy statt deepcopy"),
        P("Das Spielfeld wird als [row[:] for row in board] kopiert – etwa 5× schneller als deepcopy(board), weil nur die Zeilenlisten flach kopiert werden. Für ein 6×6-Feld mit ganzen Zahlen ist das vollständig korrekt."),
        TIP("Wer fragt: deepcopy wäre korrekt für verschachtelte Objekte, hier aber nicht nötig."),
    ],
))

# ── Folie 13 ──────────────────────────────────────────────────────────────────
slides.append((
    stich_header(13, "GUI & Threading", "daemon Thread · after(0, ...) · app_state") + [
        B("app_state{} als globaler Zustand (prozedural, kein OOP)"),
        SB("board, ai_thinking, difficulty, current_user, ..."),
        B("KI-Zug in separatem Thread → GUI bleibt reaktionsfähig"),
        B("daemon=True → Thread endet mit Fenster"),
        B("after(0, fn) → UI-Updates sicher in tkinter-Hauptthread"),
        B("tkinter ist nicht thread-safe → NIE Widgets aus Thread ändern"),
    ],
    detail_header(13, "GUI & Threading", "daemon Thread · after(0, ...) · app_state") + [
        SEC("app_state – globaler Zustand"),
        P("Statt Klassen wird der gesamte Programmzustand in einem einzigen Dictionary app_state gespeichert. Das enthält das aktuelle Spielfeld, den eingeloggten Nutzer, die gewählte Schwierigkeit, und ob die KI gerade denkt."),
        SEC("KI-Zug in separatem Thread"),
        P("Der MiniMax-Algorithmus kann bei höheren Schwierigkeitsgraden mehrere Sekunden rechnen. Würde er im Hauptthread laufen, würde das GUI einfrieren. Deshalb läuft der KI-Zug in einem separaten Thread."),
        B("<b>daemon=True</b>: Der Thread wird automatisch beendet wenn das Fenster geschlossen wird – kein Aufräumen nötig."),
        SEC("after(0, callback) – Thread-Safety"),
        P("tkinter ist nicht thread-safe. Widgets dürfen nur aus dem Hauptthread verändert werden. Deshalb ruft der KI-Thread am Ende after(0, fn) auf – das marshallt den GUI-Update sicher in den tkinter-Hauptthread zurück."),
        TIP("Gute technische Frage vorhersagen: 'Warum kann man tkinter nicht aus dem Thread aufrufen?' → Event-Loop-Architektur."),
    ],
))

# ── Folie 14 ──────────────────────────────────────────────────────────────────
slides.append((
    stich_header(14, "Unittests", "TC-01 bis TC-15 · test_all.py · pytest-kompatibel") + [
        B("TC-01–03: Passwort-Hashing (Generierung, Verifikation, Salt)"),
        B("TC-04–06: Benutzer-DB (Registrierung, Duplikat, Abfrage)"),
        B("TC-07–08: Spielergebnisse (Speichern, Bestenliste)"),
        B("TC-09–10: Bauernschach (Züge, Anwenden, Gewinner)"),
        B("TC-11–12: Tic-Tac-Toe (4-in-Reihe, Kandidatenzüge)"),
        B("TC-13–15: MiniMax (offens. Zug, Gewinn erkennen, Blockieren)"),
    ],
    detail_header(14, "Unittests", "TC-01 bis TC-15 · test_all.py · pytest-kompatibel") + [
        P("Das Projekt umfasst 15 Unittests, die alle Kernfunktionen abdecken:"),
        B("<b>TC-01–03 (Passwort-Hashing):</b> Prüft ob ein Hash korrekt generiert wird, ob die Verifikation funktioniert, und ob zwei gleiche Passwörter verschiedene Hashes erzeugen."),
        B("<b>TC-04–06 (Benutzer-DB):</b> Registrierung eines neuen Nutzers, Erkennung von Duplikaten, Abfrage des Nutzerprofils."),
        B("<b>TC-07–08 (Spielergebnisse):</b> Speichern eines Ergebnisses, korrekte Bestenliste abrufen."),
        B("<b>TC-09–10 (Bauernschach):</b> Gültige Züge generieren, Zug anwenden, Gewinner erkennen."),
        B("<b>TC-11–12 (Tic-Tac-Toe):</b> Vier-in-Reihe korrekt erkennen, Kandidatenzüge korrekt einschränken."),
        B("<b>TC-13–15 (MiniMax-KI):</b> Offensichtlichen Gewinnzug finden, drohenden Gewinn des Gegners blockieren."),
        TIP("Erwähnen dass die Tests mit 'python -m pytest test_all.py' ausgeführt werden."),
    ],
))

# ── Folie 15 ──────────────────────────────────────────────────────────────────
slides.append((
    stich_header(15, "Test-Infrastruktur", "unittest · Temp-DB-Isolation · Mocking") + [
        B("DBTestCase: jeder Test bekommt frische Temp-DB"),
        B("tempfile.mkstemp('.db') → isolierte Datenbankdatei"),
        B("patch.object(database, 'DB_PATH') → keine Produktions-DB"),
        B("assertEqual testet 4-in-Reihe-Erkennung direkt"),
    ],
    detail_header(15, "Test-Infrastruktur", "unittest · Temp-DB · Mocking") + [
        P("Damit Tests unabhängig voneinander und von der echten Datenbank laufen, verwenden wir Isolation durch temporäre Datenbanken:"),
        SEC("DBTestCase"),
        P("Jeder Testfall erbt von DBTestCase. In setUp() wird per tempfile.mkstemp() eine neue temporäre DB-Datei erstellt. Nach dem Test wird sie wieder gelöscht. So beeinflussen sich Tests nicht gegenseitig."),
        SEC("patch.object"),
        P("Mit unittest.mock.patch.object wird database.DB_PATH auf den temporären Pfad umgeleitet. Der getestete Code läuft unverändert, schreibt aber in die Temp-DB statt in die echte games.db."),
        SEC("pytest-Kompatibilität"),
        P("Die Tests sind als unittest.TestCase geschrieben, können aber direkt mit pytest ausgeführt werden – pytest erkennt unittest-Tests automatisch."),
        TIP("Falls jemand fragt: Mocking verhindert dass Tests die Produkt-DB verändern oder voneinander abhängen."),
    ],
))

# ── Folie 16 ──────────────────────────────────────────────────────────────────
slides.append((
    stich_header(16, "Zusammenfassung") + [
        B("✅ Zwei vollständige Strategiespiele auf 6×6-Feld"),
        B("🤖 Wiederverwendbarer MiniMax + Alpha-Beta-Pruning"),
        B("🔒 Sichere Authentifizierung: SHA-256 + Salt"),
        B("📦 SQLite: keine externen Abhängigkeiten"),
        B("🖥️ tkinter-GUI: Windows / macOS / Linux"),
        B("🧪 15 Unittests sichern Kernfunktionen ab"),
    ],
    detail_header(16, "Zusammenfassung", "Was haben wir erreicht?") + [
        P("Zusammenfassend haben wir alle wesentlichen Projektziele erreicht:"),
        B("✅ <b>Zwei vollständige Strategiespiele</b> auf einem 6×6-Spielfeld – vollständig spielbar gegen eine KI."),
        B("🤖 <b>Wiederverwendbarer MiniMax-Algorithmus</b> mit Alpha-Beta-Pruning – eine Engine für alle Spiele."),
        B("🔒 <b>Sichere Authentifizierung</b> mit SHA-256-Hashing und zufälligem Salt – keine Klartextpasswörter."),
        B("📦 <b>SQLite-Datenbank</b> ohne externe Abhängigkeiten – die DB wird automatisch erstellt."),
        B("🖥️ <b>tkinter-GUI</b> mit eigenem Design-System – läuft auf Windows, macOS und Linux."),
        B("🧪 <b>15 Unittests</b> sichern die Kernfunktionen ab und können jederzeit ausgeführt werden."),
        TIP("Ruhig sprechen – das ist die Zusammenfassung, kein neues Material."),
    ],
))

# ── Folie 17 ──────────────────────────────────────────────────────────────────
slides.append((
    stich_header(17, "SOLL/IST Feature-Vergleich", "Lastenheft → Pflichtenheft → Umsetzung → Test") + [
        SEC("MUSS-Ziele: 12/12 ✅"),
        B("2 Spiele · 6×6 Brett · 5 Schwierigkeitsgrade"),
        B("Login · Registrierung · Gastmodus · Spielabbruch · Regelanzeige"),
        B("Bestenliste · SHA-256-Hashing · MiniMax-KI · Unittests"),
        SEC("SOLL-Ziele: 2/2 ✅"),
        B("Alpha-Beta-Pruning · SQL-Bestenliste"),
        SEC("KANN-Ziele: 2/4 ⚠"),
        B("✅ Sprachwechsel EN/DE · Sprachpräferenz in DB"),
        B("❌ Dame (drittes Spiel) · Alt-KI-Schnittstelle (zeitbedingt)"),
    ],
    detail_header(17, "SOLL/IST Feature-Vergleich", "Lastenheft → Pflichtenheft → Umsetzung → Test") + [
        SEC("MUSS-Ziele: 12 von 12 ✅"),
        P("Alle Pflichtanforderungen wurden vollständig umgesetzt: beide Spiele, 5 Schwierigkeitsgrade, Login, Registrierung, Gastmodus, Spielabbruch mit Dialog, Regelanzeige, Bestenliste, SHA-256-Hashing, MiniMax-KI und Unittests."),
        SEC("SOLL-Ziele: 2 von 2 ✅"),
        P("Beide Soll-Anforderungen wurden erfüllt: Alpha-Beta-Pruning als MiniMax-Optimierung und die Bestenliste über SQL-Abfragen aus der Datenbank."),
        SEC("KANN-Ziele: 2 von 4 ⚠"),
        B("✅ <b>Sprachwechsel EN/DE</b> und Sprachpräferenz in der Datenbank sind implementiert."),
        B("❌ <b>Dame als drittes Spiel</b> und eine alternative KI-Schnittstelle wurden aus Zeitgründen nicht umgesetzt."),
        P("Insgesamt: Alle MUSS- und SOLL-Anforderungen sind erfüllt. Die nicht umgesetzten KANN-Ziele waren von Anfang an als optional eingestuft."),
        TIP("Nicht entschuldigen für die KANN-Ziele – sie waren optional und das ist legitim."),
    ],
))

# ── Folie 18 ──────────────────────────────────────────────────────────────────
slides.append((
    stich_header(18, "SOLL/IST Projektplanung", "Wasserfallmodell · 2 Meetings · Discord & WhatsApp") + [
        B("Analysephase (Woche 1: 20.04.–24.04.) ✅ plangemäß"),
        B("Implementierung (27.04.–04.05.) ⚠ +1 Tag (01.05. Feiertag)"),
        B("Test & Doku: parallel zur Impl. statt sequenziell ⚠"),
        B("Abschluss (Woche 3) ✅ plangemäß"),
        B("Discord-Channel statt Kanban-Board"),
        B("2 Team-Meetings: 27.04. & 29.04. je 10:00 Uhr"),
    ],
    detail_header(18, "SOLL/IST Projektplanung", "Wasserfallmodell · 2 Meetings · Discord") + [
        P("Das Projekt wurde nach dem Wasserfallmodell geplant und in drei Phasen durchgeführt:"),
        B("<b>Analysephase (Woche 1: 20.04.–24.04.)</b> ✅ plangemäß: Pflichtenheft, Work Breakdown Structure und Zeitplan wurden erstellt."),
        B("<b>Implementierung (27.04.–04.05.)</b> ⚠ +1 Tag: Durch den Feiertag am 01. Mai wurde der 04. Mai als zusätzlicher Arbeitstag genutzt."),
        B("<b>Test & Dokumentation</b> ⚠ parallel: Entgegen der ursprünglichen Planung liefen Test und Dokumentation parallel zur Implementierung – das war pragmatischer."),
        B("<b>Abschluss (Woche 3)</b> ✅ plangemäß: Abschlusspräsentation wie geplant."),
        SEC("Abweichungen"),
        P("Statt eines Kanban-Boards wurde ein Discord-Channel als leichtgewichtige Alternative genutzt. Die zwei geplanten Team-Meetings fanden am 27.04. und 29.04. jeweils um 10:00 Uhr statt."),
        TIP("Abweichungen positiv formulieren: 'wir haben uns angepasst' statt 'wir haben den Plan nicht eingehalten'."),
    ],
))

# ── Folie 19 ──────────────────────────────────────────────────────────────────
slides.append((
    stich_header(19, "Benutzeroberfläche (GUI)", "tkinter · HHBKTendo Design System · Dark Theme") + [
        SEC("Screen-Flow"),
        B("① Login → Login / Register / Als Gast spielen"),
        B("② Hauptmenü → Spiel · Schwierigkeit · Play · Bestenliste"),
        B("③ Spielscreen → 6×6 Brett · Züge per Klick"),
        SEC("Design-System (Farben)"),
        SB("#0D0D1A Deep Navy (BG)  ·  #E94560 Hot Pink (Primär)"),
        SB("#6C3FC5 Royal Purple  ·  #00D4FF Cyber Cyan (Akzent)"),
        SEC("tkinter-Besonderheiten"),
        B("Buttons als tk.Label + Bindings (macOS-Bug: bg/fg)"),
        B("KI in separatem Thread · after(0, cb) für GUI-Rückkehr"),
    ],
    detail_header(19, "Benutzeroberfläche (GUI)", "tkinter · HHBKTendo Design System · Dark Theme") + [
        SEC("Screen-Flow"),
        B("① <b>Login-Screen:</b> Nutzer können sich einloggen, registrieren oder als Gast spielen."),
        B("② <b>Hauptmenü:</b> Spiel auswählen, Schwierigkeitsgrad einstellen, starten oder Bestenliste öffnen."),
        B("③ <b>Spielscreen:</b> 6×6-Spielfeld, Züge per Mausklick, KI-Zug wird nach kurzer Denkzeit angezeigt."),
        SEC("Design-System"),
        B("Deep Navy (#0D0D1A) als Hintergrund · Hot Pink (#E94560) für Primärelemente"),
        B("Royal Purple (#6C3FC5) als Sekundärfarbe · Cyber Cyan (#00D4FF) für Hover und Akzente"),
        SEC("Technische Besonderheiten"),
        B("Buttons sind tk.Label mit Bindings implementiert – weil tk.Button auf macOS bg/fg-Farben ignoriert."),
        B("KI-Zug läuft in separatem Thread, GUI bleibt reaktionsfähig. after(0, callback) bringt das Ergebnis sicher in den Hauptthread zurück."),
        TIP("Falls Demo: kurz das Dark Theme und die Farbgebung erwähnen."),
    ],
))

# ── Folie 20 ──────────────────────────────────────────────────────────────────
slides.append((
    stich_header(20, "Quellen & Werkzeuge") + [
        SEC("Entwicklungsumgebungen"),
        B("PyCharm (JetBrains)  ·  Visual Studio Code (Microsoft)"),
        SEC("KI-Assistenten"),
        B("Claude (Anthropic)  ·  ChatGPT (OpenAI)"),
        SEC("Python-Bibliotheken (alle stdlib außer Pillow)"),
        B("tkinter · sqlite3 · hashlib · threading · Pillow (GIF)"),
        SEC("Quellen"),
        B("Wikipedia: MiniMax · Alpha-Beta-Pruning"),
        B("HHBK Lernfeld 5 – Unterrichtsmaterial"),
        B("docs.python.org – Python-Dokumentation"),
    ],
    detail_header(20, "Quellen & Werkzeuge") + [
        SEC("Entwicklungsumgebungen"),
        B("PyCharm (JetBrains) und Visual Studio Code (Microsoft)"),
        SEC("KI-Assistenten"),
        B("Claude (Anthropic) und ChatGPT (OpenAI) wurden zur Unterstützung bei der Entwicklung genutzt."),
        SEC("Python-Bibliotheken"),
        B("Alle Bibliotheken außer Pillow sind Teil der Python-Standardbibliothek: tkinter, sqlite3, hashlib, threading, unittest, tempfile."),
        B("Pillow wurde für GIF-Animationen in der GUI verwendet."),
        SEC("Quellen"),
        B("Wikipedia: Artikel zu MiniMax-Algorithmus und Alpha-Beta-Pruning"),
        B("HHBK Lernfeld 5 – Unterrichtsmaterial"),
        B("docs.python.org – offizielle Python-Dokumentation"),
        SEC("Projektkoordination"),
        B("Zwei Team-Meetings (27.04. & 29.04., 10:00 Uhr), tägliche Kommunikation über Discord und WhatsApp."),
    ],
))

# ── Folie 21 ──────────────────────────────────────────────────────────────────
slides.append((
    stich_header(21, "Fazit – Projektverlauf") + [
        SEC("Team & Rollen"),
        B("Lucas – Projektleitung, auth.py, Testing"),
        B("Jesse – database.py, Pitch, Testing"),
        B("Arda – database.py, Testing"),
        B("Uilliam – GUI (main.py), Design"),
        B("Jakub – pawn_chess.py  ·  Niklas – minimax.py"),
        SEC("Highlights"),
        B("Spielunabhängige MiniMax-Schnittstelle"),
        B("Reibungslose Teamarbeit dank klarem Pflichtenheft"),
        SEC("Lessons Learnt"),
        B("Kanban-Board früher einsetzen"),
        B("Schnittstellen detaillierter im Pflichtenheft definieren"),
        SEC("Ausblick"),
        B("Dame als drittes Spiel · Sprach-Auswahl ausbauen"),
    ],
    detail_header(21, "Fazit – Projektverlauf", "Team · Highlights · Lessons Learnt") + [
        SEC("Team & Rollenverteilung"),
        B("Lucas – Projektleitung, auth.py, Testing"),
        B("Jesse – database.py, Pitch, Testing   ·   Arda – database.py, Testing"),
        B("Uilliam – GUI (main.py), Design   ·   Jakub – pawn_chess.py"),
        B("Niklas – minimax.py   ·   Jamie – tictactoe.py"),
        SEC("Highlights"),
        B("Die spielunabhängige MiniMax-Schnittstelle war die eleganteste technische Lösung – ein KI-Code für alle Spiele."),
        B("Die Teamarbeit verlief reibungslos dank eines klaren Pflichtenhefts und gegenseitiger Unterstützung."),
        SEC("Lessons Learnt"),
        B("Ein Kanban-Board früher einsetzen hätte die Aufgabenverteilung transparenter gemacht."),
        B("Schnittstellen zwischen Modulen detaillierter im Pflichtenheft definieren."),
        SEC("Ausblick"),
        B("Dame als drittes Spiel wäre mit dem bestehenden Callback-System einfach umsetzbar."),
        B("Sprach-Auswahl im Menü und weiterer Ausbau des Design-Systems."),
        TIP("Zum Abschluss: ruhig und selbstbewusst schließen. Das Projekt ist vollständig."),
    ],
))

# ── Assemble story: for each slide → stichkarte → PageBreak → volltext → PageBreak
story = []
for stich, detail in slides:
    story += stich
    story.append(PageBreak())
    story += detail
    story.append(PageBreak())

# Remove the trailing PageBreak after the last slide
if story and isinstance(story[-1], PageBreak):
    story.pop()

# ── Build ──────────────────────────────────────────────────────────────────────
doc = DarkDoc(
    OUTPUT,
    pagesize=A5,
    leftMargin=12*mm,
    rightMargin=12*mm,
    topMargin=10*mm,
    bottomMargin=10*mm,
)
doc.build(story)
print(f"PDF erstellt: {OUTPUT}  ({len(slides)*2} Seiten)")
