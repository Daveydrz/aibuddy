#!/usr/bin/env python3
"""
Test current performance issue - understand what's happening
"""

import time
import sys
import os

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_simple_question_fast_path():
    """Test if the simple question 'who are you today?' uses fast path"""
    print("🚀 Testing simple question fast path...")
    
    try:
        # Import the functions from main.py
        from main import is_simple_question, is_user_already_identified, has_name_introduction_patterns
        
        test_question = "who are you today?"
        test_user = "Daveydrz"
        
        print(f"Testing question: '{test_question}'")
        print(f"Testing user: '{test_user}'")
        
        # Test each optimization function
        is_simple = is_simple_question(test_question)
        print(f"✅ is_simple_question('{test_question}') = {is_simple}")
        
        is_identified = is_user_already_identified(test_user)
        print(f"✅ is_user_already_identified('{test_user}') = {is_identified}")
        
        has_name_patterns = has_name_introduction_patterns(test_question)
        print(f"✅ has_name_introduction_patterns('{test_question}') = {has_name_patterns}")
        
        # Check if fast path should work
        if is_simple and is_identified and not has_name_patterns:
            print("🎉 FAST PATH SHOULD WORK!")
            print("  ✅ Question is simple")
            print("  ✅ User is identified") 
            print("  ✅ No name patterns to process")
            print("  🚀 Expected: 2-3 second response")
        else:
            print("❌ FAST PATH WILL NOT WORK")
            if not is_simple:
                print("  ❌ Question not detected as simple")
            if not is_identified:
                print("  ❌ User not identified")
            if has_name_patterns:
                print("  ❌ Name patterns detected (unexpected)")
        
        return is_simple and is_identified and not has_name_patterns
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_direct_response_functions():
    """Test if direct response functions work"""
    print("\n🚀 Testing direct response functions...")
    
    try:
        from main import is_direct_time_question, is_direct_location_question, is_direct_date_question
        
        test_cases = [
            ("who are you today?", "should NOT be direct"),
            ("what time is it?", "should be direct time"),
            ("where are you?", "should be direct location"), 
            ("what's the date?", "should be direct date")
        ]
        
        for question, expected in test_cases:
            is_time = is_direct_time_question(question)
            is_location = is_direct_location_question(question)
            is_date = is_direct_date_question(question)
            
            print(f"'{question}' ({expected}):")
            print(f"  Time: {is_time}, Location: {is_location}, Date: {is_date}")
            
            if "time" in expected and is_time:
                print("  ✅ Correctly detected as time question")
            elif "location" in expected and is_location:
                print("  ✅ Correctly detected as location question")
            elif "date" in expected and is_date:
                print("  ✅ Correctly detected as date question")
            elif "NOT" in expected and not (is_time or is_location or is_date):
                print("  ✅ Correctly NOT detected as direct question")
            else:
                print("  ❌ Detection failed")
                
    except ImportError as e:
        print(f"❌ Import error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

def trace_handle_streaming_response():
    """Try to understand what handle_streaming_response does"""
    print("\n🚀 Analyzing handle_streaming_response flow...")
    
    try:
        # We can't easily call handle_streaming_response without full setup
        # But we can check if the optimizations exist
        from main import handle_streaming_response
        print("✅ handle_streaming_response function exists")
        
        # Check the source to see if optimizations are present
        import inspect
        source = inspect.getsource(handle_streaming_response)
        
        # Look for optimization keywords
        optimizations_found = []
        if "is_simple_question" in source:
            optimizations_found.append("Simple question detection")
        if "is_user_already_identified" in source:
            optimizations_found.append("User identification check")
        if "has_name_introduction_patterns" in source:
            optimizations_found.append("Name pattern detection")
        if "FAST" in source:
            optimizations_found.append("Fast path logic")
            
        if optimizations_found:
            print("✅ Optimizations found in handle_streaming_response:")
            for opt in optimizations_found:
                print(f"  - {opt}")
        else:
            print("❌ No optimizations found in handle_streaming_response!")
            
    except Exception as e:
        print(f"❌ Error analyzing handle_streaming_response: {e}")

def main():
    """Run all tests"""
    print("🔍 CURRENT PERFORMANCE ISSUE ANALYSIS")
    print("=" * 60)
    
    # Test the optimization functions
    fast_path_works = test_simple_question_fast_path()
    
    # Test direct response functions
    test_direct_response_functions()
    
    # Analyze the main function
    trace_handle_streaming_response()
    
    print("\n" + "=" * 60)
    if fast_path_works:
        print("✅ OPTIMIZATION FUNCTIONS WORK - Issue is in integration")
        print("🎯 Next step: Check if handle_streaming_response actually calls them")
    else:
        print("❌ OPTIMIZATION FUNCTIONS HAVE ISSUES")
        print("🎯 Next step: Fix the optimization functions first")
        
    print("\n💡 Critical Issue:")
    print("   The question 'who are you today?' should:")
    print("   1. Be detected as a simple question ✅")
    print("   2. Skip expensive LLM processing ⚠️") 
    print("   3. Return fast response (2-3 seconds) ❌")
    print("   4. Current: Still takes 75+ seconds ❌")

if __name__ == "__main__":
    main()