#!/usr/bin/env python3
"""
9Router Journal Finder
Script untuk mencari dan menganalisis jurnal ilmiah menggunakan 9Router
"""

import os
import requests
import json
from typing import List, Dict

# Zotero integration
from modules.zotero.client import ZoteroClient
from modules.zotero.collection_picker import CollectionPicker
from modules.zotero.duplicate_detector import DuplicateDetector
from modules.zotero.gap_analyzer import GapAnalyzer
from modules.zotero.recommendation_engine import RecommendationEngine
from modules.zotero.citation_formatter import CitationFormatter

# Konfigurasi 9Router
NINEROUTER_URL = os.getenv("NINEROUTER_URL", "http://localhost:20128")
NINEROUTER_KEY = os.getenv("NINEROUTER_KEY", "")

class JournalFinder:
    def __init__(self):
        self.base_url = NINEROUTER_URL
        self.headers = {
            "Authorization": f"Bearer {NINEROUTER_KEY}",
            "Content-Type": "application/json"
        }
    
    def chat(self, prompt: str, model: str = "Mencari_Jurnal_Ilmiah", 
             max_tokens: int = 1000, temperature: float = 0.7) -> str:
        """
        Kirim chat request ke 9Router
        """
        url = f"{self.base_url}/v1/chat/completions"
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": temperature,
            "stream": False
        }
        
        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"]
        except requests.exceptions.RequestException as e:
            return f"Error: {e}"
    
    def find_journals(self, topic: str) -> str:
        """
        Cari rekomendasi jurnal berdasarkan topik
        """
        prompt = f"""Saya sedang mencari jurnal ilmiah tentang "{topic}".
        
Tolong berikan:
1. 5 jurnal/konferensi terbaik untuk topik ini
2. Database yang bisa digunakan untuk mencari paper
3. Keywords yang efektif untuk pencarian
4. Tips mencari paper berkualitas di bidang ini

Format response dengan jelas dan terstruktur."""
        
        print(f"\n{'='*80}")
        print(f"Mencari jurnal tentang: {topic}")
        print(f"{'='*80}\n")
        
        response = self.chat(prompt, max_tokens=1500)
        return response
    
    def analyze_paper(self, paper_title: str, paper_abstract: str = "") -> str:
        """
        Analisis paper dan berikan ringkasan
        """
        prompt = f"""Analisis paper berikut:

Judul: {paper_title}
{"Abstract: " + paper_abstract if paper_abstract else ""}

Tolong berikan:
1. Ringkasan singkat (2-3 kalimat)
2. Kontribusi utama
3. Metodologi yang digunakan
4. Relevansi dan aplikasi praktis
5. Kekuatan dan kelemahan (jika bisa diidentifikasi dari judul/abstract)"""
        
        response = self.chat(prompt, model="Merangkum_Memperjelas_Catatan", max_tokens=1000)
        return response
    
    def generate_search_keywords(self, research_question: str) -> str:
        """
        Generate keywords untuk pencarian jurnal
        """
        prompt = f"""Saya ingin meneliti: "{research_question}"

Tolong generate:
1. 10 keywords/phrases untuk pencarian di database jurnal
2. Boolean search query yang efektif
3. Sinonim dan variasi istilah yang relevan
4. Istilah yang sebaiknya di-exclude (jika ada)

Format dalam bentuk yang siap digunakan untuk pencarian."""
        
        response = self.chat(prompt, max_tokens=800)
        return response
    
    def list_available_models(self) -> List[Dict]:
        """
        List semua model yang tersedia di 9Router
        """
        url = f"{self.base_url}/v1/models"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            result = response.json()
            return result.get("data", [])
        except requests.exceptions.RequestException as e:
            print(f"Error listing models: {e}")
            return []

    # --- Zotero Integration Methods ---

    def pull_zotero(
        self,
        api_key: str = None,
        collection_name: str = None,
        citation_style: str = "apa",
    ) -> None:
        """Main entry point for Zotero analysis.

        Pulls collection from Zotero, checks duplicates, analyzes gaps,
        and recommends related papers. All output to terminal.

        Args:
            api_key: Zotero API key (or from env var).
            collection_name: Collection name to analyze (or interactive pick).
            citation_style: Citation format ('apa', 'ieee', 'mla', 'chicago').
        """
        api_key = api_key or os.getenv("ZOTERO_API_KEY")
        if not api_key:
            print("=== Zotero Integration ===")
            print("Masukkan Zotero API key: ", end="")
            try:
                api_key = input().strip()
            except (EOFError, KeyboardInterrupt):
                print("\nDibatalkan.")
                return

        if not api_key:
            print("API key diperlukan. Buat di zotero.org -> Settings -> API Keys")
            return

        # Initialize client
        print("\nMenghubungkan ke Zotero...")
        try:
            client = ZoteroClient(api_key=api_key)
            # Auto-detect user ID
            client.library_id = client.get_user_id()
        except Exception as e:
            print(f"Error: {e}")
            return

        # Pick collection
        picker = CollectionPicker(client)
        if collection_name:
            selected = picker.select_by_name(collection_name)
            if not selected:
                print(f"Koleksi '{collection_name}' tidak ditemukan.")
                return
        else:
            selected = picker.pick()
            if not selected:
                return

        print(f"\nPulling {selected['num_items']} items dari '{selected['name']}'...")
        try:
            items = client.get_collection_items(selected["key"])
        except Exception as e:
            print(f"Error: {e}")
            return

        print(f"OK: {len(items)} items berhasil di-pull\n")

        # Citation style selection
        if citation_style not in CitationFormatter.STYLES:
            print("Pilih format daftar pustaka:")
            for i, style in enumerate(CitationFormatter.STYLES, 1):
                print(f"  {i}. {style.upper()}")
            print(f"\nPilih nomor [default: 1]: ", end="")
            try:
                choice = input().strip()
                if choice.isdigit() and 1 <= int(choice) <= len(CitationFormatter.STYLES):
                    citation_style = CitationFormatter.STYLES[int(choice) - 1]
            except (EOFError, KeyboardInterrupt, ValueError):
                citation_style = "apa"

        formatter = CitationFormatter()

        # Step 1: Duplicate check
        print("=== Cek Duplikat ===")
        duplicates = self.check_duplicates(items)
        if not duplicates:
            print("Tidak ada duplikat ditemukan.\n")
        else:
            for dup in duplicates:
                titles = [item["title"] for item in dup["group"]]
                print(f"  {dup['detail']}:")
                for t in titles:
                    print(f"    - \"{t}\"")
            print()

        # Step 2: Gap analysis
        print("=== Analisis Gap ===")
        gaps = self.analyze_gaps(items)
        covered = [g for g in gaps if g["status"] == "covered"]
        low = [g for g in gaps if g["status"] == "low"]
        missing = [g for g in gaps if g["status"] == "missing"]

        if covered:
            for g in covered[:5]:  # Show top 5
                print(f"  [+] {g['topic']} ({g['count']} papers)")
        if low:
            for g in low:
                print(f"  [~] {g['topic']} ({g['count']} paper - kurang)")
        if missing:
            for g in missing[:5]:  # Show top 5
                print(f"  [-] {g['topic']} (0 papers)")
        print()

        # Step 3: Recommendations
        print("=== Rekomendasi Paper ===")
        existing_topics = [g["topic"] for g in covered]
        recs = self.recommend_related(gaps, existing_topics)
        if not recs:
            print("Tidak ada rekomendasi saat ini.\n")
        else:
            for i, rec in enumerate(recs, 1):
                print(f"  {i}. \"{rec['title']}\"")
                if rec["doi"]:
                    print(f"     DOI: {rec['doi']}")
                if rec["url"]:
                    print(f"     {rec['url']}")
                print(f"     Alasan: {rec['reason']}")
                print()

        # Step 4: Formatted bibliography (first 5 papers)
        print(f"=== Daftar Pustaka ({citation_style.upper()} - 5 teratas) ===")
        for i, item in enumerate(items[:5], 1):
            citation = formatter.format(item, style=citation_style, number=i)
            print(f"  {citation}")
        print()

    def check_duplicates(self, items: List[Dict]) -> List[Dict]:
        """Check for duplicate items in a collection."""
        detector = DuplicateDetector()
        return detector.find_duplicates(items)

    def analyze_gaps(self, items: List[Dict]) -> List[Dict]:
        """Analyze topic gaps in a collection."""
        analyzer = GapAnalyzer()
        return analyzer.analyze(items)

    def recommend_related(self, gaps: List[Dict], existing_topics: List[str]) -> List[Dict]:
        """Get paper recommendations for gap topics."""
        engine = RecommendationEngine(self)
        return engine.recommend(gaps, existing_topics)

    def create_zotero_collection(self, api_key: str, name: str, parent_key: str = None) -> Dict:
        """Create a new Zotero collection.

        Args:
            api_key: Zotero API key.
            name: Collection name.
            parent_key: Parent collection key (None for top-level).

        Returns:
            {key, name, version}.
        """
        client = ZoteroClient(api_key=api_key)
        client.library_id = client.get_user_id()
        return client.create_collection(name, parent_key)

    def add_item_to_zotero_collection(
        self, api_key: str, collection_key: str, item_data: Dict
    ) -> Dict:
        """Add an item to a Zotero collection.

        Args:
            api_key: Zotero API key.
            collection_key: Target collection key.
            item_data: Dict with title, authors/creators, date, doi, url, journal, itemType.

        Returns:
            {key, version}.
        """
        client = ZoteroClient(api_key=api_key)
        client.library_id = client.get_user_id()
        return client.add_item(collection_key, item_data)


def main():
    """
    Contoh penggunaan
    """
    finder = JournalFinder()
    
    # Contoh 1: Cari jurnal tentang topik tertentu
    print("\n" + "="*80)
    print("CONTOH 1: Mencari Jurnal tentang Machine Learning")
    print("="*80)
    result = finder.find_journals("machine learning for medical diagnosis")
    print(result)
    
    # Contoh 2: Generate keywords untuk penelitian
    print("\n\n" + "="*80)
    print("CONTOH 2: Generate Search Keywords")
    print("="*80)
    research_q = "How does deep learning improve accuracy in cancer detection from medical images?"
    keywords = finder.generate_search_keywords(research_q)
    print(keywords)
    
    # Contoh 3: List available models
    print("\n\n" + "="*80)
    print("CONTOH 3: Available Models")
    print("="*80)
    models = finder.list_available_models()
    for model in models[:10]:  # Show first 10
        print(f"- {model.get('id')} (owned_by: {model.get('owned_by')})")


if __name__ == "__main__":
    # Set environment variables jika belum
    if not NINEROUTER_KEY:
        print("Warning: NINEROUTER_KEY tidak diset!")
        print("Set dengan: export NINEROUTER_KEY='your-key-here'")
        print("Atau di Windows: $env:NINEROUTER_KEY='your-key-here'")
    
    main()
