#!/usr/bin/env python3
import os, requests, json

os.environ["NINEROUTER_URL"] = "http://localhost:20128"
os.environ["NINEROUTER_KEY"] = "sk-2ce0b3116b58ede3-4v2kkj-033fc842"

url = os.getenv("NINEROUTER_URL")
key = os.getenv("NINEROUTER_KEY")
headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}

# Check available web search models
print("="*80)
print("AVAILABLE WEB SEARCH MODELS")
print("="*80)
try:
    resp = requests.get(f"{url}/v1/models/web", headers=headers)
    resp.raise_for_status()
    result = resp.json()
    for m in result.get('data', []):
        print(f"- {m.get('id')} (kind: {m.get('kind')})")
except Exception as e:
    print(f"Error: {e}")

# Try search with "provider" instead of "model"
print("\n" + "="*80)
print("TRYING SEARCH WITH DIFFERENT PARAMS")
print("="*80)

search_payload = {
    "provider": "search-combo",
    "query": "Sriwijaya kingdom academic journal research",
    "max_results": 10
}

try:
    resp = requests.post(f"{url}/v1/search", headers=headers, json=search_payload)
    resp.raise_for_status()
    result = resp.json()
    print(f"Provider: {result.get('provider')}")
    for i, r in enumerate(result.get('results', []), 1):
        print(f"\n{i}. {r.get('title', 'N/A')}")
        print(f"   URL: {r.get('url', 'N/A')}")
        snippet = r.get('snippet', '')
        if snippet:
            print(f"   {snippet[:200]}...")
except Exception as e:
    print(f"Error: {e}")
    # Try to get more error info
    try:
        print(f"Response body: {resp.text}")
    except:
        pass
