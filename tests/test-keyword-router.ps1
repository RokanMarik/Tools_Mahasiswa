#requires -Module Pester

BeforeAll {
    . "$PSScriptRoot/../scripts/keyword-router.ps1"
}

Describe "Get-TaskComplexity" {
    Context "berat detection - English keywords" {
        It "detects 'architecture' as berat" {
            Get-TaskComplexity "Design the system architecture" | Should -Be "auto-berat"
        }
        It "detects 'complex' as berat" {
            Get-TaskComplexity "Build a complex multi-step pipeline" | Should -Be "auto-berat"
        }
        It "detects 'refactor entire' as berat" {
            Get-TaskComplexity "Refactor entire codebase to use new pattern" | Should -Be "auto-berat"
        }
        It "detects 'build from scratch' as berat" {
            Get-TaskComplexity "Build from scratch a new authentication module" | Should -Be "auto-berat"
        }
        It "detects 'end-to-end' as berat" {
            Get-TaskComplexity "Implement end-to-end testing framework" | Should -Be "auto-berat"
        }
        It "detects 'major refactor' as berat" {
            Get-TaskComplexity "Major refactor of the data layer" | Should -Be "auto-berat"
        }
    }

    Context "berat detection - Indonesian keywords" {
        It "detects 'arsitektur' as berat" {
            Get-TaskComplexity "Rancang arsitektur sistem baru" | Should -Be "auto-berat"
        }
        It "detects 'kompleks' as berat" {
            Get-TaskComplexity "Buat fitur yang kompleks" | Should -Be "auto-berat"
        }
        It "detects 'buat dari nol' as berat" {
            Get-TaskComplexity "Buat dari nol modul pembayaran" | Should -Be "auto-berat"
        }
        It "detects 'refactor total' as berat" {
            Get-TaskComplexity "Refactor total semua endpoint API" | Should -Be "auto-berat"
        }
    }

    Context "sedang detection - English keywords" {
        It "detects 'review' as sedang" {
            Get-TaskComplexity "Review this pull request" | Should -Be "auto-sedang"
        }
        It "detects 'fix bug' as sedang" {
            Get-TaskComplexity "Fix bug in authentication flow" | Should -Be "auto-sedang"
        }
        It "detects 'optimize' as sedang" {
            Get-TaskComplexity "Optimize database query performance" | Should -Be "auto-sedang"
        }
        It "detects 'code review' as sedang" {
            Get-TaskComplexity "Do a code review on this PR" | Should -Be "auto-sedang"
        }
        It "detects 'troubleshoot' as sedang" {
            Get-TaskComplexity "Troubleshoot the deployment issue" | Should -Be "auto-sedang"
        }
    }

    Context "sedang detection - Indonesian keywords" {
        It "detects 'rangkum' as sedang" {
            Get-TaskComplexity "Rangkum dokumen ini" | Should -Be "auto-sedang"
        }
        It "detects 'perbaiki' as sedang" {
            Get-TaskComplexity "Perbaiki bug di halaman login" | Should -Be "auto-sedang"
        }
        It "detects 'bandingkan' as sedang" {
            Get-TaskComplexity "Bandingkan kedua pendekatan ini" | Should -Be "auto-sedang"
        }
        It "detects 'analisa' as sedang" {
            Get-TaskComplexity "Analisa performa query ini" | Should -Be "auto-sedang"
        }
    }

    Context "ringan default" {
        It "defaults to ringan for simple translation" {
            Get-TaskComplexity "Translate hello world to Indonesian" | Should -Be "auto-ringan"
        }
        It "defaults to ringan for simple greeting" {
            Get-TaskComplexity "What is 2+2?" | Should -Be "auto-ringan"
        }
        It "defaults to ringan for short prompt" {
            Get-TaskComplexity "Say hi" | Should -Be "auto-ringan"
        }
        It "defaults to ringan for translation task" {
            Get-TaskComplexity "Translate this paragraph to English" | Should -Be "auto-ringan"
        }
    }

    Context "case insensitivity" {
        It "matches ARCHITECTURE uppercase" {
            Get-TaskComplexity "Design the ARCHITECTURE" | Should -Be "auto-berat"
        }
        It "matches Review mixed case" {
            Get-TaskComplexity "Please ReViEw this code" | Should -Be "auto-sedang"
        }
    }

    Context "berat takes priority over sedang" {
        It "returns berat when both berat and sedang keywords present" {
            Get-TaskComplexity "Refactor entire architecture and review the code" | Should -Be "auto-berat"
        }
    }

    Context "validation and edge cases" {
        It "throws on empty string input" {
            { Get-TaskComplexity "" } | Should -Throw
        }

        It "returns ringan for whitespace-only input" {
            Get-TaskComplexity "   " | Should -Be "auto-ringan"
        }

        It "matches keyword adjacent to punctuation" {
            Get-TaskComplexity "Show me the architecture." | Should -Be "auto-berat"
        }

        It "does not match 'previewer' as 'review' (word boundary)" {
            Get-TaskComplexity "Open the log file previewer" | Should -Be "auto-ringan"
        }

        It "matches 'review' when it appears as a standalone word" {
            Get-TaskComplexity "Review the architecture previewer" | Should -Be "auto-berat"
        }

        It "does not match 'complexity' as 'complex' (word boundary)" {
            Get-TaskComplexity "Assess the complexity of this task" | Should -Be "auto-ringan"
        }

        It "does not match 'architectural' as 'architecture' (word boundary)" {
            Get-TaskComplexity "Review the architectural decisions" | Should -Be "auto-sedang"
        }
    }
}
