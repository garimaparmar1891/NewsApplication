import pytest
from unittest.mock import Mock, patch
import sys
import os
from flask import Flask

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@pytest.fixture(autouse=True, scope="session")
def patch_db_utils():
    with patch("utils.db.get_db_connection"), \
         patch("utils.db.execute_write_query"), \
         patch("utils.db.fetch_one_query"), \
         patch("utils.db.fetch_all_query"), \
         patch("utils.db.fetch_all_query_with_params"):
        yield

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    return app

@pytest.fixture
def app_context(app):
    with app.app_context():
        yield app

@pytest.fixture
def mock_admin_repository():
    with patch('services.admin_service.AdminRepository') as mock_repo:
        yield mock_repo.return_value

@pytest.fixture
def sample_external_servers():
    return [
        {
            "id": 1,
            "name": "NewsAPI",
            "api_key": "test_api_key_1",
            "base_url": "https://newsapi.org/v2/",
            "is_active": 1,
            "last_accessed": "2024-01-01 10:00:00"
        },
        {
            "id": 2,
            "name": "TheNewsAPI",
            "api_key": "test_api_key_2",
            "base_url": "https://api.thenewsapi.com/v1/",
            "is_active": 0,
            "last_accessed": "2024-01-02 11:00:00"
        }
    ]

@pytest.fixture
def sample_categories():
    return [
        {
            "id": 1,
            "name": "Technology"
        },
        {
            "id": 2,
            "name": "Sports"
        },
        {
            "id": 3,
            "name": "Business"
        }
    ]

@pytest.fixture
def sample_keywords():
    return [
        {
            "id": 1,
            "word": "AI",
            "category_id": 1
        },
        {
            "id": 2,
            "word": "Football",
            "category_id": 2
        }
    ]
