from typing import Any, Callable
from channelbuilder import DelayComponent

channel_creation_funcs: dict[str, Callable[..., DelayComponent]] = {}

def register(delay_type: str, creator_fn: Callable[..., DelayComponent]) -> None:
    """Register a new delay type."""
    channel_creation_funcs[delay_type] = creator_fn

def create(arguments: dict[str, Any]) -> DelayComponent:
    """Create a delay component of a specific type, given JSON data."""
    args_copy = arguments.copy()
    delay_type = args_copy.pop("type")
    try:
        creator_func = channel_creation_funcs[delay_type]
    except KeyError:
        raise ValueError(f"unknown delay type {delay_type!r}") from None
    return creator_func(**args_copy)

