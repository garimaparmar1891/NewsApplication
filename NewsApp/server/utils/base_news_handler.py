from abc import ABC, abstractmethod
import requests

class BaseNewsHandler(ABC):
    
    def __init__(self, default_params=None):
        self.default_params = default_params or {}
    
    def fetch_articles(self, base_url, api_key, **kwargs):
        try:
            params = self._build_request_params(api_key, **kwargs)
            
            response = self._make_request(base_url, params)
            
            return self._extract_articles(response)
            
        except requests.RequestException as e:
            self._log_error(f"Request failed: {e}")
            return []
        except Exception as e:
            self._log_error(f"Unexpected error: {e}")
            return []
    
    def _make_request(self, base_url, params):
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        return response
    
    def _log_error(self, message):
        print(f"[{self.__class__.__name__}] {message}")
    
    @abstractmethod
    def _build_request_params(self, api_key, **kwargs):
        pass
    
    @abstractmethod
    def _extract_articles(self, response):
        pass
