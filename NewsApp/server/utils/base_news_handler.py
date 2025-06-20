from abc import ABC, abstractmethod

class BaseNewsHandler(ABC):
    @abstractmethod
    def fetch_articles(self, base_url, api_key, **kwargs):
        pass
