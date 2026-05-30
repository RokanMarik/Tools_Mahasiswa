#!/usr/bin/env python3
"""
Simple Journal Finder - Token-Efficient Version
Returns 3 open access paper links only
"""

import os
import requests
from typing import List, Dict, Optional
from modules.search_cache import SearchCache
from academic_apis import search_academic_papers


class SimpleJournalFinder:
    """
    Simple, token-efficient journal finder
    - Interactive clarification
    - 3 papers only
    - Links only (no content fetching)
    - ~100-200 tokens per query
    """
    
    def __init__(self):
        """Initialize simple journal finder"""
        self.cache = SearchCache()
    
    def search(self, topic: str, context: str = "") -> List[Dict]:
        """
        Search for journals using FREE academic APIs (arXiv, PubMed, CORE)
        
        Args:
            topic: Main topic (e.g., "sriwijaya")
            context: Context/clarification (e.g., "kerajaan")
        
        Returns:
            List of 3 papers with title and URL
        """
        # Build simple query
        query = f"{topic} {context}".strip()
        
        # Check cache first
        cache_key = f"academic:{query}"
        cached = self.cache.get(cache_key)
        if cached:
            print(f"[CACHE HIT] {query}")
            return cached[:3]  # Return only 3
        
        print(f"[SEARCHING] {query}")
        print(f"[SOURCES] arXiv + PubMed + CORE (FREE APIs)")
        
        try:
            # Search using free academic APIs
            papers = search_academic_papers(query, max_results=3)
            
            # Cache results
            self.cache.set(cache_key, papers)
            print(f"[FOUND] {len(papers)} papers")
            return papers
        
        except Exception as e:
            print(f"[ERROR] {e}")
            return []
    
    def format_results(self, papers: List[Dict]) -> str:
        """
        Format results as simple list (token-efficient)
        
        Args:
            papers: List of papers
        
        Returns:
            Formatted string
        """
        if not papers:
            return "Tidak ada hasil. Coba kata kunci lain?"
        
        output = f"{len(papers)} jurnal open access:\n\n"
        for i, paper in enumerate(papers, 1):
            output += f"{i}. {paper['title']}\n"
            output += f"   {paper['url']}\n\n"
        
        return output.strip()
    
    def interactive_search(self):
        """
        Interactive search workflow
        Follows the natural language trigger pattern
        """
        print("=== Simple Journal Finder ===\n")
        
        # Step 1: Get topic
        topic = input("Tentang apa? ").strip()
        if not topic:
            print("Topik tidak boleh kosong.")
            return
        
        # Step 2: Get context/clarification
        context = input(f"{topic.capitalize()} apa? ").strip()
        
        # Step 3: Search
        print("\nMencari...\n")
        papers = self.search(topic, context)
        
        # Step 4: Display results
        print(self.format_results(papers))


def simple_search(topic: str, context: str = "") -> str:
    """
    Simple function for direct use
    
    Args:
        topic: Main topic
        context: Context/clarification
    
    Returns:
        Formatted results string
    
    Example:
        >>> result = simple_search("sriwijaya", "kerajaan")
        >>> print(result)
    """
    finder = SimpleJournalFinder()
    papers = finder.search(topic, context)
    return finder.format_results(papers)


# Example usage
if __name__ == "__main__":
    # Check environment variables
    if not os.getenv("NINEROUTER_KEY"):
        print("Warning: NINEROUTER_KEY not set!")
        print("Set with: export NINEROUTER_KEY='your-key-here'")
        print()
    
    # Example 1: Interactive mode
    print("Example 1: Interactive Mode")
    print("-" * 40)
    finder = SimpleJournalFinder()
    
    # Simulate interactive workflow
    print("User: cari jurnal dong")
    print("Agent: Tentang apa?")
    print("User: sriwijaya")
    print("Agent: Sriwijaya apa? (kerajaan/universitas/budaya)")
    print("User: kerajaan")
    print("Agent: Mencari...\n")
    
    papers = finder.search("sriwijaya", "kerajaan")
    print(finder.format_results(papers))
    
    print("\n" + "=" * 40 + "\n")
    
    # Example 2: Direct function call
    print("Example 2: Direct Function Call")
    print("-" * 40)
    result = simple_search("machine learning", "medical")
    print(result)
    
    print("\n" + "=" * 40 + "\n")
    
    # Example 3: Interactive mode (uncomment to use)
    # finder.interactive_search()
