#!/usr/bin/env python3
"""
Quick Start - Test 9Router Integration
Contoh sederhana untuk test semua fitur
"""

import os
import requests

# Config
NINEROUTER_URL = "http://localhost:20128"
NINEROUTER_KEY = "sk-2ce0b3116b58ede3-4v2kkj-033fc842"

def test_health():
    """Test koneksi ke 9Router"""
    print("1. Testing 9Router connection...")
    try:
        response = requests.get(f"{NINEROUTER_URL}/api/health")
        if response.json().get("ok"):
            print("   [OK] 9Router is running!")
            return True
    except Exception as e:
        print(f"   [FAIL] Error: {e}")
        return False

def test_chat():
    """Test chat endpoint"""
    print("\n2. Testing chat endpoint...")
    headers = {
        "Authorization": f"Bearer {NINEROUTER_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "Mencari_Jurnal_Ilmiah",
        "messages": [{"role": "user", "content": "Halo! Sebutkan 3 database jurnal ilmiah terpopuler."}],
        "max_tokens": 300,
        "stream": False
    }
    
    try:
        response = requests.post(
            f"{NINEROUTER_URL}/v1/chat/completions",
            headers=headers,
            json=payload
        )
        result = response.json()
        content = result["choices"][0]["message"]["content"]
        print(f"   [OK] Chat working! Response preview:")
        print(f"   {content[:200]}...")
        return True
    except Exception as e:
        print(f"   [FAIL] Error: {e}")
        return False

def test_models():
    """Test list models"""
    print("\n3. Testing models endpoint...")
    headers = {"Authorization": f"Bearer {NINEROUTER_KEY}"}
    
    try:
        response = requests.get(f"{NINEROUTER_URL}/v1/models", headers=headers)
        models = response.json()["data"]
        print(f"   [OK] Found {len(models)} models:")
        for model in models[:5]:
            print(f"     - {model['id']}")
        if len(models) > 5:
            print(f"     ... and {len(models) - 5} more")
        return True
    except Exception as e:
        print(f"   [FAIL] Error: {e}")
        return False

def main():
    print("="*60)
    print("9Router Quick Test")
    print("="*60)
    
    results = []
    results.append(test_health())
    results.append(test_chat())
    results.append(test_models())
    
    print("\n" + "="*60)
    if all(results):
        print("[SUCCESS] All tests passed! 9Router is ready to use.")
        print("\nNext steps:")
        print("  - Run: python 9router_journal_finder.py")
        print("  - Read: README_9ROUTER.md")
    else:
        print("[FAILED] Some tests failed. Check configuration.")
    print("="*60)

if __name__ == "__main__":
    main()
