from enum import Enum
from typing import Optional


class ModelTier(Enum):
    LIGHT = "light"
    MEDIUM = "medium"
    HEAVY = "heavy"


class ModelRouter:
    """Auto-selects 9Router models based on task type and input size.

    Routing rules (from spec §5):
    - parse, extract_metadata, format_check → Light
    - summarize, translate, structure_review (<5000 words) → Medium
    - summarize, translate, structure_review (>=5000 words) → Heavy
    - critical_appraisal, methodology_review, statistical_validation, generate_article → Heavy
    - gap_analysis (simple) → Medium, (complex) → Heavy
    - data_analysis_own → Medium
    """

    LIGHT_TASKS = {"parse", "extract_metadata", "format_check"}
    MEDIUM_SUMMARY_THRESHOLD = 5000  # words
    HEAVY_TASKS = {
        "critical_appraisal", "methodology_review",
        "statistical_validation", "generate_article",
    }

    DEFAULT_MODELS = {
        "light": "google/gemini-2.0-flash",
        "medium": "anthropic/claude-sonnet-4-20250514",
        "heavy": "anthropic/claude-opus-4-20250514",
    }

    def __init__(self, models: dict | None = None):
        self.models = models or dict(self.DEFAULT_MODELS)

    def select_model(
        self,
        task_type: str,
        input_size: int,
        complexity_hint: Optional[str] = None,
    ) -> ModelTier:
        """Select the appropriate model tier for a task."""
        if task_type in self.LIGHT_TASKS:
            return ModelTier.LIGHT

        if task_type in ("summarize", "translate", "structure_review"):
            if input_size < self.MEDIUM_SUMMARY_THRESHOLD:
                return ModelTier.MEDIUM
            return ModelTier.HEAVY

        if task_type in self.HEAVY_TASKS:
            return ModelTier.HEAVY

        if task_type == "gap_analysis":
            if complexity_hint == "simple":
                return ModelTier.MEDIUM
            return ModelTier.HEAVY

        if task_type == "data_analysis_own":
            return ModelTier.MEDIUM

        # Default to medium for unknown tasks
        return ModelTier.MEDIUM

    def get_model_name(self, tier: ModelTier) -> str:
        """Get the 9Router model name for a tier."""
        return self.models[tier.value]

    def get_fallback_chain(self, tier: ModelTier) -> list[ModelTier]:
        """Get the fallback chain for a tier."""
        all_tiers = [ModelTier.LIGHT, ModelTier.MEDIUM, ModelTier.HEAVY]
        idx = all_tiers.index(tier)
        # Return tier-down chain
        return all_tiers[max(0, idx - 1):idx] + all_tiers[idx + 1:]
