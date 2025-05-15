from dataclasses import dataclass
from typing import Optional

@dataclass
class Joke:
    id: str
    text: str
    category: str
    rating: Optional[float] = None
    image_url: Optional[str] = None

@dataclass
class UserJoke:
    id: int
    text: str
    category: str
    created_at: str