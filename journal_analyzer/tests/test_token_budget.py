import pytest

from core.token_budget import TokenBudget, BudgetExceededError


def test_default_budget():
    budget = TokenBudget()
    assert budget.daily_limit == 50000
    assert budget.used_today == 0


def test_custom_budget():
    budget = TokenBudget(daily_limit=10000)
    assert budget.daily_limit == 10000


def test_add_usage():
    budget = TokenBudget(daily_limit=1000)
    budget.add_usage(500)
    assert budget.used_today == 500
    assert budget.remaining == 500


def test_check_within_budget():
    budget = TokenBudget(daily_limit=1000, used_today=400)
    assert budget.check_available(500)


def test_check_exceeds_budget():
    budget = TokenBudget(daily_limit=1000, used_today=800)
    assert not budget.check_available(300)


def test_check_exact_boundary():
    """Test exact boundary: remaining == requested should pass."""
    budget = TokenBudget(daily_limit=1000, used_today=500)
    assert budget.check_available(500)


def test_exceed_raises_error():
    budget = TokenBudget(daily_limit=1000, used_today=800)
    with pytest.raises(BudgetExceededError):
        budget.reserve(300)


def test_reserve_within_budget():
    budget = TokenBudget(daily_limit=1000, used_today=400)
    budget.reserve(500)
    assert budget.used_today == 900


def test_remaining():
    budget = TokenBudget(daily_limit=10000, used_today=3000)
    assert budget.remaining == 7000


def test_reset():
    budget = TokenBudget(daily_limit=1000, used_today=500)
    budget.reset()
    assert budget.used_today == 0


def test_get_task_budget_known_mode():
    budget = TokenBudget()
    assert budget.get_task_budget("read") == 5000
    assert budget.get_task_budget("review") == 15000
    assert budget.get_task_budget("full") == 30000


def test_get_task_budget_unknown_mode():
    budget = TokenBudget()
    assert budget.get_task_budget("unknown_mode") == TokenBudget.DEFAULT_TASK_BUDGET
