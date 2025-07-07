import pytest
from unittest.mock import Mock, patch
from datetime import datetime
from repositories.admin_repository import AdminRepository
from queries import admin_queries, category_queries
from constants import messages


class TestAdminRepository:
    
    @pytest.fixture
    def admin_repository(self):
        return AdminRepository()
    
    @pytest.fixture
    def mock_row(self):
        row = Mock()
        row.Id = 1
        row.Name = "TestServer"
        row.ApiKey = "test_key"
        row.BaseUrl = "https://test.com"
        row.IsActive = 1
        row.LastAccessed = datetime.now()
        return row
    
    @pytest.fixture
    def mock_category_row(self):
        row = Mock()
        row.Id = 1
        row.Name = "Technology"
        return row
    
    @pytest.fixture
    def mock_keyword_row(self):
        row = Mock()
        row.Id = 1
        row.Word = "AI"
        row.CategoryId = 1
        return row

    @patch('repositories.admin_repository.fetch_all_query')
    def test_get_external_servers_returns_mapped_data(self, mock_fetch_all, admin_repository, mock_row):
        expected_result = [{'id': 1, 'name': 'TestServer', 'api_key': 'test_key', 'base_url': 'https://test.com', 'is_active': 1, 'last_accessed': mock_row.LastAccessed}]
        mock_fetch_all.return_value = expected_result
        
        result = admin_repository.get_external_servers()
        
        assert result[0]['name'] == "TestServer"

    @patch('repositories.admin_repository.execute_write_query')
    def test_update_external_server_with_name_field(self, mock_execute, admin_repository):
        mock_execute.return_value = 1
        data = {"Name": "UpdatedServer"}
        
        result = admin_repository.update_external_server(1, data)
        
        assert result == 1

    @patch('repositories.admin_repository.fetch_all_query')
    def test_get_categories_returns_mapped_data(self, mock_fetch_all, admin_repository, mock_category_row):
        expected_result = [{'id': 1, 'name': 'Technology'}]
        mock_fetch_all.return_value = expected_result
        
        result = admin_repository.get_categories()
        
        assert result[0]['name'] == "Technology"

    @patch('repositories.admin_repository.execute_write_query')
    def test_add_category_executes_insert_query(self, mock_execute, admin_repository):
        mock_execute.return_value = 1
        
        result = admin_repository.add_category("NewCategory")
        
        assert result == 1

    @patch('repositories.admin_repository.fetch_all_query')
    def test_get_keywords_returns_mapped_data(self, mock_fetch_all, admin_repository, mock_keyword_row):
        expected_result = [{'id': 1, 'word': 'AI', 'category_id': 1}]
        mock_fetch_all.return_value = expected_result
        
        result = admin_repository.get_keywords()
        
        assert result[0]['word'] == "AI"

    @patch('repositories.admin_repository.execute_write_query')
    def test_add_keyword_executes_insert_query(self, mock_execute, admin_repository):
        mock_execute.return_value = 1
        
        result = admin_repository.add_keyword("NewKeyword", 1)
        
        assert result == 1

    @patch('repositories.admin_repository.execute_write_query')
    def test_delete_keyword_executes_delete_query(self, mock_execute, admin_repository):
        mock_execute.return_value = 1
        
        result = admin_repository.delete_keyword("TestKeyword")
        
        assert result == 1

    def test_build_update_params_with_name_field(self, admin_repository):
        data = {"Name": "UpdatedName"}
        
        update_fields, params = admin_repository._build_update_params(data)
        
        assert "Name = ?" in update_fields

    def test_build_update_params_with_api_key_field(self, admin_repository):
        data = {"Api_key": "new_api_key"}
        
        update_fields, params = admin_repository._build_update_params(data)
        
        assert "ApiKey = ?" in update_fields

    def test_build_update_params_with_base_url_field(self, admin_repository):
        data = {"Base_Url": "https://newurl.com"}
        
        update_fields, params = admin_repository._build_update_params(data)
        
        assert "BaseUrl = ?" in update_fields

    def test_build_update_params_with_is_active_field(self, admin_repository):
        data = {"Is_Active": 1}
        
        update_fields, params = admin_repository._build_update_params(data)
        
        assert "IsActive = ?" in update_fields

    def test_map_external_server_returns_correct_structure(self, admin_repository, mock_row):
        result = admin_repository._map_external_server(mock_row)
        
        assert result['id'] == 1

    def test_map_category_returns_correct_structure(self, admin_repository, mock_category_row):
        result = admin_repository._map_category(mock_category_row)
        
        assert result['id'] == 1

    def test_map_keyword_returns_correct_structure(self, admin_repository, mock_keyword_row):
        result = admin_repository._map_keyword(mock_keyword_row)
        
        assert result['id'] == 1
