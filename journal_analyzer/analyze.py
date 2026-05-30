#!/usr/bin/env python3
"""Journal Analysis System — CLI Orchestrator.

Usage:
    python analyze.py jurnal.pdf --mode read
    python analyze.py jurnal.pdf --mode review
    python analyze.py jurnal.pdf --mode full
    python analyze.py jurnal.pdf --mode gap
    python analyze.py jurnal.pdf --mode generate --prompt "Topik riset"
    python analyze.py --input-text "teks..." --mode review
    python analyze.py --research-question "Pertanyaan riset" --dataset data.csv --mode data-analysis
"""

import argparse
import hashlib
import json
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Journal Analysis System")
    parser.add_argument("input", nargs="?", help="PDF file or URL/DOI")
    parser.add_argument("--mode", required=True, choices=["read", "review", "full", "gap", "data-analysis", "generate", "compare"], help="Analysis mode")
    parser.add_argument("--input-text", help="Input text directly")
    parser.add_argument("--no-limit", action="store_true", help="Bypass token budget limit")
    parser.add_argument("--research-question", help="Research question for data-analysis or gap mode")
    parser.add_argument("--dataset", help="CSV/Excel dataset file for data-analysis mode")
    parser.add_argument("--prompt", help="Research topic/prompt for generate mode")
    parser.add_argument("--methodology", help="Requested methodology for generate mode")
    parser.add_argument("--citation-style", help="Citation style for generate mode (default: APA7)")
    parser.add_argument("--compare", nargs="*", help="Additional paper files to compare with")
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

    if args.mode == "gap":
        reader_result = _run_reader(article, cache, content_hash, config, router)
        results["reader"] = reader_result
        gap_result = _run_gap_analyzer(article, reader_result, cache, content_hash, config, router)
        results["gap_analyzer"] = gap_result

    if args.mode == "data-analysis":
        da_result = _run_data_analysis(args, cache, content_hash, config, router)
        results["data_analysis"] = da_result

    if args.mode == "generate":
        reader_result = _run_reader(article, cache, content_hash, config, router)
        results["reader"] = reader_result
        gap_result = _run_gap_analyzer(article, reader_result, cache, content_hash, config, router)
        results["gap_analyzer"] = gap_result
        gen_results = _run_generate(args, article, reader_result, gap_result, cache, content_hash, config, router)
        results.update(gen_results)

    if args.mode == "compare":
        all_articles = [article]
        if args.compare:
            from types import SimpleNamespace
            for compare_file in args.compare:
                compare_article = _parse_input(SimpleNamespace(input=compare_file, input_text=None))
                if compare_article:
                    all_articles.append(compare_article)
        comparison_result = _run_compare(args, all_articles, cache, content_hash, config, router)
        results["comparison"] = comparison_result

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


def _run_gap_analyzer(article, reader_result, cache, content_hash, config, router):
    from workers.gap_analyzer_worker import GapAnalyzerWorker

    cached = cache.get_analysis(content_hash, "gap_analyzer")
    if cached:
        return {"status": "success", "data": cached}

    model = router.get_model_name(router.select_model("gap_analysis", article.word_count))
    reader_summary = reader_result["data"]["summary"] if reader_result and reader_result["status"] == "success" else None

    worker = GapAnalyzerWorker()
    result = worker.run(article, reader_summary=reader_summary, model=model)

    if result is None:
        return {"status": "failed", "error": "Gap Analyzer gagal"}

    cache.set_analysis(content_hash, "gap_analyzer", result)
    return {"status": "success", "data": result}


def _run_generate(args, article, reader_result, gap_result, cache, content_hash, config, router):
    from workers.generator_worker import GeneratorWorker
    from workers.self_review_worker import SelfReviewWorker

    results = {}

    # Check cache for draft
    cached_draft = cache.get_analysis(content_hash, "generator")
    if cached_draft:
        results["generator"] = {"status": "success", "data": cached_draft}
    else:
        model = router.get_model_name(router.select_model("generate_article", article.word_count))
        reader_summaries = [reader_result["data"]["summary"]] if reader_result and reader_result["status"] == "success" else []
        gap_text = gap_result["data"].get("gap_text", "") if gap_result and gap_result["status"] == "success" else ""

        worker = GeneratorWorker()
        draft_result = worker.run(
            research_topic=args.prompt or "",
            reader_summaries=reader_summaries,
            gap_analysis=gap_text,
            methodology=args.methodology or "",
            citation_style=args.citation_style or "APA7",
            model=model,
        )

        if draft_result is None:
            results["generator"] = {"status": "failed", "error": "Generator gagal"}
        else:
            cache.set_analysis(content_hash, "generator", draft_result)
            results["generator"] = {"status": "success", "data": draft_result}

            # Self-review the draft
            cached_review = cache.get_analysis(content_hash, "self_review")
            if cached_review:
                results["self_review"] = {"status": "success", "data": cached_review}
            else:
                review_worker = SelfReviewWorker()
                review_result = review_worker.run(
                    draft_article=draft_result["draft"],
                    research_topic=args.prompt or "",
                )

                if review_result is None:
                    results["self_review"] = {"status": "failed", "error": "Self-review gagal"}
                else:
                    cache.set_analysis(content_hash, "self_review", review_result)
                    results["self_review"] = {"status": "success", "data": review_result}

    return results


def _run_data_analysis(args, cache, content_hash, config, router):
    from workers.data_analysis_worker import DataAnalysisWorker

    cached = cache.get_analysis(content_hash, "data_analysis")
    if cached:
        return {"status": "success", "data": cached}

    model = router.get_model_name(router.select_model("data_analysis_own", 1000))

    worker = DataAnalysisWorker()
    result = worker.run(
        research_question=args.research_question or "",
        dataset_description=args.dataset or "",
        statistical_results="",
    )

    if result is None:
        return {"status": "failed", "error": "Data Analysis gagal"}

    cache.set_analysis(content_hash, "data_analysis", result)
    return {"status": "success", "data": result}


def _run_compare(args, articles, cache, content_hash, config, router):
    from workers.comparison_worker import ComparisonWorker

    cached = cache.get_analysis(content_hash, "comparison")
    if cached:
        return {"status": "success", "data": cached}

    papers = []
    for art in articles:
        paper = {"title": art.metadata.get("title", "Unknown")}
        if art.sections.get("abstract"):
            paper["summary"] = art.sections["abstract"][:500]
        if art.methodology_type:
            paper["methodology"] = art.methodology_type
        if art.key_findings:
            paper["key_findings"] = art.key_findings
        papers.append(paper)

    model = router.get_model_name(ModelTier.HEAVY)
    worker = ComparisonWorker()
    result = worker.run(papers, model=model)

    if result is None:
        return {"status": "failed", "error": "Comparison gagal"}

    cache.set_analysis(content_hash, "comparison", result)
    return {"status": "success", "data": result}


def _estimate_tokens(word_count: int, mode: str) -> int:
    """Rough estimate: 1 word ≈ 1.3 tokens for input, plus output tokens."""
    input_tokens = int(word_count * 1.3)
    output_multiplier = {"read": 2, "review": 5, "full": 7}.get(mode, 3)
    return input_tokens + (input_tokens * output_multiplier // 10)


if __name__ == "__main__":
    main()
