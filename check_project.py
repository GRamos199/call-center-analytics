"""
Project structure and health check script.
Verifies all required files and modules are in place.
"""
import os
from pathlib import Path


def check_structure():
    """Check project structure and file integrity."""
    
    root = Path(__file__).parent / "analytics"
    
    required_dirs = [
        "classes",
        "utils",
        "data",
        "reporting",
        "reporting/monthly",
        "reporting/weekly",
        ".streamlit",
    ]
    
    required_files = {
        "main.py": root,
        "classes/__init__.py": root,
        "classes/base_tab.py": root,
        "classes/monthly_tab.py": root,
        "classes/weekly_tab.py": root,
        "utils/__init__.py": root,
        "utils/data_loader.py": root,
        "utils/metric_loader.py": root,
        "utils/icons_service.py": root,
        "utils/data_generator.py": root,
        "data/calls.csv": root,
        "data/agents.csv": root,
        "data/costs.csv": root,
        ".streamlit/config.toml": root,
    }
    
    errors = []
    
    # Check directories
    print("\n📁 Checking directories...")
    for dir_path in required_dirs:
        full_path = root / dir_path
        if full_path.exists():
            print(f"  ✅ {dir_path}")
        else:
            print(f"  ❌ {dir_path} - MISSING")
            errors.append(f"Missing directory: {dir_path}")
    
    # Check files
    print("\n📄 Checking files...")
    for file_name, base_path in required_files.items():
        full_path = base_path / file_name
        if full_path.exists():
            size = full_path.stat().st_size
            print(f"  ✅ {file_name} ({size} bytes)")
        else:
            print(f"  ❌ {file_name} - MISSING")
            errors.append(f"Missing file: {file_name}")
    
    # Check Python files can be imported
    print("\n🐍 Checking Python modules...")
    import sys
    sys.path.insert(0, str(root))
    
    modules_to_check = [
        ("utils.icons_service", "IconsService"),
        ("utils.data_loader", "DataLoader"),
        ("utils.metric_loader", "MetricLoader"),
        ("classes.base_tab", "BaseTab"),
        ("classes.monthly_tab", "MonthlyTab"),
        ("classes.weekly_tab", "WeeklyTab"),
    ]
    
    for module_name, class_name in modules_to_check:
        try:
            module = __import__(module_name, fromlist=[class_name])
            getattr(module, class_name)
            print(f"  ✅ {module_name}.{class_name}")
        except Exception as e:
            print(f"  ❌ {module_name}.{class_name} - {str(e)}")
            errors.append(f"Import error: {module_name}.{class_name}")
    
    # Summary
    print("\n" + "="*50)
    if errors:
        print(f"❌ Found {len(errors)} issues:")
        for error in errors:
            print(f"   - {error}")
        return False
    else:
        print("✅ All checks passed!")
        print("🚀 Project is ready to run!")
        return True


if __name__ == "__main__":
    success = check_structure()
    exit(0 if success else 1)
