#!/usr/bin/env python3
"""Test script to verify all imports work correctly."""

print("Testing imports...")

try:
    print("  - models...", end=" ")
    from models import Student
    print("✓")

    print("  - services.data_service...", end=" ")
    from services.data_service import DataService
    print("✓")

    print("  - services.optimization_service...", end=" ")
    from services.optimization_service import OptimizationService
    print("✓")

    print("  - services.config_service...", end=" ")
    from services.config_service import ConfigService
    print("✓")

    print("  - services.validation_service...", end=" ")
    from services.validation_service import ValidationService
    print("✓")

    print("  - controllers...", end=" ")
    from controllers import AppController
    print("✓")

    print("  - views...", end=" ")
    from views import MainWindow
    print("✓")

    print("\n✅ All imports successful!")

except ImportError as e:
    print(f"\n❌ Import error: {e}")
    exit(1)
