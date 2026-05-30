#!/usr/bin/env python3
"""Journal Analysis System — CLI Orchestrator.

Usage:
    python analyze.py jurnal.pdf --mode read
    python analyze.py jurnal.pdf --mode review
    python analyze.py jurnal.pdf --mode full
    python analyze.py --input-text "teks..." --mode review

Note: generate, data-analysis, and compare modes deferred to Phase 2-4.
"""

import argparse
import hashlib
import json
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Journal Analysis System")
    parser.add_argument("input", nargs="?", help="PDF file or URL/DOI")
    parser.add_argument("--mode", required=True, choices=["read", "review", "full"], help="Analysis mode")
    parser.add_argument("--input-text", help="Input text directly")
    parser.add_argument("--no-limit", action="store_true", help="Bypass token budget limit")
    args = parser.parse_args()

    # Load config
    config = _load_config()

    # Initialize core components
    from core.token_budget import TokenBudget
    from core.cache import AnalysisCache
    from core.error_handler import ErrorHandler
    from core.output_aggregator import OutputAggregator
    from models.model_router import ModelRouter, ModelTier

    budget = TokenBudget(
        daily_limit=config["token_budget"]["daily_limit"],
        per_task=config["token_budget"]["per_task"],
    )
    cache = AnalysisCache(ttl_days=config["cache_ttl_days"])
    error_handler = ErrorHandler()
    aggregator = OutputAggregator()
    router = ModelRouter(models=config["default_models"])

    # Check budget
    task_budget = budget.get_task_budget(args.mode)
    if not args.no_limit and not budget.check_available(task_budget):
        print(f"Token budget habis (sisa {budget.remaining}). Reset besok 00:00.")
        sys.exit(1)

    if not args.no_limit and budget.daily_limit > 0 and budget.used_today / budget.daily_limit >= 0.8:
        print(f"Warning: 80% token budget terpakai hari ini.")

    # Parse input
    article = _parse_input(args)
    if article is None:
        print("Error: Tidak bisa parse input.")
        sys.exit(1)

    # Content hash for caching
    content_hash = hashlib.sha256(article.raw_text.encode()).hexdigest()

    # Check parse cache
    cached = cache.get_parsed(content_hash)
    if cached:
        from models.article_data import StructuredArticleData
        article = StructuredArticleData(
            metadata=cached.get("metadata", {}),
            sections=cached.get("sections", {}),
            methodology_type=cached.get("methodology_type", "unknown"),
            raw_text=cached.get("raw_text", ""),
        )
    else:
        cache.set_parsed(content_hash, {
            "metadata": article.metadata,
            "sections": article.sections,
            "methodology_type": article.methodology_type,
            "raw_text": article.raw_text,
        })

    # Execute workers based on mode
    results = {}

    if args.mode in ("read", "review", "full"):
        reader_result = _run_reader(article, cache, content_hash, config, router)
        results["reader"] = reader_result

    if args.mode in ("review", "full"):
        reviewer_result = _run_reviewer(article, results.get("reader"), cache, content_hash, config, router)
        results["reviewer"] = reviewer_result

    # Output
    output = aggregator.aggregate(results)
    print(output)

    # Save to file
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / f"analysis_{content_hash[:8]}.md"
    output_file.write_text(output, encoding="utf-8")
    print(f"\nOutput saved to: {output_file}")

    budget.add_usage(_estimate_tokens(article.word_count, args.mode))


def _load_config() -> dict:
    config_path = Path("analyze.config.json")
    if config_path.exists():
        with open(config_path, "r") as f:
            return json.load(f)
    return {
        "token_budget": {"daily_limit": 50000, "per_task": {"read": 5000, "review": 15000, "full": 30000}},
        "default_models": {"light": "google/gemini-2.0-flash", "medium": "anthropic/claude-sonnet-4-20250514", "heavy": "anthropic/claude-opus-4-20250514"},
        "cache_ttl_days": 7,
    }


def _parse_input(args) -> "StructuredArticleData":
    from parsers.pdf_parser import PDFParser
    from parsers.text_parser import TextParser
    from parsers.url_fetcher import URLFetcher

    if args.input_text:
        parser = TextParser()
        return parser.parse(args.input_text)

    if args.input is None:
        return None

    input_path = Path(args.input)

    # Check if URL/DOI
    if args.input.startswith(("http://", "https://", "doi:")):
        fetcher = URLFetcher()
        return fetcher.fetch(args.input)

    # Check if PDF
    if input_path.suffix.lower() == ".pdf":
        pdf_parser = PDFParser()
        return pdf_parser.parse(str(input_path))

    # Default: treat as text file
    text_parser = TextParser()
    return text_parser.parse(input_path.read_text(encoding="utf-8"))


def _run_reader(article, cache, content_hash, config, router):
    from workers.reader_worker import ReaderWorker

    # Check analysis cache
    cached = cache.get_analysis(content_hash, "reader")
    if cached:
        return {"status": "success", "data": cached}

    model = router.get_model_name(router.select_model("summarize", article.word_count))
    worker = ReaderWorker()
    result = worker.run(article, model=model)

    if result is None:
        return {"status": "failed", "error": "Reader Worker gagal"}

    cache.set_analysis(content_hash, "reader", result)
    return {"status": "success", "data": result}


def _run_reviewer(article, reader_result, cache, content_hash, config, router):
    from workers.reviewer_worker import ReviewerWorker

    # Check analysis cache
    cached = cache.get_analysis(content_hash, "reviewer")
    if cached:
        return {"status": "success", "data": cached}

    model = router.get_model_name(router.select_model("critical_appraisal", article.word_count))
    reader_summary = reader_result["data"]["summary"] if reader_result and reader_result["status"] == "success" else None

    worker = ReviewerWorker()
    result = worker.run(article, reader_summary=reader_summary, model=model)

    if result is None:
        return {"status": "failed", "error": "Reviewer Worker gagal"}

    cache.set_analysis(content_hash, "reviewer", result)
    return {"status": "success", "data": result}


def _estimate_tokens(word_count: int, mode: str) -> int:
    """Rough estimate: 1 word ≈ 1.3 tokens for input, plus output tokens."""
    input_tokens = int(word_count * 1.3)
    output_multiplier = {"read": 2, "review": 5, "full": 7}.get(mode, 3)
    return input_tokens + (input_tokens * output_multiplier // 10)


if __name__ == "__main__":
    main()
