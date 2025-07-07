import pytest
from unittest.mock import Mock, patch, MagicMock
from repositories.article_visibility_repository import ArticleVisibilityRepository
from queries import article_visibility_queries as q
from queries import category_queries as cq
from constants import messages
import pyodbc


class TestArticleVisibilityRepository:
    
    @pytest.fixture
    def repository(self):
        return ArticleVisibilityRepository()
    
    @pytest.fixture
    def mock_reported_article_row(self):
        mock_row = Mock()
        mock_row.cursor_description = [('ArticleId',), ('UserId',), ('Username',), ('Email',), ('Reason',)]
        mock_row.__getitem__ = lambda self, key: [1, 1, 'testuser', 'test@example.com', 'Inappropriate content'][key]
        return mock_row
    
    @pytest.fixture
    def mock_blocked_keyword_row(self):
        mock_row = Mock()
        mock_row.cursor_description = [('Id',), ('Keyword',)]
        mock_row.__getitem__ = lambda self, key: [1, 'spam'][key]
        return mock_row

    @patch('repositories.article_visibility_repository.execute_write_query')
    def test_add_report_calls_execute_with_correct_parameters(self, mock_execute, repository):
        article_id = 1
        user_id = 2
        reason = "Inappropriate content"
        
        repository.add_report(article_id, user_id, reason)
        
        mock_execute.assert_called_once_with(q.ADD_ARTICLE_REPORT, (article_id, user_id, reason), messages.DB_ERROR_ADD_REPORT)

    @patch('repositories.article_visibility_repository.execute_write_query')
    def test_add_report_raises_value_error_on_duplicate_report(self, mock_execute, repository):
        mock_execute.side_effect = pyodbc.IntegrityError("UQ_User_Article_in_RA")
        
        with pytest.raises(ValueError, match="You have already reported this article."):
            repository.add_report(1, 1, "test")

    @patch('repositories.article_visibility_repository.fetch_all_query')
    def test_get_all_reported_articles_calls_fetch_with_correct_query(self, mock_fetch, repository):
        mock_fetch.return_value = []
        
        repository.get_all_reported_articles()
        
        mock_fetch.assert_called_once_with(q.GET_ALL_REPORTED_ARTICLES, mock_fetch.call_args[0][1], messages.DB_ERROR_GET_REPORTED_ARTICLES)

    @patch('repositories.article_visibility_repository.fetch_one_query')
    def test_get_report_count_returns_zero_when_no_reports(self, mock_fetch, repository):
        mock_fetch.return_value = None
        
        result = repository.get_report_count(1)
        
        assert result == 0

    @patch('repositories.article_visibility_repository.fetch_one_query')
    def test_get_report_count_returns_actual_count(self, mock_fetch, repository):
        mock_fetch.return_value = (5,)
        
        result = repository.get_report_count(1)
        
        assert result == 5

    @patch('repositories.article_visibility_repository.execute_write_query')
    def test_hide_article_calls_execute_with_correct_parameters(self, mock_execute, repository):
        article_id = 1
        
        repository.hide_article(article_id)
        
        mock_execute.assert_called_once_with(q.HIDE_ARTICLE, (article_id,), messages.DB_ERROR_HIDE_ARTICLE)

    @patch('repositories.article_visibility_repository.execute_write_query')
    def test_unhide_article_calls_execute_with_correct_parameters(self, mock_execute, repository):
        article_id = 1
        
        repository.unhide_article(article_id)
        
        mock_execute.assert_called_once_with(q.UNHIDE_ARTICLE, (article_id,), messages.DB_ERROR_UNHIDE_ARTICLE)

    @patch('repositories.article_visibility_repository.execute_write_query')
    def test_hide_category_calls_execute_with_correct_parameters(self, mock_execute, repository):
        category_id = 1
        
        repository.hide_category(category_id)
        
        mock_execute.assert_called_once_with(q.HIDE_CATEGORY, (category_id,), messages.DB_ERROR_HIDE_CATEGORY)

    @patch('repositories.article_visibility_repository.execute_write_query')
    def test_unhide_category_calls_execute_with_correct_parameters(self, mock_execute, repository):
        category_id = 1
        
        repository.unhide_category(category_id)
        
        mock_execute.assert_called_once_with(q.UNHIDE_CATEGORY, (category_id,), messages.DB_ERROR_UNHIDE_CATEGORY)

    @patch('repositories.article_visibility_repository.execute_write_query')
    def test_add_blocked_keyword_calls_execute_with_correct_parameters(self, mock_execute, repository):
        keyword = "spam"
        
        repository.add_blocked_keyword(keyword)
        
        mock_execute.assert_called_once_with(q.ADD_BLOCKED_KEYWORD, (keyword,), messages.DB_ERROR_ADD_BLOCKED_KEYWORD)

    @patch('repositories.article_visibility_repository.fetch_all_query')
    def test_get_blocked_keywords_calls_fetch_with_correct_query(self, mock_fetch, repository):
        mock_fetch.return_value = []
        
        repository.get_blocked_keywords()
        
        mock_fetch.assert_called_once_with(q.GET_BLOCKED_KEYWORDS, mock_fetch.call_args[0][1], messages.DB_ERROR_GET_BLOCKED_KEYWORDS)

    def test_is_keyword_blocked_returns_true_when_keyword_found(self, repository):
        with patch.object(repository, 'get_blocked_keywords') as mock_get_keywords:
            mock_get_keywords.return_value = [{"Keyword": "spam"}, {"Keyword": "scam"}]
            
            result = repository.is_keyword_blocked("This is a spam message")
            
            assert result is True

    def test_is_keyword_blocked_returns_false_when_no_keyword_found(self, repository):
        with patch.object(repository, 'get_blocked_keywords') as mock_get_keywords:
            mock_get_keywords.return_value = [{"Keyword": "spam"}, {"Keyword": "scam"}]
            
            result = repository.is_keyword_blocked("This is a normal message")
            
            assert result is False

    @patch('repositories.article_visibility_repository.fetch_one_query')
    def test_article_exists_returns_true_when_article_found(self, mock_fetch, repository):
        mock_fetch.return_value = (1,)
        
        result = repository.article_exists(1)
        
        assert result is True

    @patch('repositories.article_visibility_repository.fetch_one_query')
    def test_article_exists_returns_false_when_article_not_found(self, mock_fetch, repository):
        mock_fetch.return_value = None
        
        result = repository.article_exists(999)
        
        assert result is False

    @patch('repositories.article_visibility_repository.execute_write_query')
    def test_clear_article_reports_calls_execute_with_correct_parameters(self, mock_execute, repository):
        article_id = 1
        
        repository.clear_article_reports(article_id)
        
        mock_execute.assert_called_once_with(q.CLEAR_ARTICLE_REPORTS, (article_id,), messages.DB_ERROR_CLEAR_REPORTS)

    @patch('repositories.article_visibility_repository.execute_write_query')
    def test_delete_blocked_keyword_returns_affected_rows(self, mock_execute, repository):
        mock_execute.return_value = 1
        
        result = repository.delete_blocked_keyword(1)
        
        assert result == 1

    @patch('repositories.article_visibility_repository.fetch_all_query_with_params')
    def test_get_user_reported_articles_calls_fetch_with_correct_parameters(self, mock_fetch, repository):
        user_id = 1
        mock_fetch.return_value = []
        
        repository.get_user_reported_articles(user_id)
        
        mock_fetch.assert_called_once_with(q.GET_USER_REPORTED_ARTICLES, mock_fetch.call_args[0][1], messages.DB_ERROR_GET_USER_REPORTED, (user_id,))

    @patch('repositories.article_visibility_repository.get_db_connection')
    def test_unhide_articles_after_keyword_removal_commits_changes(self, mock_connection, repository):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.side_effect = [
            [Mock(Id=1, CategoryId=1, Title="Test", Content="Content", IsHidden=1)],
            [Mock(Keyword="spam")]
        ]
        mock_cursor.fetchone.return_value = (0,)
        mock_connection.return_value.__enter__.return_value = mock_conn
        
        repository.unhide_articles_after_keyword_removal()
        
        mock_conn.commit.assert_called_once()

    @patch('repositories.article_visibility_repository.get_db_connection')
    def test_unhide_articles_after_keyword_removal_executes_unhide_for_eligible_articles(self, mock_connection, repository):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.side_effect = [
            [Mock(Id=1, CategoryId=1, Title="Test", Content="Content", IsHidden=1)],
            []
        ]
        mock_cursor.fetchone.return_value = (0,)
        mock_connection.return_value.__enter__.return_value = mock_conn
        
        repository.unhide_articles_after_keyword_removal()
        
        mock_cursor.execute.assert_called_with(q.UNHIDE_ARTICLE, (1,))
