from abc import ABC, abstractmethod

class BaseNewsHandler(ABC):
    """
    Abstract base class that all news API handlers must inherit from.
    """

    @abstractmethod
    def fetch_articles(self, base_url: str, api_key: str, **kwargs) -> list:
        """
        Fetch articles from the external news API.

        Args:
            base_url (str): Base URL of the news API.
            api_key (str): API key/token for authentication.
            **kwargs: Optional parameters such as category, query, date range.

        Returns:
            list: A list of article dictionaries.
        """
        pass
