#requires -Version 5.1

# Pre-compile combined regex patterns at script load time
$script:beratKeywords = @(
    "architecture", "complex", "design system", "refactor entire",
    "debug difficult", "build feature", "implement from scratch",
    "multi-step", "deep analysis", "write extensive",
    "arsitektur", "kompleks", "buat dari nol", "refactor total",
    "build from scratch", "full system", "end-to-end",
    "complete rewrite", "major refactor"
)

$script:sedangKeywords = @(
    "review", "summarize", "explain", "analyze", "fix bug",
    "update", "modify", "compare", "optimize", "refactor",
    "rangkum", "perbaiki", "bandingkan", "analisa", "jelaskan",
    "code review", "troubleshoot", "investigate", "improve"
)

$escapedBerat = $script:beratKeywords | ForEach-Object { [Regex]::Escape($_) }
$script:beratRegex = [Regex]::new(
    "\b($($escapedBerat -join '|'))\b",
    [System.Text.RegularExpressions.RegexOptions]::IgnoreCase
)

$escapedSedang = $script:sedangKeywords | ForEach-Object { [Regex]::Escape($_) }
$script:sedangRegex = [Regex]::new(
    "\b($($escapedSedang -join '|'))\b",
    [System.Text.RegularExpressions.RegexOptions]::IgnoreCase
)

function Get-TaskComplexity {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)]
        [ValidateNotNullOrEmpty()]
        [string]$Prompt
    )

    # Check berat first (higher priority)
    if ($script:beratRegex.IsMatch($Prompt)) {
        return "auto-berat"
    }

    # Check sedang
    if ($script:sedangRegex.IsMatch($Prompt)) {
        return "auto-sedang"
    }

    # Default: ringan
    return "auto-ringan"
}
