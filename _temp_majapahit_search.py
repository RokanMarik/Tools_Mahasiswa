import requests, json, os

url = 'http://localhost:20128/v1/chat/completions'
headers = {
    'Authorization': 'Bearer sk-2ce0b3116b58ede3-2yi9zn-e9931f89',
    'Content-Type': 'application/json'
}

prompt = (
    "I need specific academic papers about the Majapahit Empire. "
    "Please provide exactly 5 real papers with this exact JSON format:\n\n"
    '{"papers": [{'
    '"title": "exact paper title", '
    '"authors": ["author1", "author2"], '
    '"year": 2020, '
    '"journal": "journal name", '
    '"doi": "10.xxxx/xxxxx", '
    '"url": "https://doi.org/10.xxxx/xxxxx or direct URL", '
    '"abstract": "brief abstract or description"'
    "}]}\n\n"
    "Search your knowledge for real papers. If you don't know the exact DOI, "
    "provide a Google Scholar or Semantic Scholar URL. Be as accurate as possible. "
    "Include papers from well-known historians like O.W. Wolters, Slamet Muljana, etc. "
    "Return ONLY valid JSON, no markdown formatting."
)

payload = {
    'model': 'Mencari_Jurnal_Ilmiah',
    'messages': [{'role': 'user', 'content': prompt}],
    'max_tokens': 3000,
    'temperature': 0.3,
    'stream': False
}

r = requests.post(url, headers=headers, json=payload, timeout=60)
result = r.json()['choices'][0]['message']['content']

# Try to parse and display nicely
try:
    data = json.loads(result)
    for i, paper in enumerate(data.get('papers', []), 1):
        print(f"\n{'='*60}")
        print(f"{i}. {paper.get('title', 'N/A')}")
        print(f"   Authors: {', '.join(paper.get('authors', []))}")
        print(f"   Year: {paper.get('year', 'N/A')} | Journal: {paper.get('journal', 'N/A')}")
        print(f"   DOI: {paper.get('doi', 'N/A')}")
        print(f"   URL: {paper.get('url', 'N/A')}")
        print(f"   Abstract: {paper.get('abstract', 'N/A')}")
except:
    print(result)
