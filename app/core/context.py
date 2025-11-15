from contextvars import ContextVar

# Thread-safe context variable for current user ID
current_user_id: ContextVar[int | None] = ContextVar("current_user_id", default=None)
