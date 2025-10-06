"""Constants for the workshop allocation tool."""

# Application metadata
APP_NAME = "Workshop-Zuteilungs-Tool"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Optimale Zuordnung von Schülern zu Workshops"

# Window settings
DEFAULT_WINDOW_WIDTH = 1100
DEFAULT_WINDOW_HEIGHT = 800
MIN_WINDOW_WIDTH = 900
MIN_WINDOW_HEIGHT = 700

# Wizard steps
STEP_IMPORT = 0
STEP_PARAMETERS = 1
STEP_REVIEW = 2
STEP_OPTIMIZE = 3
STEP_RESULTS = 4

STEP_NAMES = [
    "Daten",
    "Parameter",
    "Prüfen",
    "Optimieren",
    "Ergebnis"
]

# Icons/Emojis
ICON_IMPORT = "📥"
ICON_SETTINGS = "⚙️"
ICON_ROCKET = "🚀"
ICON_CHART = "📊"
ICON_FILE = "📁"
ICON_CHECK = "✅"
ICON_WARNING = "⚠️"
ICON_ERROR = "❌"
ICON_INFO = "ℹ️"
ICON_CLOCK = "⏱️"
ICON_LIGHTNING = "⚡"
ICON_CALENDAR = "📅"
ICON_PEOPLE = "👥"
ICON_SCHOOL = "🏫"
ICON_STAR = "⭐"
ICON_WORKSHOP = "🎪"
ICON_LOCK = "🔒"
ICON_SAVE = "💾"
ICON_LIGHTBULB = "💡"
ICON_TROPHY = "🏆"

# Medal icons for wish ranks
WISH_ICONS = {
    1: "🥇",
    2: "🥈",
    3: "🥉",
    4: "4️⃣"
}

# Color scheme (for reference)
COLOR_PRIMARY = "#0066CC"
COLOR_SUCCESS = "#10B981"
COLOR_WARNING = "#F59E0B"
COLOR_ERROR = "#EF4444"
COLOR_INFO = "#3B82F6"

# Theme names
THEMES = [
    "cosmo",     # Light, modern
    "darkly",    # Dark mode
    "flatly",    # Clean & minimal
    "superhero", # Dark with color
    "litera",    # Readable
    "cyborg"     # Dark tech
]

# Default configuration values
DEFAULT_NUM_DAYS = 3
DEFAULT_NUM_WORKSHOPS = 12
DEFAULT_MAX_PARTICIPANTS = None  # Unlimited
DEFAULT_KEEP_CLASSES_TOGETHER = "egal"
DEFAULT_WISH_WEIGHTS = {
    'wunsch1': 10,
    'wunsch2': 5,
    'wunsch3': 2,
    'wunsch4': 1
}

# Excel column names
REQUIRED_COLUMNS = ['vorname', 'nachname', 'klasse', 'wunsch1', 'wunsch2', 'wunsch3', 'wunsch4']

# Validation thresholds
MIN_PARTICIPANTS_WARNING = 5
MAX_PARTICIPANTS_WARNING = 50
MIN_WORKSHOP_DEMAND = 3  # Warn if fewer students want a workshop
HIGH_UTILIZATION_THRESHOLD = 90  # Percentage

# Messages
MSG_NO_FILE = "📄 Keine Datei ausgewählt"
MSG_FILE_LOADED = "✅ Geladen: {}"
MSG_IMPORT_FAILED = "❌ Import fehlgeschlagen"
MSG_OPTIMIZING = "⏳ Optimierung läuft..."
MSG_OPTIMIZATION_COMPLETE = "✓ Optimierung abgeschlossen"
MSG_OPTIMIZATION_FAILED = "❌ Optimierung fehlgeschlagen"
MSG_DSGVO = "🔒 DSGVO-konform | Alle Daten bleiben lokal"

# Tooltips
TOOLTIP_NUM_DAYS = "Jeder Schüler besucht pro Tag einen Workshop"
TOOLTIP_MAX_PARTICIPANTS = "Empfehlung: Betreuer-Schüler-Verhältnis 1:12-15"
TOOLTIP_KEEP_CLASSES = {
    'ja': "Soziale Bindungen erhalten",
    'nein': "Neue Kontakte fördern",
    'egal': "Nur Präferenzen zählen"
}
TOOLTIP_WISH_WEIGHTS = (
    "Die Optimierung versucht, die Gesamtpunktzahl zu maximieren. "
    "Höhere Gewichte = stärkerer Fokus auf Erstwünsche"
)

# Quality labels based on satisfaction rate
QUALITY_LABELS = {
    90: "Hervorragend",
    80: "Sehr gut",
    70: "Gut",
    60: "Akzeptabel",
    0: "Verbesserungswürdig"
}

# File filters for dialogs
EXCEL_FILE_TYPES = [
    ("Excel-Dateien", "*.xlsx *.xls"),
    ("Alle Dateien", "*.*")
]
