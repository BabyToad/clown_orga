# UI/UX Design Plan - Workshop-Zuteilungs-Tool

## User Research & Pain Points

### Target User Profile
- **Role**: Non-technical teacher
- **Current workflow**: Manual Excel work
- **Frustrations**: Time-consuming, error-prone, complex
- **Needs**: Simple, guided, trustworthy, explainable

### Current UX Issues Identified

1. **Cognitive Overload**: All 4 sections visible at once, overwhelming
2. **No Guidance**: User doesn't understand what the algorithm does
3. **Hidden Context**: Parameters lack explanations (what does weighting mean?)
4. **Trust Issues**: "Black box" optimization - no transparency
5. **No Progressive Disclosure**: Everything shown upfront
6. **Missing Validation Feedback**: Unclear if inputs are good/bad
7. **No Contextual Help**: Users left to figure things out alone

## Modern UX Principles to Apply

### 1. **Progressive Disclosure**
Show only what's needed, when it's needed
- Wizard/stepper interface (Step 1 → 2 → 3 → 4)
- Expand/collapse advanced options
- Focus on one task at a time

### 2. **Transparency & Trust**
Explain the "magic" behind the algorithm
- "How it works" section with simple language
- Visual representation of optimization
- Show the math in human terms

### 3. **Contextual Help**
Help embedded where it's needed
- Tooltips with ⓘ icons
- "What's this?" expandable panels
- Example values
- Live validation messages

### 4. **Visual Hierarchy**
Guide attention to what matters
- Clear primary actions
- Secondary/tertiary actions clearly distinguished
- Visual flow from top to bottom

### 5. **Feedback & Reassurance**
Tell users what's happening
- Live preview of data
- Validation indicators (✓ ✗ ⚠)
- Progress with substeps
- Success confirmations

### 6. **Forgiveness**
Allow mistakes and corrections
- Undo/reset options
- Confirmation for destructive actions
- Auto-save draft state
- Clear error recovery

## Proposed Layout: Wizard-Style Interface

### Layout Structure

```
┌─────────────────────────────────────────────────────────────────┐
│  🎨 Workshop-Zuteilung                     [?] Hilfe  [🌓] Theme │
│  Optimale Zuordnung von Schülern zu Workshops                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Fortschritt                                            │   │
│  │  ●━━━━━━━ ○────── ○────── ○────── ○                    │   │
│  │  Daten    Parameter Prüfen  Optimieren Ergebnis         │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    [MAIN CONTENT AREA]                   │   │
│  │                                                           │   │
│  │            (Changes based on current step)               │   │
│  │                                                           │   │
│  │                                                           │   │
│  │                                                           │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  💡 Wie funktioniert die Optimierung?  [▼ Mehr erfahren] │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                   │
│              [← Zurück]              [Weiter →]                  │
│                                                                   │
│  🔒 DSGVO-konform | Alle Daten bleiben lokal | v1.0             │
└─────────────────────────────────────────────────────────────────┘
```

### Step-by-Step Screens

---

## STEP 1: Daten importieren

```
┌─────────────────────────────────────────────────────────────────┐
│  Fortschritt: ●━━━━━━━ ○────── ○────── ○────── ○               │
│               Daten    Parameter Prüfen  Optimieren Ergebnis     │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  📥 Schülerdaten importieren                                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│   ┌───────────────────────────────────────────────────────┐    │
│   │                                                         │    │
│   │          📂 Excel-Datei hierher ziehen                 │    │
│   │              oder klicken zum Auswählen                │    │
│   │                                                         │    │
│   │          Unterstützte Formate: .xlsx, .xls             │    │
│   │                                                         │    │
│   └───────────────────────────────────────────────────────┘    │
│                                                                   │
│   ℹ️ Die Datei sollte folgende Spalten enthalten:               │
│   • Vorname                                                      │
│   • Nachname                                                     │
│   • Klasse                                                       │
│   • Wunsch1, Wunsch2, Wunsch3, Wunsch4                          │
│                                                                   │
│   📋 [Beispiel-Datei herunterladen]                             │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  💡 Wie funktioniert die Optimierung?          [▼ Mehr erfahren] │
└─────────────────────────────────────────────────────────────────┘

                              [Weiter →] (disabled)
```

**After file loaded:**

```
┌─────────────────────────────────────────────────────────────────┐
│  📥 Schülerdaten importieren                                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│   ✅ Datei erfolgreich geladen: schueler_2024.xlsx              │
│   [Andere Datei wählen]                                          │
│                                                                   │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │ 📊 Datenvorschau                                         │  │
│   ├─────────────────────────────────────────────────────────┤  │
│   │                                                           │  │
│   │  ✓ 47 Schüler gefunden                                   │  │
│   │  ✓ 8 Klassen (5a, 5b, 5c, 6a, 6b, 6c, 7a, 7b)          │  │
│   │  ✓ 12 verschiedene Workshops                             │  │
│   │                                                           │  │
│   │  ─────────────────────────────────────────────────────   │  │
│   │  Vorname    Nachname   Klasse   Wunsch1      Wunsch2    │  │
│   │  Anna       Müller     5a       Töpfern      Musik      │  │
│   │  Ben        Schmidt    5a       Sport        Kunst      │  │
│   │  Clara      Weber      5b       Theater      Kochen     │  │
│   │  ...                                                      │  │
│   │                                        [Alle anzeigen ▼] │  │
│   └─────────────────────────────────────────────────────────┘  │
│                                                                   │
│   ⚠️ Warnungen (3):                                              │
│   • 2 Schüler haben denselben Workshop mehrfach gewählt         │
│   • 1 Schüler hat nur 3 Wünsche angegeben                       │
│   [Details anzeigen]                                             │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘

                              [Weiter →] (enabled)
```

---

## STEP 2: Parameter einstellen

```
┌─────────────────────────────────────────────────────────────────┐
│  Fortschritt: ○━━━━━━━ ●━━━━━━ ○────── ○────── ○               │
│               Daten    Parameter Prüfen  Optimieren Ergebnis     │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  ⚙️ Optimierungs-Parameter festlegen                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  📅 Zeitrahmen                                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Über wie viele Tage sollen die Workshops verteilt      │   │
│  │  werden?                                                 │   │
│  │                                                           │   │
│  │  Anzahl Tage: [3 ▼]  ⓘ Jeder Schüler besucht pro Tag   │   │
│  │                          einen Workshop                   │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                   │
│  👥 Kapazitäten                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Gibt es eine Begrenzung für die Teilnehmerzahl?        │   │
│  │                                                           │   │
│  │  ○ Unbegrenzt                                            │   │
│  │  ● Maximum festlegen: [25] Schüler pro Workshop         │   │
│  │                                                           │   │
│  │  ⓘ Empfehlung: Betreuer-Schüler-Verhältnis 1:12-15      │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                   │
│  🏫 Klassenverbände                                              │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Sollen Schüler aus derselben Klasse bevorzugt          │   │
│  │  zusammenbleiben?                                         │   │
│  │                                                           │   │
│  │  ○ Ja, möglichst zusammen     ⓘ Soziale Bindungen       │   │
│  │  ○ Nein, mischen erwünscht    ⓘ Neue Kontakte           │   │
│  │  ● Egal, nach Wünschen        ⓘ Nur Präferenzen zählen  │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                   │
│  ⭐ Wunsch-Gewichtung                                            │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Wie stark sollen die verschiedenen Wünsche gewichtet   │   │
│  │  werden?                                                  │   │
│  │                                                           │   │
│  │  🥇 Wunsch 1: [10] Punkte    Höchste Priorität          │   │
│  │  🥈 Wunsch 2: [5]  Punkte    Mittlere Priorität         │   │
│  │  🥉 Wunsch 3: [2]  Punkte    Geringe Priorität          │   │
│  │  4️⃣  Wunsch 4: [1]  Punkt     Niedrigste Priorität       │   │
│  │                                                           │   │
│  │  💡 Standard-Einstellung (empfohlen) [Zurücksetzen]     │   │
│  │                                                           │   │
│  │  ⓘ Die Optimierung versucht, die Gesamtpunktzahl zu     │   │
│  │     maximieren. Höhere Gewichte = stärkerer Fokus auf   │   │
│  │     Erstwünsche                                           │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                   │
│  [▼ Erweiterte Optionen]                                         │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  💡 Wie funktioniert die Optimierung?          [▼ Mehr erfahren] │
└─────────────────────────────────────────────────────────────────┘

          [← Zurück]                           [Weiter →]
```

---

## STEP 3: Überprüfung

```
┌─────────────────────────────────────────────────────────────────┐
│  Fortschritt: ○━━━━━━━ ○━━━━━━ ●━━━━━━ ○────── ○               │
│               Daten    Parameter Prüfen  Optimieren Ergebnis     │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  ✓ Zusammenfassung & Überprüfung                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  Bitte überprüfen Sie die Einstellungen vor der Optimierung:    │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  📊 Daten                                                │   │
│  │  • 47 Schüler aus 8 Klassen                             │   │
│  │  • 12 verschiedene Workshops                             │   │
│  │  • Datei: schueler_2024.xlsx                            │   │
│  │                                          [Ändern]        │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  ⚙️ Parameter                                            │   │
│  │  • Tage: 3                                               │   │
│  │  • Max. Teilnehmer: 25 pro Workshop                     │   │
│  │  • Klassenverbände: Egal                                │   │
│  │  • Gewichtung: 10 / 5 / 2 / 1                           │   │
│  │                                          [Ändern]        │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  🔍 Vorschau der Optimierungsaufgabe                    │   │
│  │                                                           │   │
│  │  Gesamtzahl Plätze: 47 Schüler × 3 Tage = 141 Plätze   │   │
│  │  Verfügbare Optionen: 12 Workshops pro Tag              │   │
│  │                                                           │   │
│  │  ✓ Machbarkeit: Es gibt genug Kapazität für alle        │   │
│  │                                                           │   │
│  │  ⚠️ Potenzielle Engpässe:                                │   │
│  │    • "Programmieren" wurde von 18 Schülern als          │   │
│  │      Erstwunsch gewählt (max. 25 erlaubt)              │   │
│  │    • "Töpfern" wurde von 3 Schülern gewählt             │   │
│  │      (könnte unterbesetzt sein)                          │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  ⏱️ Geschätzte Berechnungszeit: 2-5 Sekunden             │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘

          [← Zurück]                      [⚡ Optimierung starten]
```

---

## STEP 4: Optimierung läuft

```
┌─────────────────────────────────────────────────────────────────┐
│  Fortschritt: ○━━━━━━━ ○━━━━━━ ○━━━━━━ ●━━━━━━ ○               │
│               Daten    Parameter Prüfen  Optimieren Ergebnis     │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  ⚡ Optimierung läuft...                                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│                                                                   │
│              ┌───────────────────────────────┐                   │
│              │         ⚙️  🔄  ⚡           │                   │
│              │                               │                   │
│              │    Berechne optimale          │                   │
│              │    Zuteilung...               │                   │
│              │                               │                   │
│              │  ████████████░░░░░░░ 65%     │                   │
│              │                               │                   │
│              └───────────────────────────────┘                   │
│                                                                   │
│                                                                   │
│  ℹ️ Was passiert gerade?                                         │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Der Algorithmus sucht die beste Kombination aus        │   │
│  │  Millionen möglicher Zuteilungen. Dabei werden alle     │   │
│  │  Wünsche, Kapazitäten und Regeln berücksichtigt.        │   │
│  │                                                           │   │
│  │  Aktuelle Phase: Löse lineares Optimierungsproblem...   │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                   │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘

                        [Abbrechen]
```

---

## STEP 5: Ergebnisse

```
┌─────────────────────────────────────────────────────────────────┐
│  Fortschritt: ○━━━━━━━ ○━━━━━━ ○━━━━━━ ○━━━━━━ ●━━━━━━         │
│               Daten    Parameter Prüfen  Optimieren Ergebnis     │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  ✅ Optimierung erfolgreich abgeschlossen!                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌────────────────────────┬────────────────────────────────┐   │
│  │ 📊 Übersicht          │  📈 Qualität                   │   │
│  ├────────────────────────┼────────────────────────────────┤   │
│  │                        │                                │   │
│  │  47 Schüler           │   🥇 Wunsch 1: 89 (63.1%)    │   │
│  │  3 Tage               │   🥈 Wunsch 2: 38 (27.0%)    │   │
│  │  12 Workshops         │   🥉 Wunsch 3: 12 (8.5%)     │   │
│  │  141 Zuteilungen      │   4️⃣  Wunsch 4: 2  (1.4%)     │   │
│  │                        │                                │   │
│  │                        │   Gesamtzufriedenheit: 92%    │   │
│  │                        │                                │   │
│  └────────────────────────┴────────────────────────────────┘   │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  💡 Interpretation                                       │   │
│  │                                                           │   │
│  │  ✓ Hervorragendes Ergebnis! 90.1% der Schüler haben     │   │
│  │    ihren Erst- oder Zweitwunsch bekommen.                │   │
│  │                                                           │   │
│  │  ✓ Alle Workshops sind gut ausgelastet (15-24           │   │
│  │    Teilnehmer)                                            │   │
│  │                                                           │   │
│  │  ℹ️ 2 Schüler haben ihren Viertwunsch erhalten, weil     │   │
│  │    ihre anderen Wünsche bereits ausgebucht waren.        │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  [📋 Zuteilungen]  [📊 Statistik]  [🎪 Workshops]       │  │
│  ├──────────────────────────────────────────────────────────┤  │
│  │                                                            │  │
│  │  Vorname   Nachname  Klasse  Tag 1        Tag 2    Tag 3 │  │
│  │  ─────────────────────────────────────────────────────── │  │
│  │  Anna      Müller    5a      Töpfern 🥇  Musik🥈  Sport │  │
│  │  Ben       Schmidt   5a      Sport 🥇    Kunst🥇  Koch  │  │
│  │  Clara     Weber     5b      Theater🥇   Kochen🥈  Foto │  │
│  │  ...                                                       │  │
│  │                                                            │  │
│  │                                 [Alle exportieren ▼]      │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                   │
│  [🔄 Neue Optimierung]           [💾 Als Excel speichern]      │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘

          [← Zurück]                              [Fertig]
```

---

## Expandable "How it Works" Section

**When collapsed:**
```
┌─────────────────────────────────────────────────────────────────┐
│  💡 Wie funktioniert die Optimierung?          [▼ Mehr erfahren] │
└─────────────────────────────────────────────────────────────────┘
```

**When expanded:**
```
┌─────────────────────────────────────────────────────────────────┐
│  💡 Wie funktioniert die Optimierung?          [▲ Einklappen]    │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  Dieses Tool nutzt einen mathematischen Optimierungsalgorithmus │
│  (Linear Programming), um die beste Zuteilung zu finden.        │
│                                                                   │
│  🎯 Das Ziel:                                                    │
│  Maximiere die Zufriedenheit aller Schüler, indem möglichst     │
│  viele ihre Erstwünsche bekommen.                                │
│                                                                   │
│  📐 So funktioniert es:                                          │
│                                                                   │
│  1️⃣  PUNKTE VERGEBEN                                             │
│     Jeder Wunsch bekommt Punkte:                                 │
│     • Wunsch 1: 10 Punkte  🥇                                   │
│     • Wunsch 2: 5 Punkte   🥈                                   │
│     • Wunsch 3: 2 Punkte   🥉                                   │
│     • Wunsch 4: 1 Punkt    4️⃣                                    │
│                                                                   │
│  2️⃣  REGELN BEACHTEN                                             │
│     • Jeder Schüler bekommt genau 1 Workshop pro Tag            │
│     • Kein Schüler bekommt denselben Workshop zweimal           │
│     • Kapazitätsgrenzen werden eingehalten                       │
│     • Optional: Klassenkameraden bleiben zusammen                │
│                                                                   │
│  3️⃣  BESTE LÖSUNG FINDEN                                         │
│     Der Computer testet Millionen Kombinationen und findet       │
│     die Zuteilung mit der höchsten Gesamtpunktzahl.             │
│                                                                   │
│  ✨ Beispiel:                                                     │
│  ┌──────────────────────────────────────────────────────┐       │
│  │  Anna wünscht sich: Töpfern > Musik > Sport > Kunst  │       │
│  │                                                        │       │
│  │  ✓ Tag 1: Töpfern (Wunsch 1) → 10 Punkte             │       │
│  │  ✓ Tag 2: Musik (Wunsch 2)   → 5 Punkte              │       │
│  │  ✓ Tag 3: Theater (nicht gewünscht) → 0 Punkte       │       │
│  │                                                        │       │
│  │  Annas Zufriedenheit: 15 von 17 möglichen Punkten    │       │
│  └──────────────────────────────────────────────────────┘       │
│                                                                   │
│  Das Gleiche passiert für alle 47 Schüler gleichzeitig.         │
│  Die Optimierung findet den besten Kompromiss für alle!          │
│                                                                   │
│  🔬 Technische Details (für Interessierte):                      │
│  [▼ Mehr anzeigen]                                               │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Help/Tooltip System

### Inline Tooltips (ⓘ icons)
Hover or click to show:

```
┌──────────────────────────────────────────┐
│  💡 Tooltip                              │
│  ────────────────────────────────────── │
│  Die Gewichtung bestimmt, wie stark     │
│  der Erstwunsch gegenüber den anderen   │
│  Wünschen bevorzugt wird.               │
│                                          │
│  Standard 10:5:2:1 bedeutet:            │
│  • Erstwunsch ist doppelt so wichtig    │
│    wie Zweitwunsch                       │
│  • Zweitwunsch ist 2,5× wichtiger als   │
│    Drittwunsch                           │
└──────────────────────────────────────────┘
```

### Context Validation

Show live feedback as users enter data:

```
Max. Teilnehmer: [5]  ⚠️ Sehr niedrig - einige Workshops
                      könnten nicht ausgelastet werden

Max. Teilnehmer: [25] ✓ Guter Wert für diese Schülerzahl

Max. Teilnehmer: [100] ⚠️ Sehr hoch - könnte zu großen
                       Gruppen führen
```

---

## Key UI Components & Patterns

### 1. Stepper Progress Bar
```
●━━━━━━━ ○────── ○────── ○────── ○
Active   Next     Future   Future  Future
```

### 2. Info Cards
```
┌─────────────────────────────────┐
│  🎯 Title                        │
├─────────────────────────────────┤
│  Content here                   │
│  • Bullet points                │
│  • Visual hierarchy             │
│                                  │
│              [Action Button]    │
└─────────────────────────────────┘
```

### 3. Validation States
- ✓ Success (green)
- ⚠️ Warning (orange)
- ✗ Error (red)
- ℹ️ Info (blue)

### 4. Expandable Sections
```
[▼ Show more]  → collapsed
[▲ Show less]  → expanded
```

---

## Color Palette (Modern & Accessible)

**Primary Actions:** Blue (#0066CC)
**Success:** Green (#10B981)
**Warning:** Orange (#F59E0B)
**Error:** Red (#EF4444)
**Info:** Light Blue (#3B82F6)
**Neutral:** Gray scale (#1F2937 to #F9FAFB)

**Accessibility:** WCAG 2.1 AA compliant contrast ratios

---

## Typography Hierarchy

**H1 (Title):** 28px, Bold
**H2 (Section):** 18px, Bold
**H3 (Subsection):** 14px, Bold
**Body:** 11px, Regular
**Caption:** 9px, Regular
**Monospace (Data):** 10px, Consolas

---

## Interaction Patterns

### Keyboard Navigation
- Tab to navigate between fields
- Enter to submit/continue
- Esc to cancel/go back
- Space to toggle checkboxes/radios

### Mouse/Touch
- Large click targets (min 44×44px)
- Hover states for interactive elements
- Drag & drop with visual feedback
- Tooltips on hover (desktop) or tap (mobile)

---

## Mobile/Responsive Considerations

While this is a desktop app, responsive principles apply:
- Minimum window size: 900×700px
- Content should reflow gracefully
- Scrollable content areas
- No horizontal scrolling

---

## Accessibility Features

1. **Screen Reader Support**
   - Proper ARIA labels
   - Semantic HTML structure
   - Alt text for icons

2. **Keyboard Navigation**
   - All functions accessible via keyboard
   - Visible focus indicators
   - Logical tab order

3. **Visual Accessibility**
   - High contrast mode support
   - Scalable fonts
   - Color not the only indicator (use icons + text)

4. **Clear Language**
   - Simple German
   - Avoid jargon
   - Explain technical terms

---

## Next Steps

1. Get feedback on this design
2. Create interactive prototype/mockup
3. Implement step-by-step with user testing
4. Iterate based on teacher feedback
