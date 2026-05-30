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
    assert budget.check_available(500) == True


def test_check_exceeds_budget():
    budget = TokenBudget(daily_limit=1000, used_today=800)
    assert budget.check_available(300) == False


def test_exceed_raises_error():
    budget = TokenBudget(daily_limit=1000, used_today=800)
    try:
        budget.reserve(300)
        assert False, "Should have raised BudgetExceededError"
    except BudgetExceededError:
        pass


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
