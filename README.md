# Workshop-Zuteilungs-Tool

Ein Desktop-Tool zur optimalen Zuteilung von Schülern zu Workshops basierend auf ihren Präferenzen.

**Version:** 1.0.0
**Status:** ✅ Refactored mit MVC-Architektur

## 🎯 Überblick

Dieses Tool hilft Lehrern bei der automatischen, optimalen Zuteilung von Schülern zu Workshops über mehrere Tage. Es verwendet einen mathematischen Optimierungsalgorithmus (Linear Programming), um die Gesamtzufriedenheit zu maximieren.

### Hauptfunktionen

- ✅ **Excel-Import**: Schülerdaten aus Excel-Dateien importieren
- ⚙️ **Flexible Parameter**: Anpassbare Optimierungsparameter
- 🚀 **Automatische Optimierung**: Mathematisch optimale Zuteilung
- 📊 **Detaillierte Ergebnisse**: Statistiken und Visualisierungen
- 💾 **Excel-Export**: Ergebnisse als Excel-Datei exportieren
- 🔒 **DSGVO-konform**: Alle Daten bleiben lokal

## 🏗️ Architektur

Das Projekt folgt einer sauberen **MVC (Model-View-Controller)** Architektur:

```
clown_orga/
├── models/              # Datenmodelle (Student, Workshop, etc.)
├── views/               # UI-Komponenten
│   ├── wizard/          # 5-Schritt Wizard-Interface
│   ├── components/      # Wiederverwendbare UI-Komponenten
│   └── main_window.py   # Hauptfenster
├── controllers/         # Anwendungslogik
│   ├── app_controller.py    # Haupt-Controller
│   └── app_state.py         # Zustandsverwaltung
├── services/            # Business Logic Services
│   ├── data_service.py        # Excel Import/Export
│   ├── optimization_service.py # Optimierungsalgorithmus
│   ├── validation_service.py  # Datenvalidierung
│   └── config_service.py      # Konfigurationsverwaltung
├── utils/               # Hilfsfunktionen
│   ├── constants.py     # Konstanten
│   └── helpers.py       # Formatierung, etc.
└── tests/               # Unit Tests (86 Tests)
```

### Architektur-Prinzipien

1. **Separation of Concerns**: Jede Schicht hat eine klare Verantwortung
2. **Dependency Injection**: Services werden als Dependencies übergeben
3. **Type Safety**: Type Hints und Dataclasses überall
4. **Testability**: Business Logic unabhängig von UI testbar
5. **Reusability**: Komponenten sind wiederverwendbar

Detaillierte Architektur-Dokumentation: [`ARCHITECTURE.md`](ARCHITECTURE.md)

## 🚀 Installation

### Voraussetzungen

- Python 3.8+
- pip

### Setup

```bash
# Virtual Environment erstellen
python3 -m venv venv

# Virtual Environment aktivieren
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Abhängigkeiten installieren
pip install -r requirements.txt
```

## 📖 Verwendung

### Anwendung starten

```bash
python app.py
```

### Wizard-Schritte

Die Anwendung führt Sie durch 5 Schritte:

1. **📥 Daten importieren**
   - Excel-Datei per Drag & Drop oder File Dialog
   - Automatische Validierung
   - Datenvorschau

2. **⚙️ Parameter festlegen**
   - Anzahl Tage
   - Max. Teilnehmer pro Workshop
   - Klassenverband beibehalten?
   - Gewichtung der Wünsche

3. **✅ Einstellungen prüfen**
   - Zusammenfassung aller Einstellungen
   - Machbarkeitsanalyse
   - Warnungen bei Problemen

4. **🚀 Optimierung**
   - Automatische Berechnung
   - Live-Progress-Anzeige
   - Detailliertes Log

5. **📊 Ergebnisse**
   - Zufriedenheitsrate
   - Statistiken (1./2./3./4. Wunsch)
   - Workshop-Übersicht
   - Export als Excel

## 📁 Excel-Format

### Eingabedatei

Excel-Datei mit folgenden Spalten:

| Spalte    | Beschreibung        | Pflicht |
|-----------|---------------------|---------|
| vorname   | Vorname des Schülers| Ja      |
| nachname  | Nachname            | Ja      |
| klasse    | Klassenbezeichnung  | Ja      |
| wunsch1   | Erstwunsch          | Ja      |
| wunsch2   | Zweitwunsch         | Ja      |
| wunsch3   | Drittwunsch         | Ja      |
| wunsch4   | Viertwunsch         | Ja      |

### Ausgabedatei

Die exportierte Excel-Datei enthält 3 Sheets:

1. **Schüler**: Alle Schüler mit zugeteilten Workshops (Tag 1, Tag 2, Tag 3)
2. **Workshops**: Workshop-Übersicht mit Teilnehmerlisten
3. **Statistik**: Detaillierte Statistiken zur Zuteilung

## 🧪 Testing

```bash
# Alle Tests ausführen
pytest

# Mit Coverage-Report
pytest --cov=. --cov-report=html

# Nur bestimmte Tests
pytest tests/test_models.py
pytest tests/test_services.py
```

**Test-Abdeckung:** 86 Tests, 100% Models, ~90% Services

## 🎨 UI-Komponenten

### Wiederverwendbare Komponenten

Das Projekt enthält folgende wiederverwendbare UI-Komponenten:

- **Dropzone**: Drag & Drop Dateiauswahl
- **Tooltip / TooltipIcon**: Kontextuelle Hilfe
- **DataPreview**: Tabellenvorschau für Daten
- **ProgressStepper**: Fortschrittsanzeige für Wizard
- **InfoPanel**: Ausklappbare Informationspanels

Alle Komponenten sind in `views/components/` dokumentiert.

## ⚙️ Konfiguration

### Themes

Die Anwendung unterstützt 6 Bootstrap-Themes:
- `cosmo` (Standard): Hell, modern
- `darkly`: Dark Mode
- `flatly`: Clean & minimal
- `superhero`: Dark mit Farbe
- `litera`: Gut lesbar
- `cyborg`: Dark Tech

Theme kann zur Laufzeit gewechselt werden (Dropdown oben rechts).

### Parameter

Standard-Parameter können in `utils/constants.py` angepasst werden:

```python
DEFAULT_NUM_DAYS = 3
DEFAULT_NUM_WORKSHOPS = 12
DEFAULT_MAX_PARTICIPANTS = None  # Unbegrenzt
DEFAULT_KEEP_CLASSES_TOGETHER = "egal"
DEFAULT_WISH_WEIGHTS = {
    'wunsch1': 10,
    'wunsch2': 5,
    'wunsch3': 2,
    'wunsch4': 1
}
```

## 🧮 Optimierungsalgorithmus

Der Kern der Anwendung ist ein **Linear Programming (LP)** Algorithmus, implementiert in `services/optimizer.py`.

### Funktionsweise

**Problemtyp:** Constraint Satisfaction Problem (CSP)

**Ziel:** Maximiere die Gesamtzufriedenheit aller Schüler unter Einhaltung aller Randbedingungen.

### Komponenten

#### 1. Entscheidungsvariablen (`optimizer.py:46-57`)
```
assignments[student_id][workshop_id][day] ∈ {0, 1}
```
- `1` = Schüler wird diesem Workshop an diesem Tag zugeteilt
- `0` = nicht zugeteilt

#### 2. Zielfunktion (`optimizer.py:60-75`)
```
Maximiere: Σ (Gewichtung × Zuteilungs-Variable)
```

Gewichtungen (Standard):
- 1. Wunsch: 10 Punkte
- 2. Wunsch: 5 Punkte
- 3. Wunsch: 3 Punkte
- 4. Wunsch: 1 Punkt
- Nicht gewünscht: 0 Punkte

#### 3. Nebenbedingungen

**Hard Constraints:**

1. **Ein Workshop pro Tag** (`optimizer.py:78-83`)
   ```
   Für jeden Schüler an jedem Tag: Σ assignments[s][w][d] = 1
   ```

2. **Kapazitätsgrenzen** (`optimizer.py:86-98`)
   ```
   Für jeden Workshop an jedem Tag: Σ assignments[s][w][d] ≤ max_capacity
   ```

3. **Klassenverband** (`optimizer.py:101-138`)
   - Optional: Schüler derselben Klasse müssen zusammenbleiben
   - Nutzt zusätzliche binäre Variablen für Klassen-Zuteilungen

#### 4. Solver (`optimizer.py:143-144`)

Verwendet **PULP_CBC_CMD** (COIN-OR Branch and Cut):
- Open-Source Mixed-Integer Programming Solver
- Findet garantiert optimale Lösung (oder meldet "keine Lösung möglich")
- Laufzeit: O(exponentiell im Worst-Case), in Praxis sehr schnell

### Beispiel

Für 100 Schüler, 12 Workshops, 3 Tage:
- **Variablen:** ~3.600 binäre Variablen
- **Constraints:** ~300 Nebenbedingungen
- **Laufzeit:** Typisch < 1 Sekunde

## 🔧 Technologien

- **Python 3.12**
- **tkinter**: GUI Framework
- **ttkbootstrap**: Bootstrap-Themes für tkinter
- **pandas**: Excel-Verarbeitung
- **openpyxl**: Excel-IO
- **PuLP**: Lineare Optimierung (CBC Solver)
- **pytest**: Testing Framework

## 📚 Dokumentation

- [`ARCHITECTURE.md`](ARCHITECTURE.md): Detaillierte Architektur-Dokumentation
- [`UI_UX_DESIGN.md`](UI_UX_DESIGN.md): UX/UI Design-Entscheidungen
- [`brief.md`](brief.md): Original-Anforderungen

## 🤝 Entwicklung

### Code-Stil

- Type Hints überall
- Docstrings (Google Style)
- PEP 8 konform
- Maximal 100 Zeichen pro Zeile

### Neue Features hinzufügen

1. **Model** in `models/` erstellen (mit Tests)
2. **Service** in `services/` implementieren (mit Tests)
3. **Controller**-Methode in `controllers/` hinzufügen
4. **View** in `views/` erstellen
5. Tests schreiben und ausführen

### Testing-Strategie

- **Unit Tests**: Für Models und Services
- **Integration Tests**: Für Controller
- **UI Tests**: Manuell (tkinter schwer zu testen)

## 📦 Als .exe exportieren

Um eine eigenständige .exe-Datei zu erstellen:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "Workshop-Tool" app.py
```

Die .exe findet sich dann im `dist/` Ordner.

## 📝 Lizenz

Für Schulnutzung entwickelt. Alle Rechte vorbehalten.

## 🙏 Credits

Entwickelt mit Claude Code (Anthropic).

---

**🔒 DSGVO-Hinweis:** Alle Daten bleiben lokal auf Ihrem Rechner. Es findet keine Cloud-Verarbeitung statt.
