# Pflichtenheft – HHBKTendo Spielesammlung

**Projekt:** Strategiespiele-Prototyp mit MiniMax-KI
**Auftraggeber:** HHBK Tendo Research Center
**Auftragnehmer:** Projektteam (Lernfeld 5)
**Version:** 1.2
**Datum:** 2026-04-21
**Status:** Entwurf

---

## Inhaltsverzeichnis

1. [Zielbestimmung](#1-zielbestimmung)
2. [Produkteinsatz](#2-produkteinsatz)
3. [Systemübersicht und Architektur](#3-systemübersicht-und-architektur)
4. [Funktionale Anforderungen (MUSS)](#4-funktionale-anforderungen-muss)
5. [Funktionale Anforderungen (SOLL / KANN)](#5-funktionale-anforderungen-soll--kann)
6. [Nicht-funktionale Anforderungen](#6-nicht-funktionale-anforderungen)
7. [Datenmodell](#7-datenmodell)
8. [Benutzerschnittstelle](#8-benutzerschnittstelle)
9. [Globale Variablen und Zustandsmodell](#9-globale-variablen-und-zustandsmodell)
10. [MiniMax-Algorithmus und Bewertungsfunktionen](#10-minimax-algorithmus-und-bewertungsfunktionen)
11. [Testfälle und Abnahmekriterien](#11-testfälle-und-abnahmekriterien)
12. [Liefergegenstände](#12-liefergegenstände)
13. [Projektplanung](#13-projektplanung)

---

## 1 Zielbestimmung

### 1.1 Mussziele

| ID | Herkunft (LH) | Beschreibung |
|----|---------------|--------------|
| PF-M01 | LF4000 | Mindestens zwei Strategiespiele sind vollständig spielbar. |
| PF-M02 | LF4010 | Alle Spiele sind in einer einzigen Python-Anwendung mit grafischer Benutzeroberfläche (tkinter) integriert. |
| PF-M03 | LF4020 | Jedes Spiel verwendet ein 6×6-Spielfeld. |
| PF-M04 | LF4030 | Die KI nutzt den MiniMax-Algorithmus für alle Spiele. |
| PF-M05 | LF4040 | Der menschliche Spieler macht immer den ersten Zug; die KI antwortet als zweiter Spieler. |
| PF-M06 | LF4050 | Für jedes Spiel ist die Spielstärke (Suchtiefe 1–5) vor Spielbeginn einstellbar. |
| PF-M07 | LF4060 | Ein laufendes Spiel kann jederzeit abgebrochen werden (mit Bestätigungsdialog). |
| PF-M08 | LF4070 | Benutzer können sich registrieren und anmelden. |
| PF-M09 | LF4080 | Siege und Niederlagen werden je Spiel und Schwierigkeitsgrad in der Datenbank gespeichert. |
| PF-M10 | LF4090 | Im Gastmodus werden keine Ergebnisse gespeichert. |
| PF-M11 | LF4100 | Die Bestenliste ist pro Spiel und Schwierigkeitsgrad separat abrufbar. |
| PF-M12 | LF4110 | Die Spielregeln jedes Spiels sind während des Spiels per Schaltfläche einsehbar. |

### 1.2 Sollziele

| ID | Herkunft (LH) | Beschreibung |
|----|---------------|--------------|
| PF-S01 | LF4120 | Alpha-Beta-Pruning optimiert den MiniMax-Algorithmus. |
| PF-S02 | LD4220 | Die Bestenliste wird durch SQL-Abfragen aus der Datenbank generiert. |

### 1.3 Kannziele

| ID | Herkunft (LH) | Beschreibung |
|----|---------------|--------------|
| PF-K01 | LF4130 | Der Benutzer kann die Sprache zwischen Englisch (Standard) und Deutsch umschalten. |
| PF-K02 | LD4230 | Spracheinstellung wird benutzerspezifisch in der Datenbank gespeichert. |

### 1.4 Abgrenzung (Wont-have)

- Kein Netzwerkbetrieb / Multiplayer (LF4140)
- Kein drittes KI-System als alternative Schnittstelle (LF4120 Could have – nicht priorisiert)

---

## 2 Produkteinsatz

### 2.1 Anwendungsbereich

Freizeitanwendung zum Spielen von Strategiespielen gegen eine KI. Primärzweck: Markttest des MiniMax-Algorithmus und der Spielmechaniken.

### 2.2 Zielgruppe

Testpersonen im Alter 12–99, die Strategiespiele bevorzugen, aus den Märkten: Deutschland, UK, Singapur, USA, Hongkong.

### 2.3 Produktumgebung

| Eigenschaft | Wert |
|-------------|------|
| Betriebssystem | Windows 10 / 11, macOS |
| Programmiersprache | Python 3.10+ |
| GUI-Framework | tkinter (stdlib) |
| Datenbank | SQLite (unabhängig, dateibasiert) |
| Programmierparadigma | Prozedural, funktionsorientiert (keine Klassen für Spiellogik) |

---

## 3 Systemübersicht und Architektur

### 3.1 Modulübersicht

```
HHBKTendo Spielesammlung
│
├── main.py          GUI-Steuerung (Login, Menü, Spielscreen, Bestenliste)
├── auth.py          Authentifizierung (Registrierung, Login, Session)
├── database.py      Datenbankoperationen (SQLite, CRUD)
├── minimax.py       Generischer MiniMax + Alpha-Beta-Pruning (spielunabhängig)
├── pawn_chess.py    Spiellogik Bauernschach (Brett, Züge, Bewertung)
├── tictactoe.py     Spiellogik Tic-Tac-Toe 4-gewinnt (6×6, 4 in einer Reihe, Brett, Züge, Bewertung)
├── test_all.py      Tests, welche die Methoden nach Richtigkeit prüfen (erwartetes Resultat wird geprüft)        
└── games.db         SQLite-Datenbankdatei (auto-generiert beim Start)
```

### 3.2 Schnittstellen zwischen Modulen

Der MiniMax-Algorithmus ist vollständig spielunabhängig. Er erhält spielspezifische Callback-Funktionen:

```
minimax.get_best_move(
    board,           ← aktuelles Spielfeld (2D-Liste)
    depth,           ← Suchtiefe (= Schwierigkeit)
    get_moves_fn,    ← fn(board, is_maximizing) → [Züge]
    apply_move_fn,   ← fn(board, move, is_maximizing) → neues Board
    evaluate_fn,     ← fn(board) → int (positiv = gut für KI)
    is_terminal_fn   ← fn(board) → (bool, int)
)
```

Jedes Spielmodul implementiert exakt diese vier Funktionen. Damit ist **dieselbe KI-Engine** für alle Spiele wiederverwendbar (LN5040).

### 3.3 Datenfluss

```
Benutzerinteraktion (Klick)
    → on_board_click()
    → handle_*_click()
    → Spiellogikmodul (apply_move)
    → draw_board()
    → start_ai_turn() [Thread]
        → minimax.get_best_move()
            → Spiellogikmodul (get_valid_moves, apply_move, evaluate, is_terminal)
        → after_ai_turn() [Hauptthread via .after(0, ...)]
    → end_game() → database.save_result()
```

---

## 4 Funktionale Anforderungen (MUSS)

### 4.1 Spiel: Bauernschach (PF-M01)

**Brettkonfiguration:**
- 6×6 Felder, weiße Bauern (Mensch) in Reihe 5, schwarze Bauern (KI) in Reihe 0
- Repräsentation: `board[row][col]` ∈ {WHITE=1, BLACK=−1, EMPTY=0}

**Erlaubte Züge:**

| Zugart | Bedingung |
|--------|-----------|
| Vorwärtszug | Zielfeld ist leer (direkt vor dem Bauern in Richtung gegnerische Grundlinie) |
| Diagonales Schlagen | Zielfeld enthält gegnerischen Bauern (diagonal vorwärts) |

**Gewinnbedingungen:**

| Zustand | Ergebnis |
|---------|---------|
| Weißer Bauer erreicht Reihe 0 | Mensch gewinnt |
| Schwarzer Bauer erreicht Reihe 5 | KI gewinnt |
| Weiß hat keine Figuren mehr | KI gewinnt |
| Schwarz hat keine Figuren mehr | Mensch gewinnt |
| Aktueller Spieler hat keine gültigen Züge | Gegner gewinnt |

Unentschieden ist nicht möglich.

**Bewertungsfunktion:**
```
score = Σ (Figurwert + Fortschritt × 2 + Zentrumbonus) für KI-Figuren
      − Σ (Figurwert + Fortschritt × 2 + Zentrumbonus) für Menschen-Figuren
```
- Figurwert: 10 Punkte pro Figur
- Fortschritt: Anzahl der Reihen, die eine Figur vorgerückt ist
- Zentrumbonus: +1 für Spalten 1–4

---

### 4.2 Spiel: Tic-Tac-Toe (4 gewinnt) (PF-M01)

**Brettkonfiguration:**
- 6×6 Felder, leer zu Spielbeginn
- Repräsentation: `board[row][col]` ∈ {HUMAN=1, AI=−1, EMPTY=0}

**Spielregeln:**
- Spieler setzen abwechselnd einen Stein auf ein leeres Feld
- Mensch beginnt (X), KI antwortet (O)

**Gewinnbedingungen:**

| Zustand | Ergebnis |
|---------|---------|
| 4 in einer Reihe (horizontal) | Erster Spieler gewinnt |
| 4 in einer Spalte (vertikal) | Erster Spieler gewinnt |
| 4 diagonal | Erster Spieler gewinnt |
| Brett voll (36 Felder), kein Gewinner | Unentschieden |

**Bewertungsfunktion:**
```
score = (3er-Linien KI) × 50 − (3er-Linien Mensch) × 50
      + (2er-Linien KI) × 10 − (2er-Linien Mensch) × 10
      + Zentrumsnähe-Bonus
```
Nur offene Linien (ohne gegnerische Steine im Fenster) werden gezählt.

---

### 4.3 KI-System (PF-M04)

**MiniMax mit Alpha-Beta-Pruning:**

```
minimax(board, depth, is_maximizing, α=−∞, β=+∞):
    if terminal(board): return terminal_score
    if depth == 0:      return evaluate(board)

    if is_maximizing:
        best = −∞
        for move in get_moves(board, True):
            score = minimax(apply(board, move), depth−1, False, α, β)
            best = max(best, score); α = max(α, score)
            if β ≤ α: break  # Beta-Pruning
        return best
    else:
        best = +∞
        for move in get_moves(board, False):
            score = minimax(apply(board, move), depth−1, True, α, β)
            best = min(best, score); β = min(β, score)
            if β ≤ α: break  # Alpha-Pruning
        return best
```

**Schwierigkeitsgrade:**

| Level | Suchtiefe | Verhalten |
|-------|-----------|-----------|
| 1 – Leicht | 1 | Nur einen Zug voraus, kaum strategisch |
| 2 – Mittel | 2 | Einfache Taktiken erkannt |
| 3 – Schwer | 3 | Mittlere Planung (Standard) |
| 4 – Experte | 4 | Starke KI, schwer zu schlagen |
| 5 – Meister | 5 | Sehr starke KI, KI-Zug kann mehrere Sekunden dauern |

**Zeitlimit:** KI-Zug läuft in eigenem Thread (max. 45 Sekunden, LN5010).

---

### 4.4 Benutzerverwaltung (PF-M08–M10)

| Funktion | Beschreibung |
|----------|-------------|
| Registrierung | Benutzername (min. 3 Zeichen), Passwort (min. 4 Zeichen), Eindeutigkeit geprüft |
| Login | Benutzername + Passwort, Verifikation gegen gespeicherten Hash |
| Gastmodus | Spiel ohne Registrierung, keine Speicherung |
| Passwort-Hashing | SHA-256 + 16-Byte Zufalls-Salt, Format: `salt:hash` |

---

### 4.5 Bestenliste (PF-M09, M11)

- Speicherung: User-ID, Spielname, Schwierigkeitsgrad, gewonnen (0/1)
- Abfrage: gruppiert nach Benutzer, sortiert nach Siegen absteigend
- Anzeige: Rang, Benutzername, Siege, Niederlagen, Gesamt-Spiele
- Unentschieden (nur Tic-Tac-Toe) werden nicht gespeichert

---

## 5 Funktionale Anforderungen (SOLL / KANN)

### 5.1 Sprachumschaltung (PF-K01)

- Umschaltung zwischen EN (Standard) und DE jederzeit möglich
- Alle UI-Texte, Regeln und Statusmeldungen werden in der gewählten Sprache angezeigt
- Spracheinstellung wird bei eingeloggten Benutzern in der DB persistiert

---

## 6 Nicht-funktionale Anforderungen

| ID | Anforderung | Maßnahme |
|----|-------------|----------|
| NF-01 (LN5000) | Python + geeignetes GUI-Framework | Python 3.10+, tkinter |
| NF-02 (LN5001) | Prozedurale Programmierung | Keine Klassen für Spiellogik; Module mit Funktionen |
| NF-03 (LN5010) | KI-Zug max. 45 Sekunden | KI in separatem Thread |
| NF-04 (LN5020) | Persistente Benutzerdaten | SQLite-Datenbankdatei |
| NF-05 (LN5030) | Passwörter nicht im Klartext | SHA-256 + Salt (auth.py) |
| NF-06 (LN5040) | Wiederverwendbare Software | Generischer MiniMax, spielunabhängige Schnittstelle |
| NF-07 (LN5050) | Intuitive Bedienung | Einheitliches Design, klare Labels, Statusanzeige |
| NF-08 (LN5060) | Brand Identity | Dunkles Farbschema (HHBKTendo CI), konsistentes Layout |
| NF-09 | Plattformkompatibilität | Buttons als `tk.Label` mit Bindings implementiert, da macOS den `bg`/`fg`-Parameter von `tk.Button` ignoriert |

---

## 7 Datenmodell

### 7.1 Tabelle: `users`

| Spalte | Typ | Beschreibung |
|--------|-----|-------------|
| id | INTEGER PK AUTO | Primärschlüssel |
| username | TEXT UNIQUE NOT NULL | Eindeutiger Benutzername |
| password_hash | TEXT NOT NULL | SHA-256-Hash mit Salt (Format: `salt:hash`) |
| language | TEXT DEFAULT 'en' | Sprachpräferenz |
| created_at | TIMESTAMP | Registrierungszeitpunkt |

### 7.2 Tabelle: `results`

| Spalte | Typ | Beschreibung |
|--------|-----|-------------|
| id | INTEGER PK AUTO | Primärschlüssel |
| user_id | INTEGER FK | Verweis auf `users.id` |
| game | TEXT | `'pawn_chess'` oder `'tictactoe'` |
| difficulty | INTEGER | Suchtiefe 1–5 |
| won | INTEGER | 1 = Sieg, 0 = Niederlage |
| played_at | TIMESTAMP | Zeitpunkt des Spielendes |

### 7.3 Bestenlisten-Abfrage (SQL)

```sql
SELECT u.username,
       SUM(r.won)       AS wins,
       SUM(1 - r.won)   AS losses,
       COUNT(*)         AS total_games
FROM results r
JOIN users u ON r.user_id = u.id
WHERE r.game = ? AND r.difficulty = ?
GROUP BY r.user_id
ORDER BY wins DESC, losses ASC
LIMIT 10;
```

---

## 8 Benutzerschnittstelle

### 8.1 Bildschirmfluss

```
Startbildschirm (Login/Register)
    ├── [Login]       → Hauptmenü
    ├── [Register]    → Hauptmenü
    └── [Als Gast]    → Hauptmenü
         │
         ├── [Bauernschach spielen] → Spielscreen
         │       ├── [Regeln]      → Regelpopup
         │       ├── [Abbrechen]   → Hauptmenü (mit Bestätigung)
         │       └── [Spielende]   → Ergebnis anzeigen → Hauptmenü
         │
         ├── [Tic-Tac-Toe spielen] → Spielscreen (analog)
         │
         ├── [Bestenliste]         → Bestenlisten-Popup
         └── [Abmelden]            → Startbildschirm
```

### 8.2 Spielfeld-Design

**Bauernschach:**
- Helles Feld: `#eecc99`, Dunkles Feld: `#8b5e3c`
- Weiße Figur: weißer Kreis (`#ffffff`) mit ♙-Symbol, schwarzer Kontur
- Schwarze Figur: dunkler Kreis (`#1a1a2e`) mit ♟-Symbol, helle Kontur
- Ausgewählte Figur: rotes Feld, gültige Züge: grünes Feld

**Tic-Tac-Toe (6×6):**
- X (Mensch): hellblau (`#64b5f6`), dicke Linien
- O (KI): rot (`#ef5350`), dicke Ovallinie

### 8.3 Farbschema (CI)

| Element | Farbe | Hex |
|---------|-------|-----|
| Hintergrund dunkel | Nacht-Marine | `#1a1a2e` |
| Hintergrund Karten | Dunkel-Blau | `#0f3460` |
| Akzent (Buttons, Titel) | HHBKTendo-Rot | `#e94560` |
| Akzent2 (Sekundär) | Lila | `#533483` |
| Text (Standard) | Hellgrau | `#eaeaea` |

---

## 9 Globale Variablen und Zustandsmodell

Das gesamte Laufzeit-Zustand der Anwendung ist im Dictionary `app_state` in `main.py` konzentriert (LN5001):

| Variable | Typ | Bedeutung |
|----------|-----|-----------|
| `app_state["language"]` | str | Aktuelle Sprache ('en'/'de') |
| `app_state["current_screen"]` | tk.Frame | Aktuell angezeigter Screen |
| `app_state["game"]` | str | Aktives Spiel ('pawn_chess'/'tictactoe') |
| `app_state["board"]` | list[list[int]] | Aktuelles 6×6-Spielfeld |
| `app_state["difficulty"]` | int | Suchtiefe 1–5 |
| `app_state["human_turn"]` | bool | True = Mensch am Zug |
| `app_state["selected"]` | tuple\|None | Ausgewählte Figur (Bauernschach) |
| `app_state["valid_moves"]` | list | Gültige Züge der ausgewählten Figur |
| `app_state["game_over"]` | bool | True nach Spielende |
| `app_state["ai_thinking"]` | bool | True während KI-Berechnung |

In `auth.py`:

| Variable | Typ | Bedeutung |
|----------|-----|-----------|
| `current_user` | dict\|None | Aktuell eingeloggter Benutzer (None = Gast) |

---

## 10 MiniMax-Algorithmus und Bewertungsfunktionen

### 10.1 Illustrationsdiagramm

```
        maximize (KI)
         /          \
    +3              -2
   minimize       minimize
   /    \         /    \
 +3     +5     -2     -9
```
KI wählt den Zug, der zum Wert +3 führt (Minimizer wählt den schlechtesten für KI = +3 statt +5).

### 10.2 Alpha-Beta-Pruning

Äste des Spielbaums werden abgeschnitten, wenn feststeht, dass der Gegner diesen Pfad nie wählen wird:

- **Alpha (α)**: Bisher bestes Ergebnis für den Maximizer → wird nach oben weitergegeben
- **Beta (β)**: Bisher bestes Ergebnis für den Minimizer → wird nach unten weitergegeben
- Abbruch wenn `β ≤ α`

Einsparung: Im besten Fall O(b^(d/2)) statt O(b^d) Knoten (b = Verzweigungsgrad, d = Tiefe).

### 10.3 Terminale Bewertungen

| Zustand | Score |
|---------|-------|
| KI gewinnt | +1.000.000 |
| Mensch gewinnt | −1.000.000 |
| Unentschieden | 0 |
| Tiefenlimit (Blatt) | evaluate(board) |

---

## 11 Testfälle und Abnahmekriterien

### 11.1 Funktionstests

| TC-ID | Testfall | Erwartetes Ergebnis |
|-------|----------|---------------------|
| TC-01 | Registrierung mit gültigem Namen/Passwort | Benutzer angelegt, Login möglich |
| TC-02 | Registrierung mit bereits vergebenem Namen | Fehlermeldung "Username already taken" |
| TC-03 | Login mit falschem Passwort | Fehlermeldung "Incorrect password" |
| TC-04 | Gastmodus – Spiel beenden | Kein Eintrag in Datenbank |
| TC-05 | Bauernschach – Zug vorwärts auf leeres Feld | Bauer bewegt sich |
| TC-06 | Bauernschach – Zug auf eigene Figur | Zug wird verweigert |
| TC-07 | Bauernschach – Diagonales Schlagen | Gegnerischer Bauer wird entfernt |
| TC-08 | Bauernschach – Bauer erreicht Grundlinie | Spiel endet mit korrektem Gewinner |
| TC-09 | TTT – 4 in einer Reihe (horizontal) | Spiel endet, Gewinner korrekt |
| TC-10 | TTT – 4 in einer Diagonale | Spiel endet, Gewinner korrekt |
| TC-11 | TTT – Alle 36 Felder belegt ohne Gewinner | Unentschieden angezeigt |
| TC-12 | KI-Zug bei Suchtiefe 5 | KI zieht innerhalb 45 Sekunden |
| TC-13 | Spielabbruch | Bestätigungsdialog, Rückkehr ins Hauptmenü |
| TC-14 | Bestenliste anzeigen | Korrekte Sortierung nach Siegen |
| TC-15 | Sprachwechsel EN → DE | Alle UI-Texte auf Deutsch |

### 11.2 Abnahmekriterien (aus Lastenheft)

- Alle MUSS-Anforderungen (PF-M01 bis PF-M12) sind implementiert und testbar
- Live-Demo zeigt mind. 2 vollständige Spiele gegen KI
- Bestenliste zeigt korrekte Ergebnisse eingeloggter Benutzer
- Passwörter sind nicht im Klartext in der DB gespeichert (prüfbar per DB-Viewer)
- Anwendung startet auf Zielumgebung (Windows 10/11) mit `python main.py`

---

## 12 Liefergegenstände

| # | Liefergegenstand | Verantwortlich |
|---|-----------------|----------------|
| 1 | Pflichtenheft (dieses Dokument) | Team |
| 2 | Quellcode (alle .py-Dateien + games.db) | Entwickler |
| 3 | Benutzerdokumentation (Installation, Start, Spielanleitung) | Dokumentation |
| 4 | Technische Dokumentation (Architektur, Algorithmen, Variablen) | Entwickler |
| 5 | Testprotokoll (TC-01 bis TC-15) | Test |
| 6 | Abschlusspräsentation (SOLL/IST, Softwarekomponenten, Fazit) | Team |
| 7 | Konzept Corporate Identity & Branding | Design |
| 8 | Pitch-Deck (englischsprachig, für Investoren) | Team |
| 9 | Konzept Arbeitszeitgestaltung (Plan vs. IST) | Projektleitung |

---

## 13 Projektplanung

### 13.1 Projektphasen (Wasserfallmodell)

| Phase | Inhalt | Zeitraum              |
|-------|--------|-----------------------|
| Analysephase | Lastenheft lesen, Pflichtenheft erstellen, WBS, Zeitplan, Ressourcenplan | Woche 1 (Vollzeit)    |
| Design & Implementierung | Architektur, Datenbankdesign, Spiellogik, MiniMax, GUI | Woche 2 (Vollzeit)    |
| Test | Testprotokoll, Bugfixes, Abnahmetests | Woche 2 (Mitte + Ende) |
| Dokumentation | Benutzerdokumentation, Technische Doku, Präsentation, Pitch, CI-Konzept | Woche 2 (Ende)        |
| Abschluss | Live-Demo, Präsentation, Fachgespräch (ca. 20+10 min) | Woche 3 (letzter Tag) |

### 13.2 Offene Punkte

| # | Offener Punkt | Status |
|---|---------------|--------|
| 1 | Dame (Checkers) als drittes Spiel implementieren | Optional / Zeit abhängig |
| 2 | Testprotokoll-Dokument erstellen und ausfüllen | Ausstehend |
| 3 | Benutzerdokumentation schreiben | Ausstehend |
| 4 | CI/Branding-Konzept | Ausstehend |
| 5 | Englischsprachiger Pitch | Ausstehend |

---

---

## Änderungshistorie

| Version | Datum | Änderung |
|---------|-------|----------|
| 1.0 | 2026-04-20 | Erstversion |
| 1.1 | 2026-04-21 | Tic-Tac-Toe zwischenzeitlich auf 3×3 geändert; NF-09 (macOS-Kompatibilität) ergänzt |
| 1.2 | 2026-04-21 | Tic-Tac-Toe gemäß Lastenheft (LF4020) auf 6×6 / 4 in einer Reihe zurückgesetzt; PF-M03, Abschnitt 4.2, Bewertungsfunktion, TC-09–TC-11 wiederhergestellt |

*Pflichtenheft erstellt auf Basis des Lastenhefts Strategiespiele V13a, HHBK Tendo Research Center, 2026.*
