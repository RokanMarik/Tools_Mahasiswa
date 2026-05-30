#!/usr/bin/env python3
import os, requests, json

os.environ["NINEROUTER_URL"] = "http://localhost:20128"
os.environ["NINEROUTER_KEY"] = "sk-2ce0b3116b58ede3-4v2kkj-033fc842"

url = os.getenv("NINEROUTER_URL")
key = os.getenv("NINEROUTER_KEY")
headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}

# First: search via /v1/search endpoint for actual journal links
print("="*80)
print("MENCARI LINK JURNAL SRIWIJAYA - WEB SEARCH")
print("="*80)

search_payload = {
    "model": "tavily",
    "query": "Sriwijaya kingdom academic journal articles research papers",
    "max_results": 10
}

try:
    resp = requests.post(f"{url}/v1/search", headers=headers, json=search_payload)
    resp.raise_for_status()
    result = resp.json()
    print(f"\nProvider: {result.get('provider')}")
    print(f"Query: {result.get('query')}")
    print(f"\nResults ({len(result.get('results', []))} found):\n")
    for i, r in enumerate(result.get('results', []), 1):
        print(f"{i}. {r.get('title', 'N/A')}")
        print(f"   URL: {r.get('url', 'N/A')}")
        snippet = r.get('snippet', '')
        if snippet:
            print(f"   {snippet[:200]}...")
        print()
except Exception as e:
    print(f"Search Error: {e}")

# Second: search Indonesian journals
print("\n" + "="*80)
print("MENCARI JURNAL SRIWIJAYA - INDONESIA (GARUDA/Google Scholar)")
print("="*80)

search_payload2 = {
    "model": "tavily",
    "query": "jurnal Kerajaan Sriwijaya arkeologi sejarah site:garuda.ristekbrin.go.id OR site:garuda.kemdikbud.go.id",
    "max_results": 5
}

try:
    resp = requests.post(f"{url}/v1/search", headers=headers, json=search_payload2)
    resp.raise_for_status()
    result = resp.json()
    print(f"\nProvider: {result.get('provider')}")
    for i, r in enumerate(result.get('results', []), 1):
        print(f"\n{i}. {r.get('title', 'N/A')}")
        print(f"   URL: {r.get('url', 'N/A')}")
        snippet = r.get('snippet', '')
        if snippet:
            print(f"   {snippet[:200]}...")
except Exception as e:
    print(f"Search Error: {e}")

# Third: search for direct PDF/paper links
print("\n" + "="*80)
print("MENCARI PAPER/PDF SRIWIJAYA - ACADEMIC DATABASES")
print("="*80)

search_payload3 = {
    "model": "tavily",
    "query": "Srivijaya kingdom archaeological research paper PDF journal download",
    "max_results": 5
}

try:
    resp = requests.post(f"{url}/v1/search", headers=headers, json=search_payload3)
    resp.raise_for_status()
    result = resp.json()
    print(f"\nProvider: {result.get('provider')}")
    for i, r in enumerate(result.get('results', []), 1):
        print(f"\n{i}. {r.get('title', 'N/A')}")
        print(f"   URL: {r.get('url', 'N/A')}")
        snippet = r.get('snippet', '')
        if snippet:
            print(f"   {snippet[:200]}...")
except Exception as e:
    print(f"Search Error: {e}")
