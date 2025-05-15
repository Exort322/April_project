import requests
from typing import Dict, Optional

class JokeAPIClient:
    BASE_URL = 'https://v2.jokeapi.dev/joke/'

    def get_joke(self, category: str = 'Any') -> Optional[Dict]:
        try:
            response = requests.get(f"{self.BASE_URL}{category}")
            response.raise_for_status()
            data = response.json()
            return {
                'id': data.get('id'),
                'text': '\n'.join([
                    data.get('setup', ''),
                    data.get('delivery', '')
                ]).strip(),
                'category': data.get('category')
            }
        except requests.exceptions.RequestException as e:
            print(f"Joke API Error: {e}")

class ImageAPIClient:
    def get_random_image(self, keywords: str = 'funny') -> Optional[str]:
        try:
            url = f"https://source.unsplash.com/random/800x600/?{keywords}"
            response = requests.get(url, allow_redirects=True)
            return response.url if response.status_code == 200 else None
        except Exception as e:
            print(f"Image API Error: {e}")
            return None