import pytest
from unittest.mock import patch
from services.user_keyword_service import UserKeywordService
from utils.custom_exceptions import AppError
from http import HTTPStatus

class TestUserKeywordService:

    @pytest.fixture(autouse=True)
    def setup(self):
        with patch('services.user_keyword_service.UserKeywordRepository') as MockRepo:
            self.repo = MockRepo.return_value
            self.service = UserKeywordService()
            yield

    def test_add_user_keyword_raises_conflict(self):
        self.repo.check_user_keyword_exists.return_value = True
        data = {'category_id': 1, 'word': 'test'}
        with pytest.raises(AppError) as exc:
            self.service.add_user_keyword(1, data)
        assert exc.value.status_code == HTTPStatus.CONFLICT

    def test_delete_user_keyword_raises_not_found(self):
        self.repo.delete_user_keyword.return_value = 0
        with pytest.raises(AppError) as exc:
            self.service.delete_user_keyword(1, 2)
        assert exc.value.status_code == HTTPStatus.NOT_FOUND

    def test_add_user_keyword_missing_fields(self):
        data = {'category_id': 1}
        with pytest.raises(AppError) as exc:
            self.service.add_user_keyword(1, data)
        assert exc.value.status_code == HTTPStatus.BAD_REQUEST

    def test_clean_and_validate_keyword_returns_cleaned(self):
        result = self.service._clean_and_validate_keyword('  test  ')
        assert result == 'test'

    def test_check_keyword_exists_raises(self):
        self.repo.check_user_keyword_exists.return_value = True
        with pytest.raises(AppError) as exc:
            self.service._check_keyword_exists(1, 1, 'test')
        assert exc.value.status_code == HTTPStatus.CONFLICT

    def test_check_keyword_exists_no_raise(self):
        self.repo.check_user_keyword_exists.return_value = False
        self.service._check_keyword_exists(1, 1, 'test')
        assert True

    def test_insert_keyword_raises(self):
        self.repo.insert_user_keyword.return_value = 0
        with pytest.raises(AppError) as exc:
            self.service._insert_keyword(1, 1, 'test')
        assert exc.value.status_code == HTTPStatus.INTERNAL_SERVER_ERROR

    def test_insert_keyword_no_raise(self):
        self.repo.insert_user_keyword.return_value = 1
        self.service._insert_keyword(1, 1, 'test')
        assert True
