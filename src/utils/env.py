import os
from datetime import datetime
from typing import (
    cast,
    Optional,
    Type,
    TypeVar,
    overload,
)

from dotenv import load_dotenv

T = TypeVar("T", str, int, datetime)


@overload
def _get_env(name: str, type_: Type[T]) -> T: ...


@overload
def _get_env(name: str, type_: Type[T], *, optional: bool = False) -> T: ...


@overload
def _get_env(name: str, type_: Type[T], *, optional: bool) -> Optional[T]: ...


def _get_env(name: str, type_: Type[T], optional: bool = False) -> Optional[T]:
    """
    Get an environment variable and parse it as a specific type.

    Arguments:
        name (`str`): The name of the environment variable.
        type_ (`Type[T]`): The type to parse the environment variable as.
        optional (`bool`, optional): Whether the environment variable is optional.

    Returns:
        `Optional[T]`: The parsed value, or `None` if the environment variable is not set.

    Raises:
        `KeyError`: If the environment variable is required but not set.
        `ValueError`: If the environment variable cannot be parsed as the requested type.
        `TypeError`: If the requested type is not supported.
    """
    value = os.getenv(name)

    if value is None:
        # Not set
        if not optional:
            raise KeyError(f"Missing required environment variable: {name}")
        return None

    if type_ is str:
        return cast(T, value)

    if type_ is int:
        try:
            return cast(T, int(value))
        except ValueError as e:
            raise ValueError(
                f"Environment variable '{name}' cannot be parsed as int. "
                f"Raw value: '{value}'"
            ) from e

    if type_ is datetime:
        try:
            # Parse as an ISO-8601 string, e.g., "2021-01-01T12:34:56"
            return cast(T, datetime.fromisoformat(value))
        except ValueError as e:
            raise ValueError(
                f"Environment variable '{name}' cannot be parsed as datetime. "
                f"Expected ISO-8601 string, got: '{value}'"
            ) from e

    # If there's a type we haven't covered, raise an error or handle it as needed
    raise TypeError(f"Unsupported type requested: {type_}")


# Load environment variables from a .env file, for local development
load_dotenv()

AIRTABLE_API_KEY = _get_env("AIRTABLE_API_KEY", str)
AIRTABLE_BASE_ID = _get_env("AIRTABLE_BASE_ID", str)
