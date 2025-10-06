# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a desktop application for optimal workshop allocation for students. The tool reads student data from Excel files, runs an optimization algorithm to assign students to workshops based on their preferences, and exports results back to Excel.

**Target User**: Non-technical teacher who currently does everything manually in Excel. The application must be self-explanatory and fault-tolerant.

**Key Constraint**: All processing must run locally (DSGVO/GDPR compliant - no cloud/internet).

## Technology Stack

- **Language**: Python
- **GUI Framework**: tkinter or PyQt (choose based on ease of creating standalone .exe)
- **Optimization Engine**: pulp or ortools
- **Excel Handling**: pandas + openpyxl
- **Packaging**: PyInstaller (must create standalone .exe)

## Core Functionality

### Input Format
Excel file with student data containing:
- Vorname (First name)
- Nachname (Last name)
- Klasse (Class)
- Wunsch 1-4 (Wishes/preferences 1-4)

### Configurable Parameters (set BEFORE calculation)
- Maximum participants per workshop (number or "unlimited")
- Should students from the same class stay together? (Yes/No/Doesn't matter)
- Weighting of wishes (e.g., Wish 1: 10 points, Wish 2: 5 points, etc.)
- Number of days (default: 3)
- Number of workshops (default: 12)

### Output Format
Excel file with three components:
1. **Student assignments**: All student data + assigned workshops (Day 1, Day 2, Day 3)
2. **Workshop overview**: Which workshop on which day, with participant list
3. **Statistics sheet**: Distribution of how many students got their 1st/2nd/3rd/4th choice, workshop capacity status

## GUI Requirements (German language)

The interface must be simple and intuitive:
- File upload via drag & drop or file dialog
- Parameter input fields BEFORE calculation
- Progress indicator during calculation
- Results overview showing:
  - How many students received their 1st/2nd/3rd/4th choice
  - Which workshops are full/empty
  - List of conflicts/problems if any
- "Save as" dialog for export

## Architecture Notes

When implementing, follow this sequence:
1. Create basic GUI structure
2. Implement Excel import with preview and validation
3. Build optimization algorithm
4. Add export functionality
5. Test with sample data

### Important Design Considerations
- **Validation**: Warn if wishes are missing or inconsistent
- **Error handling**: Must be fault-tolerant for non-technical users
- **Progress feedback**: Show clear progress during potentially long calculations
- **Parameter persistence**: Consider saving/loading parameter settings (nice-to-have)
- **Manual adjustment mode**: Allow manual tweaking after automatic assignment (nice-to-have)

## Development Workflow

Since this is a new project with only a requirements document (brief.md), start by creating the basic project structure with appropriate modules for GUI, data handling, optimization, and export.
