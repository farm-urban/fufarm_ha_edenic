"""Types for tests."""

from typing import TypedDict


class EdenicCredentials(TypedDict):
    """Real Edenic credentials for live API tests."""

    org_key: str
    api_key: str
    device_label: str
