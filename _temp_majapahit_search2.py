import requests, json

url = 'http://localhost:20128/v1/chat/completions'
headers = {
    'Authorization': 'Bearer sk-2ce0b3116b58ede3-2yi9zn-e9931f89',
    'Content-Type': 'application/json'
}

prompt = (
    "List 5 real academic papers about Majapahit Empire. "
    "Return ONLY valid JSON, no thinking tags, no markdown, no extra text. "
    "Format: {\"papers\":[{\"title\":\"\",\"authors\":[],\"year\":0,\"journal\":\"\",\"doi\":\"\",\"url\":\"\",\"abstract\":\"\"},{},{},{},{},{}]} "
    "Use real papers from historians like O.W. Wolters, M.C. Ricklefs, Theodore Pigeaud. "
    "If unsure about DOI, use a Google Scholar or Semantic Scholar search URL."
)

payload = {
    'model': 'kr/claude-sonnet-4.5',
    'messages': [{'role': 'user', 'content': prompt}],
    'max_tokens': 2000,
    'temperature': 0.1,
    'stream': False
}

r = requests.post(url, headers=headers, json=payload, timeout=90)
result = r.json()['choices'][0]['message']['content']

try:
    data = json.loads(result)
    for i, paper in enumerate(data.get('papers', []), 1):
        print(f"\n{'='*70}")
        print(f"{i}. {paper.get('title', 'N/A')}")
        print(f"   Authors: {', '.join(paper.get('authors', []))}")
        print(f"   Year: {paper.get('year', 'N/A')} | Journal: {paper.get('journal', 'N/A')}")
        print(f"   DOI: {paper.get('doi', 'N/A')}")
        print(f"   URL: {paper.get('url', 'N/A')}")
        print(f"   Abstract: {paper.get('abstract', 'N/A')}")
except Exception as e:
    print(f"Parse error: {e}")
    print(result)
