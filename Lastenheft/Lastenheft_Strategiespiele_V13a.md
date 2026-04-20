Lastenheft Strategiespiele

HHBKTendo

![Lastenheft_Strategiespiele_V13a](<Projekt%202026/Lastenheft/Attachments/Lastenheft_Strategiespiele_V13a.png>)

**MinIMax**

![Lastenheft_Strategiespiele_V13a](<Projekt%202026/Lastenheft/Attachments/Lastenheft_Strategiespiele_V13a%201.png>)

© 2026 | HHBK | Düsseldorf

Lastenheft Strategiespiele

[Lastenheft Strategiespiele 2](#_Toc194753956)

[1 Ausgangssituation 3](#_Toc194753957)

[2 Zielsetzung 3](#_Toc194753958)

[2.1 Spielbeschreibungen 4](#_Toc194753959)

[2.1.1 Bauernschach 4](#_Toc194753960)

[2.1.2 Dame 4](#_Toc194753961)

[2.1.3 Tic-Tac-Toe 5](#_Toc194753962)

[2.1.4 MiniMax Algorithmus 5](#_Toc194753963)

[3 Produkteinsatz 5](#_Toc194753964)

[3.1 Anwendungsbereiche 5](#_Toc194753965)

[3.2 Zielgruppen 5](#_Toc194753966)

[3.3 Produktumgebung 5](#_Toc194753967)

[4 Funktionale Anforderungen 6](#_Toc194753968)

[4.1 Produktfunktionen 6](#_Toc194753969)

[4.2 Produktdaten 6](#_Toc194753970)

[5 Nicht funktionale Anforderungen 7](#_Toc194753971)

[5.1 Produkt Leistung, Informationssicherheit, Schnittstellen 7](#_Toc194753972)

[5.2 Anforderung an Dokumentationen und Konzepte 7](#_Toc194753973)

[5.2.1 Benutzerdokumentation 7](#_Toc194753974)

[5.2.2 Technische Dokumentation 7](#_Toc194753975)

[5.2.3 Abschlusspräsentation (Produkt) 7](#_Toc194753976)

[5.2.4 Konzept CI und Branding 7](#_Toc194753977)

[5.2.5 Konzept Arbeitszeitgestaltung 8](#_Toc194753978)

[6 Liefergegenstände 8](#_Toc194753979)

[7 Projektplanung 8](#_Toc194753980)

[7.1 Projektphasen 8](#_Toc194753981)

[8 Offene Punkte, Ergänzungen 9](#_Toc194753982)

[9 Abnahmekriterien 9](#_Toc194753983)

[10 Ansprechpartner Kunde 9](#_Toc194753984)

# Ausgangssituation

Das HHBK Tendo Research Center entwickelt und vertreibt Computerspiele. Der Schwerpunkt lag bislang auf Entwicklung und Verkauf von kleineren Reaktionsspielen, die als OEM Produkte an verschiedene Hersteller mobiler Endgeräte geliefert wurden.

Die Geschäftsführung hat beschlossen, im Rahmen eines Spin-off (Ausgründung) selbst am Spielemarkt für Endkunden (B2C) teilzuhaben. Um mögliche Konkurrenzsituationen mit den Firmenkunden (B2B) zu vermeiden, soll der Schwerpunkt des Spin-off auf der Entwicklung linearer Algorithmen zur Unterstützung optimaler Spielstrategien von Strategiespielen liegen.

# Zielsetzung

Im ersten Schritt soll der Markteintritt mithilfe eines Markttests vorbereitet werden. Dazu sollen zeitgleich ein Prototyp einer Sammlung verschiedener Strategiespiele sowie eine Markenidentität für das Produkt entwickelt werden.

Corporate Identity soll von Beginn an als Unterstützung der Marke (Brand) mitgedacht werden, um auch als neuer Arbeitgeber im Wettbewerb um Fachkräfte bestehen zu können. In diesem Zusammenhang erachtet es die Geschäftsführung als wichtig, Erfahrungen und Vorschläge für das künftige Arbeitsmodell des Spin-off zu machen, mit dem Ziel, effektiv und nachhaltig in einem schnell veränderlichen Markt zu agieren.

Der Markttest soll mit Kunden möglichst verschiedener internationaler Märkte stattfinden (Deutschland, UK, Singapur, USA, Hongkong). Um den Markteintritt zu beschleunigen, soll ein mündlicher Pitch in englischer Sprache entwickelt und vorgetragen werden, mit dem Ziel, weitere Investoren (Kapitalgeber) zu gewinnen. Daher soll der Prototyp der Spielesammlung mindestens in englischer Sprache verfügbar sein.

Die Geschäftsführung bewertet den Einsatz eines Algorithmus aus dem Bereich der künstlichen Intelligenz, den sogenannten **MiniMax** Algorithmus, als entscheidend für den Markterfolg.

Für den Markttest der Spielesammlung und des **MiniMax** Algorithmus sollen daher zunächst die folgenden Spiele mit vereinfachten Regeln auf einem Spielfeld mit 6x6 Feldern umgesetzt werden :

- **Bauernschach**
- **Dame**
- **Tic-Tac-Toe**

Auf den nächsten Seiten werden diese Spiele genauer beschrieben.

## Spielbeschreibungen

Für den Prototypen soll immer der menschliche Spieler beginnen und die KI entsprechend mit den schwarzen Spielfiguren ziehen.

### ![Lastenheft_Strategiespiele_V13a](<Projekt%202026/Lastenheft/Attachments/Lastenheft_Strategiespiele_V13a%202.png>)Bauernschach

ist eine simple Variante des Schachs, die nur mit Bauern gespielt wird. In der Ausgansstellung stehen dabei die weißen bzw. schwarzen Spielfiguren (Bauern) auf der jeweiligen Grundlinie. Die Spieler machen abwechselnd einen Zug, wobei Weiß beginnt.

Es gibt zwei erlaubte Sorten von Zügen :

1. Ziehen

kann ein Bauer, indem er ein Feld in Richtung der gegnerischen Grundlinie (das sind die Felder, auf denen anfangs die gegnerischen Bauern stehen) geht, aber nur sofern dieses Feld frei ist (also nicht von einem eigenen oder gegnerischen Bauern besetzt ist).

1. Schlagen

kann ein Bauer in Richtung der gegnerischen Grundlinie durch diagonales Ziehen in Richtung der gegnerischen Grundlinie, aber nur auf ein Feld, auf dem ein gegnerischer Bauer steht.

Ziel des Spieles ist es, einen Bauern auf die generische Grundlinie zu platzieren; wenn das gelingt, ist das Spiel sofort zu Ende und die Farbe, die das erreicht hat, hat gewonnen. Wenn ein Spieler nicht mehr ziehen kann, oder überhaupt keine Figuren mehr hat, ist das Spiel für ihn als verloren zu werten. Ein unentschieden ist daher in dieser Variante nicht möglich.

### ![Lastenheft_Strategiespiele_V13a](<Projekt%202026/Lastenheft/Attachments/Lastenheft_Strategiespiele_V13a%203.png>)Dame

Das Dame Spiel soll mit vereinfachten Regeln auf einem 6x6 Spielfeld umgesetzt werden.

Zu Beginn werden für beide Spieler die Spielsteine auf den schwarzen Feldern der ersten zwei Reihen des Spielfeldes verteilt. Gespielt wird nur auf den dunklen Feldern. Die Steine ziehen jeweils ein Feld vorwärts in diagonaler Richtung.

Es herrscht generell Schlagzwang, gegnerische Steine müssen entsprechend übersprungen und dadurch geschlagen werden, sofern das direkt angrenzende dahinter liegende Feld frei ist. Der schlagende Stein wird auf dieses freie Feld gezogen und wenn das Zielfeld eines Sprungs auf ein Feld führt, von dem aus ein weiterer Stein übersprungen werden kann, wird der Sprung fortgesetzt. Alle übersprungenen Steine werden nach dem Zug vom Brett genommen. Es darf dabei nicht über eigene Spielsteine gesprungen werden.

- Das Spiel ist gewonnen, wenn ein Spieler einen Spielstein auf der gegnerischen Grundlinie platzieren kann.
- Das Spiel ist verloren, wenn ein Spieler nicht mehr ziehen kann, oder keine Spielsteine mehr hat
- Ein unentschieden ist somit in dieser Variante ebenfalls nicht möglich.

### ![Lastenheft_Strategiespiele_V13a](<Projekt%202026/Lastenheft/Attachments/Lastenheft_Strategiespiele_V13a%204.png>)Tic-Tac-Toe

Dieses Spiel wird in dieser Version ebenfalls auf einem 6x6 Spielfeld gespielt und ist auch unter dem Namen „Vier gewinnt“ bekannt.

Beide Spieler setzen abwechselnd ihre Spielsteine auf ein freies Feld.

Der Spieler, der als Erster vier seiner Spielsteine in eine Zeile, Spalte oder Diagonale setzen kann, gewinnt.

Das Spiel ist unentschieden, wenn alle Felder belegt sind, ohne dass ein Spieler die erforderlichen Spielsteine in einer Reihe, Spalte oder Diagonalen setzen konnte.

### MiniMax Algorithmus

Der Minimax-Algorithmus ist ein Algorithmus, der im Bereich der künstlichen Intelligenz und der Spieltheorie verwendet wird. Grundlage des Minimax-Algorithmus ist eine Bewertungsfunktion. Diese misst für jede Position eines Zwei-Personen-Nullsummenspiels (ein Spieler gewinnt bedeutet, der andere Spieler verliert) die Gewinnaussichten, und zwar aus der Perspektive eines der beiden Spieler. Das folgende in der Literatur beschriebene Diagramm illustriert den **rekursiv** arbeitenden Algorithmus. Im Idealfall kann derselbe Algorithmus unabhängig vom konkret ausgewählten Spiel wiederverwendet werden.

![Lastenheft_Strategiespiele_V13a](<Projekt%202026/Lastenheft/Attachments/Lastenheft_Strategiespiele_V13a%205.png>)

# Produkteinsatz

## Anwendungsbereiche

- Freizeitbereich
- Der Prototype dient einerseits zum Testen der eigentlichen Spielstrategie, andererseits zum Ausloten der vom Kunden gewünschten Funktionalität.

## Zielgruppen

- Zielgruppe sind ausgewählte Testpersonen im Alter zwischen 12 und 99, die strategische Spiele bevorzugen.

## Produktumgebung

- Die Anwendung wird auf PC gespielt. Das Betriebssystem ist Windows 10 oder 11.

# Funktionale Anforderungen

## Produktfunktionen

LF4000 Für den Prototypen sollen mindestens zwei der Spiele realisiert werden. (Must have)

LF4010 Beide Spiele sollen in eine gemeinsame Anwendung mit graphischer Benutzeroberfläche integriert werden. (Must have)

LF4020 Alle Spiele werden auf einem Spielfeld mit 6x6 Feldern gespielt. (Must have)

LF4030 Der KI Spieler nutzt jeweils den Minimax Algorithmus. (Must have)

LF4040 Bei allen Spielen hat der Mensch den ersten Zug, und die KI zieht als Zweites. (Must have)

LF4050 Für jedes Spiel soll die Spielstärke einstellbar sein (Suchtiefe mit Bewertungsfunktion) (Must have)

LF4060 Ein Spielabbruch während des Spiels soll möglich sein. (Must have)

LF4070 Jeder Spieler muss sich als Benutzer registrieren bzw. einloggen können. (Must have)

LF4080 Für jedes Spiel soll in Abhängigkeit der eingestellten Spielstärke die Anzahl der Siege und Niederlagen in einer Bestenliste gespeichert werden. (Must have)

LF4090 Beim Spielen als nicht registrierter Gast entfällt die Speicherung in der Bestenliste. (Must have)

LF4100 Die Bestenliste soll für jedes Spiel separat angezeigt werden können. (Must have)

LF4110 Für jedes Spiel sollen die Spielregeln während des Spiels angezeigt werden können. (Must have)

LF4120 Der Minimax-Algorithmus kann durch Verwendung von Alpha-Beta-Pruning optimiert werden. (Should have)

LF4120 Es besteht die Möglichkeit zur Einbindung einer anderen KI’s (Vereinbarung einer Schnittstelle) (Could have)

LF4130 Es besteht für jeden Nutzer die Möglichkeit zur Auswahl der alternativen Sprache Deutsch als Alternative zur Standardsprache (Could have)

LF4140 Das Spiel wird von einem Spieler am PC gespielt. Netzwerkfähigkeit ist nicht gefordert. (Wont have)

## Produktdaten

LD4200 Die Speicherung der registrierten Spieler erfolgt in einer Datenbank. Das DBMS ist unabhängig von der Anwendung. (Must have)

LD4210 Siege und Niederlagen werden für den Spieler, abhängig vom Spiel und der Spielstärke, in der Datenbank gespeichert. (Must have)

LD4220 Die Bestenliste kann durch geeignete Datenbankabfragen generiert werden. (should have)

LD4230Speicherung der Spracheinstellungen für Benutzer, Default-Spracheinstellung in einer Datenbank. (Could have)

# Nicht funktionale Anforderungen

## Produkt Leistung, Informationssicherheit, Schnittstellen

LN5000 Die Anwendung muss in Python programmiert werden. Ein für Python geeignetes GUI Framework ist zu verwenden.

LN5001 Aufgrund des algorithmischen Schwerpunkts muss die Anwendung prozedural programmiert werden. Insbesondere soll „Boilerplate-Code“ der Objektorientierung vermieden werden.

LN5010 Der Zug des Computerspielers darf nicht länger als 45 Sekunden dauern.

LN5020 Alle Benutzerdaten müssen persistent gespeichert werden

LN5030 Passworte dürfen nicht als Klartext gespeichert werden.

LN5040 Beim Design des Prototyps soll der Schwerpunkt auf wiederverwendbare Software gelegt werden. Aus diesem Grund wird eine modulare und funktionsorientierte Architektur mit sauber definierten Schnittstellen erwartet.

LN5050 Die Benutzerschnittstelle soll eine intuitive Bedienung ermöglichen.

LN5060 Die Benutzerschnittstelle soll das Brand Identity Konzept und damit verbundene Design Elemente aufgreifen.

## Anforderung an Dokumentationen und Konzepte

### Benutzerdokumentation

LD5100 Einer nicht im Projekt beteiligten Person ist die Installation und Ausführung der Anwendung möglich.

### Technische Dokumentation

LD5200 Beschreibung des Spielverhaltens zur Laufzeit.

LD5210 Erläuterungen des Spielealgorithmus und der Bewertungsfunktion mit Schwierigkeitsgrad.

LD5220 Beschreibung der Software-Architektur.

LD5230 Beschreibung der verwendeten globalen Variablen.

### Abschlusspräsentation (Produkt)

LD5300 Darstellung SOLL/IST Vergleich realisierte Features Lastenheft vs Pflichtenheft vs Umsetzung vs Test

LD5310 Darstellung SOLL/IST Projektplanung Pflichtenheft vs. Projektverlauf

LD5320 Darstellung wesentlicher Softwarekomponenten oder Ideen, z.B. Erläuterung MinMax, Bewertungsfunktion, GUI

LD5330 Quellen oder Werkzeuge

LD5340 Fazit zum Projektverlauf: Zusammenarbeit, Aufwand, Lessons learnt

### Konzept CI und Branding

LD5400 Konzept begründet gewählte Design Elemente, Mission und Vision Statement für CI und die neue Marke der HHBKTendo.

LD5410 Englischsprachiges Pitch-Konzept und Skript für eine mündliche Präsentation. Der Pitch muss eine überzeugende Argumentation für potentielle Investoren enthalten und einen hohen Aufmerksamkeitswert besitzen.

### Konzept Arbeitszeitgestaltung

LD5500 Das Konzept stellt insbesondere Plan und IST Arbeitszeiten gegenüber, benennt Risiken und Herausforderungen und stellt diese zukünftig zu etablierenden Rahmenbedingungen für Projektarbeit innerhalb der HHBKTendo gegenüber.

# Liefergegenstände

- Pflichtenheft inkl. Projektplan, Work (Product) Breakdown, Ressourcenplan, Zeitplan
- Testprotokoll Abnahmetestcases
- Software Prototyp inkl. Dokumentation, Präsentation
- Konzept Corporate Identity und Brand Identity, Präsentation
- Konzept Arbeitszeitgestaltung und Auswertung, Empfehlung
- Mündlicher Pitch in englischer Sprache (inkl. Präsentationsfolien und Handout für potenzielle Investoren) zur Vorstellung auf einer internationalen Fachmesse

# Projektplanung

## Projektphasen

Das Projekt soll aufgrund der kurzen Laufzeit sequenziell nach dem erweiterten Wasserfallmodell geplant und durchgeführt werden.

Folgende Artefakte sind während der Analysephase (Woche 1: LF2, LF5, DKO, FKO, WBL) zu erstellen und dem Kunden vor Beginn der SW Design und Implementierungsphase vorzulegen:

- Projektplan
- Work (Product) Breakdown Structure
- Ressourcenplan
- Zeitplan
- Pflichtenheft mit Detaillierung der Produktanforderungen und sonstiger Liefergegenstände.

Während des Projekts ist dem Kunden zu mindestens zwei Terminen ein Projektstatus vorzutragen. Dieser beinhaltet in Form einer Powerpoint Präsentation:

- SOLL-IST Vergleich des Projektfortschritts
- Übersicht über den Ressourceneinsatz
- Benennung von Problemen und Risiken

Nach Abschluss von SW Design, Implementierung und Test (Woche 2: Vollzeit in distanz):

- Lieferung (Upload in Moodle) aller Quellcodedateien incl. Datenbank.
- Benutzerdokumentation zu Installation.
- Testprotokolle

Nach Abschluss der Dokumentationsphase (Woche 3: LF2, LF5, DKO, FKO, WBL)

- Projektabschluss durch Präsentation und Live Demo (ca. 20min + 10min Fachgespräch).

# Offene Punkte, Ergänzungen

- Der Projektauftrag wird an kleinere Teams mehrfach vergeben, um zwischen den besten Prototypen wählen zu können. Einem Projektteam sollten nicht mehr als 5-6 Mitglieder angehören. Die einzelnen Teams sollten so weit möglich „autark“ arbeiten. Ein Austausch von Arbeitsergebnissen ist im Sinne der Konkurrenzsituation nicht erwünscht.Technische Ratschläge und Hilfestellungen unter Kolleginnen und Kollegen sollten allerdings selbstverständlich sein.
- Der Teamleiter oder die Teamleiterin ist Ansprechpartner des Auftraggebers. Rückfragen an den Auftraggeber können aber an Teammitglieder delegiert werden. Rückfragen an den Kunden werden auf Bitte des Kunden öffentlich über die Lernplattform im Projektforum gestellt.

# Abnahmekriterien

Abnahmekriterien sind:

- Vollständigkeit der Liefergegenstände, insbes. Life Demo und Abschlusspräsentation.
- Anforderungen gem. Pflichtenheft
- Konsistenz der Produkteigenschaften mit Testprotokollen

# Ansprechpartner Kunde

APRA, WENK: Produkteigenschaften, Projektmanagement, Produktrealisierung

SOET: Projektmanagement Artefakte, Statusbericht, Ex-post Analyse

VEIT: Arbeitszeitgestaltung und Teamarbeit

KRAE: Pitch-Deck bzw. Investment Memorandum

FISC: Corporate Identity Konzept