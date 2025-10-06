"""Helper functions for the workshop allocation tool."""
from typing import Dict, List
from pathlib import Path


def format_percentage(value: float, decimals: int = 1) -> str:
    """Format a float as percentage string.

    Args:
        value: Value between 0 and 100
        decimals: Number of decimal places

    Returns:
        Formatted string like "85.5%"
    """
    return f"{value:.{decimals}f}%"


def format_student_count(count: int, singular: str = "Schüler", plural: str = "Schüler") -> str:
    """Format student count with proper singular/plural.

    Args:
        count: Number of students
        singular: Singular form
        plural: Plural form

    Returns:
        Formatted string like "1 Schüler" or "5 Schüler"
    """
    word = singular if count == 1 else plural
    return f"{count} {word}"


def format_class_list(classes: List[str]) -> str:
    """Format a list of class names.

    Args:
        classes: List of class names

    Returns:
        Comma-separated string
    """
    return ", ".join(sorted(set(classes)))


def truncate_string(text: str, max_length: int = 50, suffix: str = "...") -> str:
    """Truncate a string to maximum length.

    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated

    Returns:
        Truncated string
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def get_file_size_mb(file_path: str) -> float:
    """Get file size in megabytes.

    Args:
        file_path: Path to file

    Returns:
        Size in MB
    """
    try:
        size_bytes = Path(file_path).stat().st_size
        return size_bytes / (1024 * 1024)
    except:
        return 0.0


def sanitize_filename(filename: str) -> str:
    """Sanitize a filename by removing invalid characters.

    Args:
        filename: Original filename

    Returns:
        Sanitized filename
    """
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename


def format_time_seconds(seconds: float) -> str:
    """Format time in seconds to human-readable string.

    Args:
        seconds: Time in seconds

    Returns:
        Formatted string like "2.5s" or "1m 30s"
    """
    if seconds < 60:
        return f"{seconds:.1f}s"

    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes}m {secs}s"


def get_quality_label_for_rate(rate: float) -> str:
    """Get quality label for satisfaction rate.

    Args:
        rate: Satisfaction percentage (0-100)

    Returns:
        Quality label string
    """
    if rate >= 90:
        return "Hervorragend"
    elif rate >= 80:
        return "Sehr gut"
    elif rate >= 70:
        return "Gut"
    elif rate >= 60:
        return "Akzeptabel"
    else:
        return "Verbesserungswürdig"


def count_by_class(students: List) -> Dict[str, int]:
    """Count students by class.

    Args:
        students: List of student objects/dicts

    Returns:
        Dictionary mapping class name to count
    """
    counts = {}
    for student in students:
        klasse = getattr(student, 'klasse', None) or student.get('klasse', 'Unbekannt')
        counts[klasse] = counts.get(klasse, 0) + 1
    return counts


def create_summary_text(
    num_students: int,
    num_classes: int,
    num_workshops: int,
    num_days: int
) -> str:
    """Create a summary text for data import.

    Args:
        num_students: Number of students
        num_classes: Number of classes
        num_workshops: Number of workshops
        num_days: Number of days

    Returns:
        Formatted summary string
    """
    return (
        f"{num_students} Schüler aus {num_classes} Klassen\n"
        f"{num_workshops} Workshops über {num_days} Tage"
    )


def validate_excel_extension(filename: str) -> bool:
    """Check if filename has valid Excel extension.

    Args:
        filename: Filename to check

    Returns:
        True if valid Excel file
    """
    valid_extensions = ['.xlsx', '.xls']
    return any(filename.lower().endswith(ext) for ext in valid_extensions)


def format_warning_list(warnings: List[str], max_show: int = 5) -> str:
    """Format a list of warnings for display.

    Args:
        warnings: List of warning messages
        max_show: Maximum number to show

    Returns:
        Formatted warning string
    """
    if not warnings:
        return ""

    shown = warnings[:max_show]
    text = "\n".join(f"• {w}" for w in shown)

    if len(warnings) > max_show:
        remaining = len(warnings) - max_show
        text += f"\n... und {remaining} weitere"

    return text
