import os
from typing import List, Dict
from modules.web_search_optimizer import WebSearchOptimizer
from modules.content_fetcher import ContentFetcher
from modules.search_cache import SearchCache


class BatchProcessor:
    def __init__(self, ninerouter_url: str = None, ninerouter_key: str = None):
        """Initialize batch processor"""
        self.ninerouter_url = ninerouter_url or os.getenv("NINEROUTER_URL", "http://localhost:20128")
        self.ninerouter_key = ninerouter_key or os.getenv("NINEROUTER_KEY", "")
        
        self.cache = SearchCache()
        self.search_optimizer = WebSearchOptimizer(self.ninerouter_url, self.ninerouter_key, self.cache)
        self.content_fetcher = ContentFetcher(self.ninerouter_url, self.ninerouter_key, self.cache)
    
    def process_batch(self, research_questions: List[str], max_papers_per_question: int = 5) -> Dict:
        """Process batch of research questions"""
        results = {
            "questions": [],
            "total_papers_found": 0,
            "total_errors": 0,
            "processing_status": "completed"
        }
        
        print(f"\n[BATCH START] Processing {len(research_questions)} research questions...")
        
        for i, question in enumerate(research_questions, 1):
            print(f"\n[QUESTION {i}/{len(research_questions)}] {question}")
            question_result = self._process_single_question(question, max_papers_per_question)
            results["questions"].append(question_result)
            results["total_papers_found"] += len(question_result.get("papers", []))
            results["total_errors"] += len(question_result.get("errors", []))
        
        print(f"\n[BATCH COMPLETE] Found {results['total_papers_found']} papers total")
        return results
    
    def _process_single_question(self, research_question: str, max_papers: int = 5) -> Dict:
        """Process a single research question with retry/fallback logic"""
        result = {
            "question": research_question,
            "papers": [],
            "errors": [],
            "status": "pending"
        }
        
        try:
            # Step 1: Search for papers
            print(f"  [STEP 1] Searching for papers...")
            papers = self.search_optimizer.optimize_and_search(research_question)
            
            if not papers:
                # Retry with fallback: try alternative search
                print(f"  [STEP 1 FALLBACK] No results, retrying with simplified query...")
                papers = self._retry_search_with_fallback(research_question)
            
            if not papers:
                result["status"] = "no_results"
                result["errors"].append("No papers found after retry")
                print(f"  [STATUS] No papers found")
                return result
            
            print(f"  [STEP 2] Fetching content from {len(papers)} papers...")
            # Step 2: Fetch content from top papers
            urls = [p["url"] for p in papers]
            fetched_papers = self.content_fetcher.fetch_papers(urls, max_papers=max_papers)
            
            result["papers"] = fetched_papers
            result["status"] = "success"
            print(f"  [STATUS] Success - {len(fetched_papers)} papers fetched")
        
        except Exception as e:
            result["status"] = "error"
            result["errors"].append(str(e))
            print(f"  [STATUS] Error - {str(e)}")
        
        return result
    
    def _retry_search_with_fallback(self, research_question: str) -> List[Dict]:
        """Retry search with alternative terms (fallback strategy B->D)"""
        try:
            # Try with simplified query
            simplified_query = " ".join(research_question.split()[:3])
            print(f"  [FALLBACK QUERY] {simplified_query}")
            papers = self.search_optimizer.optimize_and_search(simplified_query)
            return papers
        except Exception as e:
            print(f"  [FALLBACK ERROR] Fallback search also failed: {e}")
            return []
