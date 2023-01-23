from dataclasses import dataclass


@dataclass
class MALTokenInfo:
    token_type: str
    expires_in: int
    access_token: str
    refresh_token: str
