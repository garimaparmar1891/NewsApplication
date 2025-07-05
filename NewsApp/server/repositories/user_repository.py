from utils.db import fetch_one_query, fetch_all_query, fetch_all_query_with_params, execute_write_query
from queries import user_queries as q
import pyodbc
from constants import messages
from utils.custom_exceptions import AppError
from http import HTTPStatus

class UserRepository:
    def save_article(self, user_id, article_id):
        self._validate_article_exists(article_id)
        self._validate_article_not_hidden(article_id)
        self._insert_saved_article(user_id, article_id)
        return True

    def unsave_article(self, user_id, article_id):
        affected_rows = execute_write_query(q.UNSAVE_ARTICLE, (user_id, article_id), messages.DB_ERROR_UNSAVE_ARTICLE)
        return affected_rows

    def is_article_saved_by_user(self, user_id, article_id):
        result = fetch_one_query(q.CHECK_ARTICLE_SAVED, (user_id, article_id))
        return result is not None

    def get_saved_articles(self, user_id):
        return fetch_all_query_with_params(
            q.GET_SAVED_ARTICLES, 
            self._map_row_to_dict, 
            messages.DB_ERROR_GET_SAVED_ARTICLES, 
            (user_id,)
        )

    def get_visible_article_ids(self, article_ids):
        if not article_ids:
            return set()
        placeholders = ','.join(['?'] * len(article_ids))
        query = q.GET_VISIBLE_ARTICLE_IDS(placeholders)
        rows = fetch_all_query_with_params(query, lambda row: row[0], messages.DB_ERROR_GET_VISIBLE_ARTICLE_IDS, article_ids)
        return set(rows)

    def get_saved_article_ids(self, user_id):
        return [row[0] for row in fetch_all_query_with_params(
            q.GET_SAVED_ARTICLE_IDS,
            lambda row: row,
            messages.DB_ERROR_GET_SAVED_ARTICLE_IDS,
            (user_id,)
        )]

    def _validate_article_exists(self, article_id):
        row = fetch_one_query(q.GET_ARTICLE_IS_HIDDEN, (article_id,))
        if row is None:
            raise AppError(messages.ARTICLE_NOT_FOUND, HTTPStatus.NOT_FOUND)

    def _validate_article_not_hidden(self, article_id):
        row = fetch_one_query(q.GET_ARTICLE_IS_HIDDEN, (article_id,))
        if row and row[0] == 1:
            raise AppError(messages.ARTICLE_HIDDEN_ERROR, HTTPStatus.BAD_REQUEST)

    def _insert_saved_article(self, user_id, article_id):
        try:
            execute_write_query(
                q.SAVE_ARTICLE,
                (user_id, article_id, user_id, article_id),
                messages.DB_ERROR_SAVE_ARTICLE
            )
        except pyodbc.IntegrityError as e:
            if "FOREIGN KEY constraint" in str(e):
                raise AppError(messages.ARTICLE_NOT_FOUND, HTTPStatus.NOT_FOUND)
            raise AppError(str(e), HTTPStatus.INTERNAL_SERVER_ERROR)
        except Exception as e:
            print(f"[Save Article Error]: {e}")
            raise AppError(str(e), HTTPStatus.INTERNAL_SERVER_ERROR)

    def _map_row_to_dict(self, row):
        return {desc[0]: value for desc, value in zip(row.cursor_description, row)}
