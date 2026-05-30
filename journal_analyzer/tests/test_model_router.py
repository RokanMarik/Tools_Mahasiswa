from models.model_router import ModelRouter, ModelTier


def test_light_tier_for_parse():
    router = ModelRouter()
    tier = router.select_model("parse", input_size=1000)
    assert tier == ModelTier.LIGHT


def test_light_tier_for_metadata():
    router = ModelRouter()
    tier = router.select_model("extract_metadata", input_size=500)
    assert tier == ModelTier.LIGHT


def test_medium_tier_for_small_summary():
    router = ModelRouter()
    tier = router.select_model("summarize", input_size=3000)
    assert tier == ModelTier.MEDIUM


def test_heavy_tier_for_large_summary():
    router = ModelRouter()
    tier = router.select_model("summarize", input_size=10000)
    assert tier == ModelTier.HEAVY


def test_heavy_tier_for_critical_appraisal():
    router = ModelRouter()
    tier = router.select_model("critical_appraisal", input_size=5000)
    assert tier == ModelTier.HEAVY


def test_heavy_tier_for_generate():
    router = ModelRouter()
    tier = router.select_model("generate_article", input_size=8000)
    assert tier == ModelTier.HEAVY


def test_medium_for_gap_simple():
    router = ModelRouter()
    tier = router.select_model("gap_analysis", input_size=2000, complexity_hint="simple")
    assert tier == ModelTier.MEDIUM


def test_heavy_for_gap_complex():
    router = ModelRouter()
    tier = router.select_model("gap_analysis", input_size=2000, complexity_hint="complex")
    assert tier == ModelTier.HEAVY


def test_medium_for_data_analysis():
    router = ModelRouter()
    tier = router.select_model("data_analysis_own", input_size=1000)
    assert tier == ModelTier.MEDIUM


def test_get_model_name():
    router = ModelRouter(
        models={
            "light": "google/gemini-flash",
            "medium": "anthropic/claude-sonnet",
            "heavy": "anthropic/claude-opus",
        }
    )
    assert router.get_model_name(ModelTier.LIGHT) == "google/gemini-flash"
    assert router.get_model_name(ModelTier.HEAVY) == "anthropic/claude-opus"
