# validate.py
import os
import sys

print("="*80)
print("DARUKAA CHATBOT - ENVIRONMENT VALIDATION")
print("="*80 + "\n")

errors = []
warnings = []

# CHECK 1: Python version
print("CHECK 1: Python Version")
python_version = sys.version_info
if python_version.major >= 3 and python_version.minor >= 8:
    print(f"  ✓ Python {python_version.major}.{python_version.minor} (OK)")
else:
    errors.append(f"Python 3.8+ required, you have {python_version.major}.{python_version.minor}")
print()

# CHECK 2: .env file
print("CHECK 2: .env File")
if os.path.exists('.env'):
    print("  ✓ .env file found")
    try:
        with open('.env', 'r') as f:
            content = f.read()
            if 'OPENAI_API_KEY' in content:
                if content.split('=')[1].strip().startswith('sk-'):
                    print("  ✓ OPENAI_API_KEY format looks correct (sk-xxx...)")
                else:
                    errors.append("OPENAI_API_KEY doesn't start with 'sk-'")
            else:
                errors.append(".env exists but OPENAI_API_KEY not found")
    except Exception as e:
        errors.append(f"Error reading .env: {e}")
else:
    errors.append(".env file NOT FOUND - create it with: notepad .env")
print()

# CHECK 3: Required modules
print("CHECK 3: Python Modules")
required_modules = [
    'langchain',
    'openai',
    'flask',
    'flask_cors',
    'dotenv'
]

missing_modules = []
for module in required_modules:
    try:
        __import__(module)
        print(f"  ✓ {module}")
    except ImportError:
        print(f"  ✗ {module} - NOT INSTALLED")
        missing_modules.append(module)

if missing_modules:
    errors.append(f"Missing modules: {', '.join(missing_modules)}. Run: pip install {' '.join(missing_modules)}")
print()

# CHECK 4: Project files
print("CHECK 4: Project Files")
required_files = [
    'knowledge_base.py',
    'recommendation_engine.py',
    'chatbot.py',
    'app.py'
]

for file in required_files:
    if os.path.exists(file):
        print(f"  ✓ {file}")
    else:
        print(f"  ✗ {file} - MISSING")
        errors.append(f"{file} not found")
print()

# RESULTS
print("="*80)
if errors:
    print("❌ VALIDATION FAILED - FIX THESE ERRORS:\n")
    for i, error in enumerate(errors, 1):
        print(f"  {i}. {error}\n")
    sys.exit(1)
elif warnings:
    print("⚠️  VALIDATION PASSED WITH WARNINGS:\n")
    for warning in warnings:
        print(f"  - {warning}\n")
else:
    print("✅ ALL CHECKS PASSED - READY TO RUN!\n")
    print("Next step: python app.py")
    print("Then test in another PowerShell window")
print("="*80)