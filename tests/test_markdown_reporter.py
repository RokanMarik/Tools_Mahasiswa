import os
import sys
import tempfile

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.markdown_reporter import MarkdownReporter


def test_generate_report_creates_file():
    """Test that generate_report creates a markdown file"""
    with tempfile.TemporaryDirectory() as tmpdir:
        reporter = MarkdownReporter()
        
        results = {
            "questions": [
                {
                    "question": "Test question",
                    "papers": [
                        {"title": "Paper 1", "url": "http://example.com", "content": "Content"}
                    ],
                    "status": "success",
                    "errors": []
                }
            ],
            "total_papers_found": 1,
            "total_errors": 0,
            "processing_status": "completed"
        }
        
        output_file = os.path.join(tmpdir, "report.md")
        reporter.generate_report(results, output_file)
        
        assert os.path.exists(output_file)
        with open(output_file, 'r', encoding='utf-8') as f:
            content = f.read()
            assert "Test question" in content
            assert "Paper 1" in content
        print("[PASS] test_generate_report_creates_file passed")


def test_report_contains_all_sections():
    """Test that report contains all required sections"""
    with tempfile.TemporaryDirectory() as tmpdir:
        reporter = MarkdownReporter()
        
        results = {
            "questions": [
                {
                    "question": "Test question",
                    "papers": [{"title": "Paper 1", "url": "http://example.com", "content": "Content"}],
                    "status": "success",
                    "errors": []
                }
            ],
            "total_papers_found": 1,
            "total_errors": 0,
            "processing_status": "completed"
        }
        
        output_file = os.path.join(tmpdir, "report.md")
        reporter.generate_report(results, output_file)
        
        with open(output_file, 'r', encoding='utf-8') as f:
            content = f.read()
            assert "Journal Research Report" in content
            assert "Research Question 1" in content
            assert "Metadata" in content
            assert "Total Questions" in content
        print("[PASS] test_report_contains_all_sections passed")


def test_report_handles_multiple_questions():
    """Test report generation with multiple questions"""
    with tempfile.TemporaryDirectory() as tmpdir:
        reporter = MarkdownReporter()
        
        results = {
            "questions": [
                {
                    "question": "Question 1",
                    "papers": [{"title": "Paper 1", "url": "http://example.com/1", "content": "Content 1"}],
                    "status": "success",
                    "errors": []
                },
                {
                    "question": "Question 2",
                    "papers": [{"title": "Paper 2", "url": "http://example.com/2", "content": "Content 2"}],
                    "status": "success",
                    "errors": []
                }
            ],
            "total_papers_found": 2,
            "total_errors": 0,
            "processing_status": "completed"
        }
        
        output_file = os.path.join(tmpdir, "report.md")
        reporter.generate_report(results, output_file)
        
        with open(output_file, 'r', encoding='utf-8') as f:
            content = f.read()
            assert "Research Question 1" in content
            assert "Research Question 2" in content
            assert "Question 1" in content
            assert "Question 2" in content
            assert "Total Questions" in content
        print("[PASS] test_report_handles_multiple_questions passed")


def test_report_handles_errors():
    """Test report generation with errors"""
    with tempfile.TemporaryDirectory() as tmpdir:
        reporter = MarkdownReporter()
        
        results = {
            "questions": [
                {
                    "question": "Failed question",
                    "papers": [],
                    "status": "error",
                    "errors": ["API Error", "Network timeout"]
                }
            ],
            "total_papers_found": 0,
            "total_errors": 2,
            "processing_status": "completed"
        }
        
        output_file = os.path.join(tmpdir, "report.md")
        reporter.generate_report(results, output_file)
        
        with open(output_file, 'r', encoding='utf-8') as f:
            content = f.read()
            assert "error" in content.lower()
            assert "API Error" in content
            assert "Total Errors" in content
        print("[PASS] test_report_handles_errors passed")


def test_report_handles_no_papers():
    """Test report generation when no papers found"""
    with tempfile.TemporaryDirectory() as tmpdir:
        reporter = MarkdownReporter()
        
        results = {
            "questions": [
                {
                    "question": "No results question",
                    "papers": [],
                    "status": "no_results",
                    "errors": ["No papers found after retry"]
                }
            ],
            "total_papers_found": 0,
            "total_errors": 1,
            "processing_status": "completed"
        }
        
        output_file = os.path.join(tmpdir, "report.md")
        reporter.generate_report(results, output_file)
        
        with open(output_file, 'r', encoding='utf-8') as f:
            content = f.read()
            assert "No papers found" in content
        print("[PASS] test_report_handles_no_papers passed")


if __name__ == "__main__":
    test_generate_report_creates_file()
    test_report_contains_all_sections()
    test_report_handles_multiple_questions()
    test_report_handles_errors()
    test_report_handles_no_papers()
    print("\n[SUCCESS] All MarkdownReporter tests passed!")
