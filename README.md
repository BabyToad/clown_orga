# Workshop-Zuteilungs-Tool

Ein Desktop-Tool zur optimalen Zuteilung von Schülern auf Workshops basierend auf ihren Präferenzen.

## Features

- 📊 **Excel Import/Export** - Einfaches Einlesen und Exportieren von Schülerdaten
- 🎯 **Intelligente Optimierung** - Maximiert die Zufriedenheit basierend auf Wünschen
- ⚙️ **Flexible Parameter** - Alle Einstellungen vor der Berechnung anpassbar
- 🎨 **Moderne GUI** - Intuitive, deutschsprachige Benutzeroberfläche
- 🔒 **DSGVO-konform** - Alle Daten bleiben lokal auf dem Computer
- 💾 **Persistente Settings** - Parameter werden automatisch gespeichert

## Installation

### Voraussetzungen

- Python 3.8 oder höher
- pip (Python Package Manager)

### Einrichtung

1. Repository klonen oder herunterladen

2. Abhängigkeiten installieren:
```bash
pip install -r requirements.txt
```

## Verwendung

### Anwendung starten

```bash
python gui.py
```

### Workflow

1. **Excel-Datei importieren**
   - Klick auf "Excel-Datei auswählen"
   - Datei mit Schülerdaten auswählen (siehe Format unten)

2. **Parameter einstellen**
   - Anzahl der Tage
   - Anzahl der Workshops
   - Maximale Teilnehmerzahl pro Workshop
   - Klassen-Zusammenhalt-Präferenz
   - Gewichtung der Wünsche anpassen

3. **Optimierung starten**
   - Klick auf "Optimierung starten"
   - Warten bis Berechnung abgeschlossen ist

4. **Ergebnisse exportieren**
   - Klick auf "Ergebnisse exportieren"
   - Speicherort wählen

## Excel-Format

### Eingabe-Datei

Die Excel-Datei muss folgende Spalten enthalten:

| Spalte | Beschreibung |
|--------|--------------|
| `vorname` | Vorname des Schülers |
| `nachname` | Nachname des Schülers |
| `klasse` | Klasse (z.B. "5a", "6b") |
| `wunsch1` | Erster Wunsch (Workshop-Name) |
| `wunsch2` | Zweiter Wunsch (Workshop-Name) |
| `wunsch3` | Dritter Wunsch (Workshop-Name) |
| `wunsch4` | Vierter Wunsch (Workshop-Name) |

**Hinweise:**
- Groß-/Kleinschreibung der Spaltenüberschriften ist egal
- Workshop-Namen können frei gewählt werden (z.B. "Töpfern", "Musik", "Sport")
- Workshop-Namen und -Anzahl können jedes Jahr unterschiedlich sein

### Ausgabe-Datei

Die exportierte Excel-Datei enthält drei Sheets:

1. **Zuteilungen** - Alle Schülerdaten plus zugeteilte Workshops pro Tag
2. **Workshop-Übersicht** - Welcher Workshop an welchem Tag, mit Teilnehmerliste
3. **Statistik** - Zusammenfassung der Wunsch-Erfüllung

## Projekt-Struktur

```
clown_orga/
├── gui.py              # Hauptanwendung mit GUI
├── config.py           # Konfigurations-Management
├── data_handler.py     # Excel Import/Export & Validierung
├── optimizer.py        # Optimierungs-Algorithmus
├── requirements.txt    # Python-Abhängigkeiten
├── settings.json       # Gespeicherte Parameter (wird automatisch erstellt)
└── README.md          # Diese Datei
```

## Als .exe exportieren

Um eine eigenständige .exe-Datei zu erstellen (ohne Python-Installation):

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "Workshop-Tool" gui.py
```

Die .exe findet sich dann im `dist/` Ordner.

## Technische Details

### Optimierungs-Algorithmus

- **Engine:** PuLP (Linear Programming)
- **Ziel:** Maximierung der Gesamt-Zufriedenheit
- **Constraints:**
  - Jeder Schüler bekommt pro Tag genau einen Workshop
  - Keine Workshop-Wiederholungen für denselben Schüler
  - Maximale Teilnehmerzahl pro Workshop (optional)
  - Klassen-Zusammenhalt (optional, soft constraint)

### Parameter-Anpassung

Alle Parameter sind Jahr für Jahr anpassbar:
- Workshop-Namen werden automatisch aus der Excel-Datei erkannt
- Anzahl der Workshops kann variieren
- Anzahl der Tage ist flexibel (Standard: 3)
- Gewichtung der Wünsche kann individuell eingestellt werden

## Testing

Das Projekt enthält umfassende Tests (58+ Tests):

```bash
# Alle Tests ausführen
python -m pytest -v

# Mit Coverage-Report
./run_tests.sh        # Linux/Mac
run_tests.bat         # Windows

# Test-Daten generieren
python create_test_data.py
```

Weitere Details siehe [TESTING.md](TESTING.md).

## Lizenz

Dieses Tool wurde für den internen Gebrauch an Schulen entwickelt.

## Support

Bei Fragen oder Problemen, bitte ein Issue erstellen oder direkt kontaktieren.
