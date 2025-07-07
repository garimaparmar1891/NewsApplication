import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, date
from repositories.article_repository import ArticleRepository
from queries import article_queries as q
from queries import article_visibility_queries as avq
from queries import category_queries
from constants import messages


class TestArticleRepository:
    
    @pytest.fixture
    def article_repository(self):
        return ArticleRepository()
    
    @pytest.fixture
    def mock_article_row(self):
        return (
            1,
            "Test Article Title",
            "Test article content",
            "Test Source",
            "https://test.com/article",
            "Technology",
            "2024-01-01 10:00:00"
        )
    
    @pytest.fixture
    def mock_category_row(self):
        return (1, "Technology")
    
    @pytest.fixture
    def mock_read_history_row(self):
        return (1, "2024-01-01 10:00:00")
    
    @pytest.fixture
    def sample_article_data(self):
        return {
            "title": "Test Article",
            "content": "Test content",
            "source": "Test Source",
            "url": "https://test.com",
            "category_id": 1,
            "published_at": "2024-01-01 10:00:00",
            "server_id": 1,
            "is_hidden": 0
        }

    @patch('repositories.article_repository.fetch_all_query_with_params')
    def test_get_today_headlines_calls_fetch_with_correct_query(self, mock_fetch, article_repository):
        test_date = date(2024, 1, 1)
        mock_fetch.return_value = []
        
        article_repository.get_today_headlines(test_date)
        
        mock_fetch.assert_called_once_with(q.GET_TODAY_HEADLINES, article_repository._format_article_row, messages.DB_ERROR_GET_TODAY_HEADLINES, (test_date,))

    @patch('repositories.article_repository.fetch_all_query_with_params')
    def test_get_today_headlines_returns_formatted_articles(self, mock_fetch, article_repository, mock_article_row):
        mock_fetch.return_value = [mock_article_row]
        
        result = article_repository.get_today_headlines(date(2024, 1, 1))
        
        assert len(result) == 1

    @patch('repositories.article_repository.fetch_all_query_with_params')
    def test_get_today_headlines_handles_empty_result(self, mock_fetch, article_repository):
        mock_fetch.return_value = []
        
        result = article_repository.get_today_headlines(date(2024, 1, 1))
        
        assert result == []

    @patch('repositories.article_repository.fetch_all_query_with_params')
    def test_get_today_headlines_passes_correct_error_message(self, mock_fetch, article_repository):
        mock_fetch.return_value = []
        
        article_repository.get_today_headlines(date(2024, 1, 1))
        
        mock_fetch.assert_called_once_with(q.GET_TODAY_HEADLINES, article_repository._format_article_row, messages.DB_ERROR_GET_TODAY_HEADLINES, (date(2024, 1, 1),))

    @patch('repositories.article_repository.fetch_all_query_with_params')
    def test_search_articles_by_keyword_and_range_calls_fetch_with_correct_query(self, mock_fetch, article_repository):
        mock_fetch.return_value = []
        
        article_repository.search_articles_by_keyword_and_range("test", "2024-01-01", "2024-01-02")
        
        mock_fetch.assert_called_once_with(q.SEARCH_ARTICLES_BY_KEYWORD_AND_RANGE, article_repository._format_article_row, messages.DB_ERROR_SEARCH_ARTICLES, ("%test%", "%test%", "2024-01-01", "2024-01-02"))

    @patch('repositories.article_repository.fetch_all_query_with_params')
    def test_search_articles_by_keyword_and_range_returns_formatted_results(self, mock_fetch, article_repository, mock_article_row):
        mock_fetch.return_value = [mock_article_row]
        
        result = article_repository.search_articles_by_keyword_and_range("test", "2024-01-01", "2024-01-02")
        
        assert len(result) == 1

    @patch('repositories.article_repository.fetch_all_query_with_params')
    def test_search_articles_by_keyword_and_range_handles_empty_results(self, mock_fetch, article_repository):
        mock_fetch.return_value = []
        
        result = article_repository.search_articles_by_keyword_and_range("test", "2024-01-01", "2024-01-02")
        
        assert result == []

    @patch('repositories.article_repository.fetch_all_query_with_params')
    def test_search_articles_by_keyword_and_range_wraps_keyword_with_percent(self, mock_fetch, article_repository):
        mock_fetch.return_value = []
        
        article_repository.search_articles_by_keyword_and_range("test", "2024-01-01", "2024-01-02")
        
        mock_fetch.assert_called_once_with(q.SEARCH_ARTICLES_BY_KEYWORD_AND_RANGE, article_repository._format_article_row, messages.DB_ERROR_SEARCH_ARTICLES, ("%test%", "%test%", "2024-01-01", "2024-01-02"))

    @patch('repositories.article_repository.fetch_all_query_with_params')
    def test_get_articles_by_range_without_categories_calls_fetch_with_base_query(self, mock_fetch, article_repository):
        mock_fetch.return_value = []
        
        article_repository.get_articles_by_range("2024-01-01", "2024-01-02")
        
        expected_query = q.GET_ARTICLES_BY_RANGE_BASE.format(category_clause="")
        mock_fetch.assert_called_once_with(expected_query, article_repository._format_article_row, messages.DB_ERROR_GET_ARTICLES_BY_RANGE, ["2024-01-01", "2024-01-02"])

    @patch('repositories.article_repository.fetch_all_query_with_params')
    def test_get_articles_by_range_with_single_category_uses_equals_clause(self, mock_fetch, article_repository):
        mock_fetch.return_value = []
        
        article_repository.get_articles_by_range("2024-01-01", "2024-01-02", [1])
        
        expected_query = q.GET_ARTICLES_BY_RANGE_BASE.format(category_clause="AND A.CategoryId = ?")
        mock_fetch.assert_called_once_with(expected_query, article_repository._format_article_row, messages.DB_ERROR_GET_ARTICLES_BY_RANGE, ["2024-01-01", "2024-01-02", 1])

    @patch('repositories.article_repository.fetch_all_query_with_params')
    def test_get_articles_by_range_with_multiple_categories_uses_in_clause(self, mock_fetch, article_repository):
        mock_fetch.return_value = []
        
        article_repository.get_articles_by_range("2024-01-01", "2024-01-02", [1, 2, 3])
        
        expected_query = q.GET_ARTICLES_BY_RANGE_BASE.format(category_clause="AND A.CategoryId IN (?,?,?)")
        mock_fetch.assert_called_once_with(expected_query, article_repository._format_article_row, messages.DB_ERROR_GET_ARTICLES_BY_RANGE, ["2024-01-01", "2024-01-02", 1, 2, 3])

    @patch('repositories.article_repository.fetch_all_query_with_params')
    def test_get_articles_by_range_returns_formatted_results(self, mock_fetch, article_repository, mock_article_row):
        mock_fetch.return_value = [mock_article_row]
        
        result = article_repository.get_articles_by_range("2024-01-01", "2024-01-02")
        
        assert len(result) == 1

    @patch('repositories.article_repository.get_db_connection')
    def test_bulk_insert_articles_commits_successful_inserts(self, mock_connection, article_repository, sample_article_data):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = (1,)
        mock_connection.return_value.__enter__.return_value = mock_conn
        
        result = article_repository.bulk_insert_articles([sample_article_data])
        
        mock_conn.commit.assert_called_once()

    @patch('repositories.article_repository.get_db_connection')
    def test_bulk_insert_articles_returns_inserted_ids(self, mock_connection, article_repository, sample_article_data):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = (1,)
        mock_connection.return_value.__enter__.return_value = mock_conn
        
        result = article_repository.bulk_insert_articles([sample_article_data])
        
        assert result == [1]

    @patch('repositories.article_repository.get_db_connection')
    def test_bulk_insert_articles_rolls_back_on_exception(self, mock_connection, article_repository, sample_article_data):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.execute.side_effect = Exception("Database error")
        mock_connection.return_value.__enter__.return_value = mock_conn
        
        result = article_repository.bulk_insert_articles([sample_article_data])
        
        mock_conn.rollback.assert_called_once()

    @patch('repositories.article_repository.get_db_connection')
    def test_bulk_insert_articles_handles_missing_fetchone_result(self, mock_connection, article_repository, sample_article_data):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None
        mock_connection.return_value.__enter__.return_value = mock_conn
        
        result = article_repository.bulk_insert_articles([sample_article_data])
        
        assert result == []

    @patch('repositories.article_repository.execute_write_query')
    def test_record_article_read_calls_execute_with_correct_params(self, mock_execute, article_repository):
        mock_execute.return_value = True
        
        article_repository.record_article_read(1, 1)
        
        mock_execute.assert_called_once_with(q.INSERT_READ_HISTORY, (1, 1), messages.DB_ERROR_INSERT_READ_HISTORY)

    @patch('repositories.article_repository.execute_write_query')
    def test_record_article_read_returns_true_on_success(self, mock_execute, article_repository):
        mock_execute.return_value = True
        
        result = article_repository.record_article_read(1, 1)
        
        assert result is True

    @patch('repositories.article_repository.execute_write_query')
    def test_record_article_read_returns_false_on_exception(self, mock_execute, article_repository):
        mock_execute.side_effect = Exception("Database error")
        
        result = article_repository.record_article_read(1, 1)
        
        assert result is False

    @patch('repositories.article_repository.fetch_all_query')
    def test_get_all_categories_calls_fetch_with_correct_query(self, mock_fetch, article_repository):
        mock_fetch.return_value = []
        
        article_repository.get_all_categories()
        
        mock_fetch.assert_called_once_with(category_queries.GET_CATEGORIES, article_repository._format_category_row, messages.DB_ERROR_GET_CATEGORIES)

    @patch('repositories.article_repository.fetch_all_query')
    def test_get_all_categories_returns_formatted_categories(self, mock_fetch, article_repository, mock_category_row):
        mock_fetch.return_value = [mock_category_row]
        
        result = article_repository.get_all_categories()
        
        assert len(result) == 1

    @patch('repositories.article_repository.fetch_all_query')
    def test_get_all_categories_handles_empty_result(self, mock_fetch, article_repository):
        mock_fetch.return_value = []
        
        result = article_repository.get_all_categories()
        
        assert result == []

    @patch('repositories.article_repository.fetch_one_query')
    def test_get_article_by_id_calls_fetch_with_correct_params(self, mock_fetch, article_repository):
        mock_fetch.return_value = None
        
        article_repository.get_article_by_id(1)
        
        mock_fetch.assert_called_once_with(q.GET_ARTICLE_BY_ID, (1,), messages.DB_ERROR_GET_ARTICLE_BY_ID)

    @patch('repositories.article_repository.fetch_one_query')
    def test_get_article_by_id_returns_formatted_article_when_found(self, mock_fetch, article_repository, mock_article_row):
        mock_fetch.return_value = mock_article_row
        
        result = article_repository.get_article_by_id(1)
        
        assert result is not None

    @patch('repositories.article_repository.fetch_one_query')
    def test_get_article_by_id_returns_none_when_not_found(self, mock_fetch, article_repository):
        mock_fetch.return_value = None
        
        result = article_repository.get_article_by_id(1)
        
        assert result is None

    @patch('repositories.article_repository.fetch_all_query')
    def test_get_blocked_keywords_calls_fetch_with_correct_query(self, mock_fetch, article_repository):
        mock_fetch.return_value = []
        
        article_repository.get_blocked_keywords()
        
        mock_fetch.assert_called_once()
        args, kwargs = mock_fetch.call_args
        assert args[0] == avq.GET_BLOCKED_KEYWORDS
        assert args[2] == messages.DB_ERROR_GET_BLOCKED_KEYWORDS

    @patch('repositories.article_repository.fetch_all_query')
    def test_get_blocked_keywords_returns_keyword_list(self, mock_fetch, article_repository):
        mock_fetch.return_value = ["spam", "fake"]
        
        result = article_repository.get_blocked_keywords()
        
        assert result == ["spam", "fake"]

    @patch('repositories.article_repository.fetch_all_query')
    def test_get_blocked_keywords_handles_empty_result(self, mock_fetch, article_repository):
        mock_fetch.return_value = []
        
        result = article_repository.get_blocked_keywords()
        
        assert result == []

    @patch('repositories.article_repository.fetch_all_query')
    def test_get_all_articles_calls_fetch_with_correct_query(self, mock_fetch, article_repository):
        mock_fetch.return_value = []
        
        article_repository.get_all_articles()
        
        mock_fetch.assert_called_once_with(q.GET_ALL_ARTICLES, article_repository._format_article_row, messages.DB_ERROR_GET_ALL_ARTICLES)

    @patch('repositories.article_repository.fetch_all_query')
    def test_get_all_articles_returns_formatted_articles(self, mock_fetch, article_repository, mock_article_row):
        mock_fetch.return_value = [mock_article_row]
        
        result = article_repository.get_all_articles()
        
        assert len(result) == 1

    @patch('repositories.article_repository.fetch_all_query')
    def test_get_all_articles_handles_empty_result(self, mock_fetch, article_repository):
        mock_fetch.return_value = []
        
        result = article_repository.get_all_articles()
        
        assert result == []

    @patch('repositories.article_repository.fetch_one_query')
    def test_article_exists_by_title_calls_fetch_with_correct_params(self, mock_fetch, article_repository):
        mock_fetch.return_value = None
        
        article_repository.article_exists_by_title("Test Title")
        
        mock_fetch.assert_called_once_with(q.GET_ARTICLE_BY_TITLE, ("Test Title",))

    @patch('repositories.article_repository.fetch_one_query')
    def test_article_exists_by_title_returns_true_when_found(self, mock_fetch, article_repository):
        mock_fetch.return_value = (1,)
        
        result = article_repository.article_exists_by_title("Test Title")
        
        assert result is True

    @patch('repositories.article_repository.fetch_one_query')
    def test_article_exists_by_title_returns_false_when_not_found(self, mock_fetch, article_repository):
        mock_fetch.return_value = None
        
        result = article_repository.article_exists_by_title("Test Title")
        
        assert result is False

    @patch('repositories.article_repository.fetch_one_query')
    def test_article_exists_duplicate_calls_fetch_with_all_params_when_all_provided(self, mock_fetch, article_repository):
        mock_fetch.return_value = None
        
        article_repository.article_exists_duplicate("Test Title", "https://test.com", "2024-01-01")
        
        mock_fetch.assert_called_once_with(q.CHECK_ARTICLE_DUPLICATE, ("Test Title", "https://test.com", "2024-01-01"))

    @patch('repositories.article_repository.fetch_one_query')
    def test_article_exists_duplicate_falls_back_to_title_check_when_missing_params(self, mock_fetch, article_repository):
        mock_fetch.return_value = None
        
        article_repository.article_exists_duplicate("Test Title", None, None)
        
        mock_fetch.assert_called_once_with(q.GET_ARTICLE_BY_TITLE, ("Test Title",))

    @patch('repositories.article_repository.fetch_one_query')
    def test_article_exists_duplicate_returns_true_when_found(self, mock_fetch, article_repository):
        mock_fetch.return_value = (1,)
        
        result = article_repository.article_exists_duplicate("Test Title", "https://test.com", "2024-01-01")
        
        assert result is True

    @patch('repositories.article_repository.fetch_one_query')
    def test_article_exists_duplicate_returns_false_when_not_found(self, mock_fetch, article_repository):
        mock_fetch.return_value = None
        
        result = article_repository.article_exists_duplicate("Test Title", "https://test.com", "2024-01-01")
        
        assert result is False

    @patch('repositories.article_repository.fetch_all_query_with_params')
    def test_get_read_history_calls_fetch_with_correct_params(self, mock_fetch, article_repository):
        mock_fetch.return_value = []
        
        article_repository.get_read_history(1)
        
        mock_fetch.assert_called_once_with(q.GET_READ_HISTORY, article_repository._format_read_history_row, messages.DB_ERROR_GET_READ_HISTORY, (1,))

    @patch('repositories.article_repository.fetch_all_query_with_params')
    def test_get_read_history_returns_formatted_history(self, mock_fetch, article_repository, mock_read_history_row):
        mock_fetch.return_value = [mock_read_history_row]
        
        result = article_repository.get_read_history(1)
        
        assert len(result) == 1

    @patch('repositories.article_repository.fetch_all_query_with_params')
    def test_get_read_history_handles_empty_result(self, mock_fetch, article_repository):
        mock_fetch.return_value = []
        
        result = article_repository.get_read_history(1)
        
        assert result == []

    def test_format_article_row_returns_correct_structure(self, article_repository, mock_article_row):
        result = article_repository._format_article_row(mock_article_row)
        
        assert "Id" in result

    def test_format_article_row_maps_all_fields_correctly(self, article_repository, mock_article_row):
        result = article_repository._format_article_row(mock_article_row)
        
        assert result["Title"] == "Test Article Title"

    def test_format_category_row_returns_correct_structure(self, article_repository, mock_category_row):
        result = article_repository._format_category_row(mock_category_row)
        
        assert "Id" in result

    def test_format_category_row_maps_fields_correctly(self, article_repository, mock_category_row):
        result = article_repository._format_category_row(mock_category_row)
        
        assert result["Name"] == "Technology"

    def test_format_read_history_row_returns_correct_structure(self, article_repository, mock_read_history_row):
        result = article_repository._format_read_history_row(mock_read_history_row)
        
        assert "ArticleId" in result

    def test_format_read_history_row_maps_fields_correctly(self, article_repository, mock_read_history_row):
        result = article_repository._format_read_history_row(mock_read_history_row)
        
        assert result["ReadAt"] == "2024-01-01 10:00:00"

    def test_prepare_article_data_returns_correct_tuple(self, article_repository, sample_article_data):
        result = article_repository._prepare_article_data(sample_article_data)
        
        assert len(result) == 8

    def test_prepare_article_data_maps_title_correctly(self, article_repository, sample_article_data):
        result = article_repository._prepare_article_data(sample_article_data)
        
        assert result[0] == "Test Article"

    def test_prepare_article_data_maps_content_correctly(self, article_repository, sample_article_data):
        result = article_repository._prepare_article_data(sample_article_data)
        
        assert result[1] == "Test content"

    def test_prepare_article_data_maps_source_correctly(self, article_repository, sample_article_data):
        result = article_repository._prepare_article_data(sample_article_data)
        
        assert result[2] == "Test Source"

    def test_prepare_article_data_maps_url_correctly(self, article_repository, sample_article_data):
        result = article_repository._prepare_article_data(sample_article_data)
        
        assert result[3] == "https://test.com"

    def test_prepare_article_data_maps_category_id_correctly(self, article_repository, sample_article_data):
        result = article_repository._prepare_article_data(sample_article_data)
        
        assert result[4] == 1

    def test_prepare_article_data_maps_published_at_correctly(self, article_repository, sample_article_data):
        result = article_repository._prepare_article_data(sample_article_data)
        
        assert result[5] == "2024-01-01 10:00:00"

    def test_prepare_article_data_maps_server_id_correctly(self, article_repository, sample_article_data):
        result = article_repository._prepare_article_data(sample_article_data)
        
        assert result[6] == 1

    def test_prepare_article_data_maps_is_hidden_correctly(self, article_repository, sample_article_data):
        result = article_repository._prepare_article_data(sample_article_data)
        
        assert result[7] == 0 