#!/usr/bin/env python3
"""
Test script to verify GPT4Free functionality including image generation
Run this before deploying to check if g4f is working
"""

import g4f
import sys
import time
import json

def test_basic_chat():
    """Test basic chat functionality"""
    print("Testing basic chat...")
    
    try:
        messages = [
            {"role": "user", "content": "Hello, can you say hi back?"}
        ]
        
        response = g4f.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            stream=False
        )
        
        print(f"Response: {response}")
        return True
        
    except Exception as e:
        print(f"Basic chat test failed: {e}")
        return False

def test_streaming():
    """Test streaming functionality"""
    print("\nTesting streaming...")
    
    try:
        messages = [
            {"role": "user", "content": "Count from 1 to 5"}
        ]
        
        response = g4f.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            stream=True
        )
        
        full_response = ""
        for chunk in response:
            if chunk:
                full_response += str(chunk)
                print(chunk, end='', flush=True)
        
        print(f"\nFull response received: {len(full_response)} chars")
        return True
        
    except Exception as e:
        print(f"Streaming test failed: {e}")
        return False

def test_providers():
    """Test different providers"""
    print("\nTesting text providers...")
    
    # Extended list of providers to test
    providers_to_test = [
        'Blackbox', 'DDG', 'ChatGpt', 'DeepInfraChat',
        'You', 'Aichat', 'ChatBase', 'FreeGpt'
    ]
    
    working_providers = []
    
    for provider_name in providers_to_test:
        try:
            if hasattr(g4f.Provider, provider_name):
                provider = getattr(g4f.Provider, provider_name)
                print(f"Testing {provider_name}...")
                
                messages = [
                    {"role": "user", "content": "Say 'test successful'"}
                ]
                
                response = g4f.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                    provider=provider,
                    stream=False,
                    timeout=10
                )
                
                if response and "test" in str(response).lower():
                    print(f"✅ {provider_name} working")
                    working_providers.append(provider_name)
                else:
                    print(f"❌ {provider_name} returned empty response")
                
        except Exception as e:
            print(f"❌ Provider {provider_name} failed: {e}")
            continue
    
    print(f"\nWorking providers: {working_providers}")
    return len(working_providers) > 0

def test_image_generation():
    """Test image generation functionality"""
    print("\nTesting image generation...")
    
    # Test providers that might support image generation
    image_providers = ['ARTA', 'Blackbox', 'PollinationsImage', 'Bing']
    
    for provider_name in image_providers:
        try:
            if hasattr(g4f.Provider, provider_name):
                provider = getattr(g4f.Provider, provider_name)
                print(f"Testing image generation with {provider_name}...")
                
                # Method 1: Using ImageGeneration if available
                if hasattr(g4f, 'ImageGeneration'):
                    try:
                        response = g4f.ImageGeneration.create(
                            prompt="a simple red circle",
                            provider=provider,
                            timeout=15
                        )
                        if response:
                            print(f"✅ {provider_name} image generation working (Method 1)")
                            return True
                    except Exception as e:
                        print(f"Method 1 failed for {provider_name}: {e}")
                
                # Method 2: Try alternative approaches
                try:
                    # Some providers might use chat completion with image flag
                    response = g4f.ChatCompletion.create(
                        model="dalle" if "dall" in provider_name.lower() else "default",
                        messages=[{"role": "user", "content": "Generate image: a red circle"}],
                        provider=provider,
                        image=True,
                        timeout=15
                    )
                    if response:
                        print(f"✅ {provider_name} image generation working (Method 2)")
                        return True
                except Exception as e:
                    print(f"Method 2 failed for {provider_name}: {e}")
                    
        except Exception as e:
            print(f"❌ Image provider {provider_name} failed: {e}")
            continue
    
    print("⚠️  No image providers working in test environment")
    return False

def test_models():
    """Test different models"""
    print("\nTesting different models...")
    
    models_to_test = [
        'gpt-3.5-turbo',
        'gpt-4',
        'gpt-4o-mini',
        'claude-v1',
        'llama-3-8b',
        'deepseek-chat'
    ]
    
    working_models = []
    
    for model in models_to_test:
        try:
            print(f"Testing model {model}...")
            
            messages = [
                {"role": "user", "content": "Reply with 'ok' if you understand"}
            ]
            
            response = g4f.ChatCompletion.create(
                model=model,
                messages=messages,
                stream=False,
                timeout=10
            )
            
            if response:
                print(f"✅ Model {model} responded")
                working_models.append(model)
            else:
                print(f"❌ Model {model} no response")
                
        except Exception as e:
            print(f"❌ Model {model} failed: {e}")
            continue
    
    print(f"\nWorking models: {working_models}")
    return len(working_models) > 0

def test_concurrent_requests():
    """Test handling multiple concurrent requests"""
    print("\nTesting concurrent requests...")
    
    import concurrent.futures
    import threading
    
    def make_request(i):
        try:
            response = g4f.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": f"Say 'Response {i}'"}],
                stream=False,
                timeout=15
            )
            return f"Request {i}: Success"
        except Exception as e:
            return f"Request {i}: Failed - {e}"
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(make_request, i) for i in range(3)]
        results = [f.result() for f in concurrent.futures.as_completed(futures)]
        
    for result in results:
        print(result)
    
    success_count = sum(1 for r in results if "Success" in r)
    print(f"\nConcurrent requests: {success_count}/3 successful")
    return success_count > 0

def main():
    """Run all tests"""
    print("Starting GPT4Free comprehensive tests...\n")
    print(f"g4f version: {g4f.__version__ if hasattr(g4f, '__version__') else 'unknown'}")
    print("=" * 50)
    
    test_results = {}
    
    # Test basic functionality
    test_results['basic_chat'] = test_basic_chat()
    print("=" * 50)
    
    # Test streaming
    test_results['streaming'] = test_streaming()
    print("=" * 50)
    
    # Test providers
    test_results['providers'] = test_providers()
    print("=" * 50)
    
    # Test models
    test_results['models'] = test_models()
    print("=" * 50)
    
    # Test image generation
    test_results['image_generation'] = test_image_generation()
    print("=" * 50)
    
    # Test concurrent requests
    test_results['concurrent'] = test_concurrent_requests()
    print("=" * 50)
    
    # Summary
    print("\n📊 TEST SUMMARY:")
    print("-" * 30)
    for test_name, result in test_results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name.ljust(20)}: {status}")
    
    total_passed = sum(1 for r in test_results.values() if r)
    total_tests = len(test_results)
    
    print("-" * 30)
    print(f"Total: {total_passed}/{total_tests} tests passed")
    
    if total_passed == total_tests:
        print("\n🎉 All tests passed! Ready for deployment.")
        return True
    else:
        print("\n⚠️  Some tests failed. Review the results above.")
        print("Note: Image generation might not work in all environments.")
        return total_passed >= 4  # At least core functionality should work

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)