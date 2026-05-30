#!/usr/bin/env python3
import os, requests, json

os.environ["NINEROUTER_URL"] = "http://localhost:20128"
os.environ["NINEROUTER_KEY"] = "sk-2ce0b3116b58ede3-4v2kkj-033fc842"

url = os.getenv("NINEROUTER_URL")
key = os.getenv("NINEROUTER_KEY")
headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}

# First: Ask AI model for specific URLs/links to Sriwijaya journals
print("="*80)
print("ASKING AI FOR SPECIFIC JOURNAL LINKS")
print("="*80)

prompt = """Saya butuh link URL langsung ke jurnal/artikel akademik tentang Kerajaan Sriwijaya (Srivijaya Kingdom).

Tolong berikan 10-15 link URL langsung ke:
1. Paper/artikel di Google Scholar
2. Paper di JSTOR
3. Paper di Academia.edu
4. Jurnal di Garuda (garuda.kemdikbud.go.id)
5. Repository universitas Indonesia (UI, UGM, Unsri)

Format:
- Judul paper
- URL langsung
- Sumber (Google Scholar, JSTOR, dll)
- Singkatannya 1 kalimat tentang isinya

Pastikan URL yang kamu berikan adalah URL yang realistis dan valid."""

chat_payload = {
    "model": "Mencari_Jurnal_Ilmiah",
    "messages": [{"role": "user", "content": prompt}],
    "max_tokens": 3000,
    "temperature": 0.3,
    "stream": False
}

try:
    resp = requests.post(f"{url}/v1/chat/completions", headers=headers, json=chat_payload)
    resp.raise_for_status()
    result = resp.json()
    print(result["choices"][0]["message"]["content"])
except Exception as e:
    print(f"Error: {e}")
