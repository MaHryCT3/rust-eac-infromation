from typing import NamedTuple, Optional
from datetime import datetime


class EACInfo(NamedTuple):
    steamid: int
    is_ban: bool
    ban_time: Optional[datetime] = None
    days_since_ban: int = None
    post_link: Optional[str] = None
    nexus_link: Optional[str] = None
