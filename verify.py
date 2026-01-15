"""
Quick Test Script
=================
Run this to quickly verify all functionality before submission.
"""

import sys
import os

print("=" * 60)
print("TalentScout AI - Quick Verification Test")
print("=" * 60)
print()

# Test 1: Import all modules
print("Test 1: Checking imports...")
try:
    import streamlit
    import huggingface_hub
    from dotenv import load_dotenv
    import chatbot_engine
    import data_handler
    import utils
    print("✅ All modules imported successfully")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Run: pip install -r requirements.txt")
    sys.exit(1)

# Test 2: Check environment file
print("\nTest 2: Checking environment file...")
load_dotenv()
api_key = os.getenv('HUGGINGFACE_API_KEY')
if api_key and api_key != 'your_huggingface_api_key_here':
    print("✅ API key is configured")
elif not api_key:
    print("⚠️  .env file not found")
    print("Run: copy .env.example .env")
else:
    print("⚠️  API key not configured (still using placeholder)")
    print("Edit .env and add your actual API key")

# Test 3: Test utility functions
print("\nTest 3: Testing utility functions...")
try:
    from utils import validate_email, validate_phone, sanitize_input
    
    # Email validation
    assert validate_email("test@example.com") == True
    assert validate_email("invalid.email") == False
    
    # Phone validation
    assert validate_phone("123-456-7890") == True
    assert validate_phone("abc") == False
    
    # Input sanitization
    sanitized = sanitize_input("<script>alert('xss')</script>")
    assert "<script>" not in sanitized
    
    print("✅ Utility functions working correctly")
except AssertionError:
    print("❌ Utility function tests failed")
except Exception as e:
    print(f"❌ Error testing utilities: {e}")

# Test 4: Test data handler
print("\nTest 4: Testing data handler...")
try:
    from data_handler import CandidateDataHandler
    
    # Create instance
    handler = CandidateDataHandler(data_dir="test_temp_data")
    
    # Test save
    test_data = {
        "name": "Test User",
        "email": "test@example.com",
        "phone": "1234567890",
        "experience": "5 years",
        "position": "Test Position",
        "location": "Test Location",
        "tech_stack": ["Python", "JavaScript"]
    }
    
    candidate_id = handler.save_candidate_data(test_data)
    assert candidate_id is not None
    
    # Test retrieve
    retrieved = handler.get_candidate_data(candidate_id)
    assert retrieved is not None
    assert retrieved['email'] == "test@example.com"
    
    # Cleanup
    import shutil
    if os.path.exists("test_temp_data"):
        shutil.rmtree("test_temp_data")
    
    print("✅ Data handler working correctly")
except Exception as e:
    print(f"❌ Data handler test failed: {e}")

# Test 5: Test chatbot engine
print("\nTest 5: Testing chatbot engine...")
try:
    from chatbot_engine import HiringAssistant
    
    chatbot = HiringAssistant()
    
    # Test greeting
    greeting = chatbot.generate_greeting()
    assert "TalentScout" in greeting
    
    # Test email extraction
    email = chatbot.extract_email("My email is john@example.com")
    assert email == "john@example.com"
    
    # Test phone extraction
    phone = chatbot.extract_phone("Call me at 123-456-7890")
    assert phone is not None
    
    # Test experience extraction
    exp = chatbot.extract_years_experience("5 years")
    assert exp == "5"
    
    # Test tech categorization
    categorized = chatbot.categorize_tech_stack(["Python", "Django", "PostgreSQL"])
    assert "Python" in categorized['languages']
    
    print("✅ Chatbot engine working correctly")
except Exception as e:
    print(f"❌ Chatbot engine test failed: {e}")

# Test 6: Check required files
print("\nTest 6: Checking required files...")
required_files = [
    'app.py',
    'chatbot_engine.py',
    'data_handler.py',
    'utils.py',
    'requirements.txt',
    '.env.example',
    '.gitignore',
    'README.md',
    'LICENSE'
]

missing_files = []
for file in required_files:
    if not os.path.exists(file):
        missing_files.append(file)

if missing_files:
    print(f"⚠️  Missing files: {', '.join(missing_files)}")
else:
    print("✅ All required files present")

# Test 7: Check documentation
print("\nTest 7: Checking documentation...")
doc_files = [
    'README.md',
    'QUICKSTART.md',
    'DEPLOYMENT.md',
    'API_KEY_GUIDE.md',
    'DEMO_SCRIPT.md',
    'PROJECT_SUMMARY.md',
    'SUBMISSION_CHECKLIST.md'
]

present_docs = [f for f in doc_files if os.path.exists(f)]
print(f"✅ Found {len(present_docs)}/{len(doc_files)} documentation files")

# Test 8: Check .gitignore
print("\nTest 8: Verifying .gitignore...")
if os.path.exists('.gitignore'):
    with open('.gitignore', 'r') as f:
        gitignore_content = f.read()
    
    important_entries = ['.env', 'candidate_data/', '__pycache__']
    missing_entries = [e for e in important_entries if e not in gitignore_content]
    
    if missing_entries:
        print(f"⚠️  .gitignore missing: {', '.join(missing_entries)}")
    else:
        print("✅ .gitignore properly configured")
else:
    print("❌ .gitignore not found")

# Summary
print("\n" + "=" * 60)
print("VERIFICATION SUMMARY")
print("=" * 60)
print()
print("If all tests show ✅, you're ready to:")
print("1. Record your demo video")
print("2. Create GitHub repository")
print("3. Push code to GitHub")
print("4. Submit to career portal")
print()
print("If any tests show ❌ or ⚠️, fix those issues first.")
print()
print("Good luck! 🚀")
print("=" * 60)
