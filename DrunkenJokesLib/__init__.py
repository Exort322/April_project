from datetime import datetime
from .database import DatabaseManager
from .api_client import JokeAPIClient, ImageAPIClient
from .models import Joke, UserJoke
from .exceptions import *

class JokeLibrary:
    def __init__(self, db_name: str = 'jokes.db'):
        self.db = DatabaseManager(db_name)
        self.joke_client = JokeAPIClient()
        self.image_client = ImageAPIClient()
        self.categories = [
            'Programming', 'Misc', 'Dark',
            'Pun', 'Spooky', 'Christmas'
        ]

    def get_joke_of_the_day(self) -> Joke:
        db_joke = self.db.get_joke_of_the_day()
        if db_joke:
            return Joke(
                id='local',
                text=db_joke[0],
                category='top_rated',
                rating=db_joke[1]
            )
        return self._fetch_joke()

    def get_joke_with_image(self, category: str = 'Any', image_keywords: str = 'funny') -> Joke:
        joke = self._fetch_joke(category)
        joke.image_url = self.image_client.get_random_image(image_keywords)
        return joke

    def add_user_joke(self, text: str, category: str = 'Custom') -> UserJoke:
        joke_id = self.db.add_user_joke(text, category)
        return UserJoke(
            id=joke_id,
            text=text,
            category=category,
            created_at=str(datetime.now())
        )

    def _fetch_joke(self, category: str = 'Any') -> Joke:
        api_joke = self.joke_client.get_joke(category)
        if api_joke:
            self.db.add_to_history(api_joke['id'], api_joke['text'])
            return Joke(**api_joke)
        raise JokeAPIError("Failed to fetch joke from API")

    def rate_joke(self, joke_id: str, rating: int):
        if not 1 <= rating <= 5:
            raise ValueError("Rating must be between 1 and 5")
        self.db.rate_joke(joke_id, rating)

    def get_categories(self) -> list:
        return self.categories.copy()