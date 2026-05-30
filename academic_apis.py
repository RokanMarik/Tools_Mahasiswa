#!/usr/bin/env python3
"""
Academic APIs Module - Free APIs for Journal Search
Supports: arXiv, PubMed, CORE (all FREE, no API key needed)
"""

import requests
import xml.etree.ElementTree as ET
from typing import List, Dict
from urllib.parse import quote


class AcademicAPIs:
    """Aggregate search across free academic APIs"""
    
    def __init__(self):
        self.arxiv_base = "http://export.arxiv.org/api/query"
        self.pubmed_base = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
        self.core_base = "https://api.core.ac.uk/v3"
    
    def search_all(self, query: str, max_results: int = 3) -> List[Dict]:
        """
        Search across all academic APIs
        
        Args:
            query: Search query
            max_results: Max papers to return (default 3)
        
        Returns:
            List of papers with title and URL
        """
        papers = []
        
        # Search arXiv
        try:
            arxiv_papers = self.search_arxiv(query, max_results=2)
            papers.extend(arxiv_papers)
        except Exception as e:
            print(f"[arXiv ERROR] {e}")
        
        # Search PubMed (if not enough from arXiv)
        if len(papers) < max_results:
            try:
                pubmed_papers = self.search_pubmed(query, max_results=2)
                papers.extend(pubmed_papers)
            except Exception as e:
                print(f"[PubMed ERROR] {e}")
        
        # Search CORE (if still not enough)
        if len(papers) < max_results:
            try:
                core_papers = self.search_core(query, max_results=2)
                papers.extend(core_papers)
            except Exception as e:
                print(f"[CORE ERROR] {e}")
        
        # Return top N results
        return papers[:max_results]
    
    def search_arxiv(self, query: str, max_results: int = 3) -> List[Dict]:
        """
        Search arXiv API (FREE, no key needed)
        Coverage: Physics, Math, CS, Biology
        """
        url = f"{self.arxiv_base}?search_query=all:{quote(query)}&start=0&max_results={max_results}"
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # Parse XML response
        root = ET.fromstring(response.content)
        ns = {'atom': 'http://www.w3.org/2005/Atom'}
        
        papers = []
        for entry in root.findall('atom:entry', ns):
            title = entry.find('atom:title', ns)
            link = entry.find('atom:id', ns)
            
            if title is not None and link is not None:
                papers.append({
                    'title': title.text.strip().replace('\n', ' '),
                    'url': link.text.strip(),
                    'source': 'arXiv'
                })
        
        return papers
    
    def search_pubmed(self, query: str, max_results: int = 3) -> List[Dict]:
        """
        Search PubMed API (FREE, no key needed)
        Coverage: Medical, Biomedical
        """
        # Step 1: Search for IDs
        search_url = f"{self.pubmed_base}/esearch.fcgi"
        search_params = {
            'db': 'pubmed',
            'term': query,
            'retmax': max_results,
            'retmode': 'json'
        }
        
        search_response = requests.get(search_url, params=search_params, timeout=10)
        search_response.raise_for_status()
        search_data = search_response.json()
        
        ids = search_data.get('esearchresult', {}).get('idlist', [])
        if not ids:
            return []
        
        # Step 2: Fetch details for IDs
        fetch_url = f"{self.pubmed_base}/esummary.fcgi"
        fetch_params = {
            'db': 'pubmed',
            'id': ','.join(ids),
            'retmode': 'json'
        }
        
        fetch_response = requests.get(fetch_url, params=fetch_params, timeout=10)
        fetch_response.raise_for_status()
        fetch_data = fetch_response.json()
        
        papers = []
        for pmid in ids:
            article = fetch_data.get('result', {}).get(pmid, {})
            title = article.get('title', 'Untitled')
            
            # PubMed URL
            url = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
            
            papers.append({
                'title': title,
                'url': url,
                'source': 'PubMed'
            })
        
        return papers
    
    def search_core(self, query: str, max_results: int = 3) -> List[Dict]:
        """
        Search CORE API (FREE, no key needed for basic search)
        Coverage: 200M+ open access papers
        """
        url = f"{self.core_base}/search/works"
        params = {
            'q': query,
            'limit': max_results
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            papers = []
            for item in data.get('results', []):
                title = item.get('title', 'Untitled')
                
                # Try to get download URL or landing page
                download_url = item.get('downloadUrl')
                landing_url = item.get('sourceFulltextUrls', [None])[0] if item.get('sourceFulltextUrls') else None
                url = download_url or landing_url or f"https://core.ac.uk/works/{item.get('id', '')}"
                
                papers.append({
                    'title': title,
                    'url': url,
                    'source': 'CORE'
                })
            
            return papers
        
        except Exception as e:
            # CORE API might require key for some endpoints, fallback gracefully
            print(f"[CORE] Using fallback (no API key): {e}")
            return []


def search_academic_papers(query: str, max_results: int = 3) -> List[Dict]:
    """
    Convenience function to search academic papers
    
    Args:
        query: Search query
        max_results: Max papers to return
    
    Returns:
        List of papers with title, URL, source
    
    Example:
        >>> papers = search_academic_papers("machine learning cancer detection")
        >>> for paper in papers:
        ...     print(f"{paper['title']} - {paper['url']}")
    """
    api = AcademicAPIs()
    return api.search_all(query, max_results)


# Example usage
if __name__ == "__main__":
    print("Testing Academic APIs (FREE, no API key needed)\n")
    print("=" * 60)
    
    # Test 1: arXiv (CS/Physics/Math)
    print("\n[TEST 1] arXiv - Machine Learning")
    print("-" * 60)
    api = AcademicAPIs()
    papers = api.search_arxiv("machine learning", max_results=2)
    for i, paper in enumerate(papers, 1):
        print(f"{i}. {paper['title'][:60]}...")
        print(f"   {paper['url']}\n")
    
    # Test 2: PubMed (Medical)
    print("\n[TEST 2] PubMed - Cancer Detection")
    print("-" * 60)
    papers = api.search_pubmed("cancer detection", max_results=2)
    for i, paper in enumerate(papers, 1):
        print(f"{i}. {paper['title'][:60]}...")
        print(f"   {paper['url']}\n")
    
    # Test 3: Aggregate Search
    print("\n[TEST 3] Aggregate - Deep Learning Medical Imaging")
    print("-" * 60)
    papers = search_academic_papers("deep learning medical imaging", max_results=3)
    for i, paper in enumerate(papers, 1):
        print(f"{i}. [{paper['source']}] {paper['title'][:50]}...")
        print(f"   {paper['url']}\n")
    
    print("=" * 60)
    print("All tests complete!")
