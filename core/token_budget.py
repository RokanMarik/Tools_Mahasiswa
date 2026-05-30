class BudgetExceededError(Exception):
    """Raised when token budget is exceeded."""
    pass


class TokenBudget:
    """Tracks and manages daily token usage with per-task limits."""

    DEFAULT_DAILY_LIMIT = 50000
    DEFAULT_PER_TASK = {
        "read": 5000,
        "review": 15000,
        "full": 30000,
        "generate": 40000,
        "data_analysis": 10000,
    }

    def __init__(
        self,
        daily_limit: int = DEFAULT_DAILY_LIMIT,
        per_task: dict | None = None,
        used_today: int = 0,
    ):
        self.daily_limit = daily_limit
        self.per_task = per_task or dict(self.DEFAULT_PER_TASK)
        self._used_today = used_today

    @property
    def used_today(self) -> int:
        return self._used_today

    @used_today.setter
    def used_today(self, value: int):
        self._used_today = value

    @property
    def remaining(self) -> int:
        return max(0, self.daily_limit - self._used_today)

    def check_available(self, tokens: int) -> bool:
        """Check if adding `tokens` would stay within budget."""
        return self._used_today + tokens <= self.daily_limit

    def reserve(self, tokens: int) -> None:
        """Reserve tokens. Raises BudgetExceededError if over limit."""
        if not self.check_available(tokens):
            raise BudgetExceededError(
                f"Token budget exceeded: need {tokens}, "
                f"have {self.remaining} of {self.daily_limit}"
            )
        self._used_today += tokens

    def add_usage(self, tokens: int) -> None:
        """Add token usage. Does NOT raise — just tracks."""
        self._used_today += tokens

    def get_task_budget(self, mode: str) -> int:
        """Get per-task budget for a mode."""
        return self.per_task.get(mode, 10000)

    def reset(self) -> None:
        """Reset daily counter."""
        self._used_today = 0
