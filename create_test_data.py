"""
Script to generate test Excel files with realistic student data.
Run this to create sample data for testing.
"""
import pandas as pd
import random
from pathlib import Path


def generate_test_excel(filename: str, num_students: int = 30):
    """
    Generate a test Excel file with student data.

    Args:
        filename: Output filename
        num_students: Number of students to generate
    """

    # German first names
    first_names = [
        'Anna', 'Ben', 'Clara', 'David', 'Emma', 'Felix', 'Greta', 'Hannah',
        'Ida', 'Jakob', 'Klara', 'Leon', 'Mia', 'Noah', 'Olivia', 'Paul',
        'Sophia', 'Tim', 'Lena', 'Max', 'Laura', 'Lukas', 'Marie', 'Jonas',
        'Sophie', 'Finn', 'Lina', 'Elias', 'Emilia', 'Luis', 'Charlotte', 'Anton'
    ]

    # German last names
    last_names = [
        'Müller', 'Schmidt', 'Schneider', 'Fischer', 'Weber', 'Meyer',
        'Wagner', 'Becker', 'Schulz', 'Hoffmann', 'Koch', 'Bauer',
        'Richter', 'Klein', 'Wolf', 'Schröder', 'Neumann', 'Schwarz',
        'Zimmermann', 'Braun', 'Hofmann', 'Hartmann', 'Lange', 'Werner'
    ]

    # Workshop options
    workshops = [
        'Töpfern', 'Musik & Band', 'Sport & Bewegung', 'Kunst & Malerei',
        'Theater', 'Programmieren', 'Kochen & Backen', 'Nähen & Textil',
        'Fotografie', 'Experimente', 'Tanz', 'Holzwerken'
    ]

    # Classes
    classes = ['5a', '5b', '5c', '6a', '6b', '6c', '7a', '7b']

    # Generate students
    students = []
    for i in range(num_students):
        # Random student
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        klasse = random.choice(classes)

        # Generate wishes (random but unique)
        wishes = random.sample(workshops, 4)

        students.append({
            'vorname': first_name,
            'nachname': last_name,
            'klasse': klasse,
            'wunsch1': wishes[0],
            'wunsch2': wishes[1],
            'wunsch3': wishes[2],
            'wunsch4': wishes[3]
        })

    # Sort by class and last name
    students.sort(key=lambda x: (x['klasse'], x['nachname']))

    # Create DataFrame and save
    df = pd.DataFrame(students)
    df.to_excel(filename, index=False)

    print(f"✓ Created {filename} with {num_students} students")
    print(f"  Classes: {', '.join(sorted(set(s['klasse'] for s in students)))}")
    print(f"  Workshops: {len(workshops)}")


def generate_edge_case_files():
    """Generate Excel files for testing edge cases."""

    # 1. Small dataset (5 students)
    small_data = {
        'vorname': ['Anna', 'Ben', 'Clara', 'David', 'Emma'],
        'nachname': ['Schmidt', 'Müller', 'Weber', 'Fischer', 'Wagner'],
        'klasse': ['5a', '5a', '5b', '5b', '5a'],
        'wunsch1': ['Töpfern', 'Sport', 'Musik', 'Töpfern', 'Kunst'],
        'wunsch2': ['Musik', 'Musik', 'Kunst', 'Sport', 'Töpfern'],
        'wunsch3': ['Sport', 'Töpfern', 'Töpfern', 'Musik', 'Musik'],
        'wunsch4': ['Kunst', 'Kunst', 'Sport', 'Kunst', 'Sport']
    }
    pd.DataFrame(small_data).to_excel('test_small.xlsx', index=False)
    print("✓ Created test_small.xlsx (5 students, 2 classes)")

    # 2. Missing wishes (incomplete data)
    incomplete_data = {
        'vorname': ['Anna', 'Ben', 'Clara'],
        'nachname': ['Schmidt', 'Müller', 'Weber'],
        'klasse': ['5a', '5a', '5b'],
        'wunsch1': ['Töpfern', 'Sport', 'Musik'],
        'wunsch2': ['Musik', None, 'Kunst'],  # Ben has missing wish
        'wunsch3': ['Sport', 'Töpfern', None],  # Clara has missing wish
        'wunsch4': [None, 'Kunst', 'Sport']  # Anna has missing wish
    }
    pd.DataFrame(incomplete_data).to_excel('test_incomplete.xlsx', index=False)
    print("✓ Created test_incomplete.xlsx (missing wishes)")

    # 3. Duplicate wishes (validation test)
    duplicate_data = {
        'vorname': ['Anna', 'Ben'],
        'nachname': ['Schmidt', 'Müller'],
        'klasse': ['5a', '5a'],
        'wunsch1': ['Töpfern', 'Sport'],
        'wunsch2': ['Töpfern', 'Musik'],  # Anna has duplicate
        'wunsch3': ['Musik', 'Sport'],    # Ben has duplicate
        'wunsch4': ['Kunst', 'Sport']     # Ben has another duplicate
    }
    pd.DataFrame(duplicate_data).to_excel('test_duplicates.xlsx', index=False)
    print("✓ Created test_duplicates.xlsx (duplicate wishes)")

    # 4. Large dataset (100 students)
    generate_test_excel('test_large.xlsx', num_students=100)

    # 5. Very popular workshops (stress test)
    popular_data = []
    for i in range(20):
        popular_data.append({
            'vorname': f'Student{i+1}',
            'nachname': f'Test{i+1}',
            'klasse': '5a',
            'wunsch1': 'Töpfern',  # Everyone wants this
            'wunsch2': 'Musik',
            'wunsch3': 'Sport',
            'wunsch4': 'Kunst'
        })
    pd.DataFrame(popular_data).to_excel('test_popular.xlsx', index=False)
    print("✓ Created test_popular.xlsx (20 students all want same workshop)")


def main():
    """Generate all test files."""
    print("Generating test Excel files...")
    print()

    # Main test file
    generate_test_excel('example_students.xlsx', num_students=30)
    print()

    # Edge case files
    generate_edge_case_files()
    print()
    print("All test files created successfully!")
    print()
    print("Files created:")
    for file in Path('.').glob('*.xlsx'):
        if file.stem.startswith(('example_', 'test_')):
            print(f"  - {file.name}")


if __name__ == "__main__":
    main()
