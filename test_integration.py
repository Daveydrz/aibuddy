#!/usr/bin/env python3
"""
Test that main.py can import and run the optimization functions
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that we can import the functions from main.py"""
    print("🚀 Testing imports from main.py...")
    
    try:
        # Try to import the optimization functions
        from main import is_simple_question, is_user_already_identified, has_name_introduction_patterns
        print("✅ Successfully imported optimization functions")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Other error: {e}")
        return False

def test_functions():
    """Test that the functions work correctly"""
    print("\n🚀 Testing function behavior...")
    
    try:
        from main import is_simple_question, is_user_already_identified, has_name_introduction_patterns
        
        # Test the critical case
        critical_text = "who are you today?"
        test_user = "Daveydrz"
        
        is_simple = is_simple_question(critical_text)
        is_identified = is_user_already_identified(test_user)
        has_patterns = has_name_introduction_patterns(critical_text)
        
        print(f"Testing: '{critical_text}' with user '{test_user}'")
        print(f"  is_simple_question: {is_simple}")
        print(f"  is_user_already_identified: {is_identified}")
        print(f"  has_name_introduction_patterns: {has_patterns}")
        
        # Expected: True, True, False
        if is_simple and is_identified and not has_patterns:
            print("✅ Functions work correctly - will use fast path!")
            return True
        else:
            print("❌ Functions not working as expected")
            return False
            
    except Exception as e:
        print(f"❌ Error testing functions: {e}")
        return False

def test_config():
    """Test that config can be imported"""
    print("\n🚀 Testing config import...")
    
    try:
        from config import FAST_PATH_ROUTING, SIMPLE_QUESTION_PATTERNS
        print(f"✅ FAST_PATH_ROUTING: {FAST_PATH_ROUTING}")
        print(f"✅ SIMPLE_QUESTION_PATTERNS: {len(SIMPLE_QUESTION_PATTERNS)} patterns")
        return True
    except ImportError as e:
        print(f"❌ Config import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Config error: {e}")
        return False

def main():
    """Run all tests"""
    print("🎯 MAIN.PY OPTIMIZATION INTEGRATION TEST")
    print("=" * 60)
    
    imports_ok = test_imports()
    functions_ok = test_functions() if imports_ok else False
    config_ok = test_config()
    
    print("\n" + "=" * 60)
    if imports_ok and functions_ok and config_ok:
        print("🎉 ALL INTEGRATION TESTS PASSED!")
        print("✅ main.py optimization functions are working")
        print("✅ Config settings are available")
        print("✅ Ready for end-to-end testing")
        print("\n💡 Next step: Test actual performance in full application")
    else:
        print("❌ INTEGRATION TESTS FAILED")
        if not imports_ok:
            print("❌ Cannot import optimization functions")
        if not functions_ok:
            print("❌ Functions not working correctly")
        if not config_ok:
            print("❌ Config settings not available")

if __name__ == "__main__":
    main()