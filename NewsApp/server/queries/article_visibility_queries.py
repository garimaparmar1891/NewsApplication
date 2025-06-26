INSERT_REPORT = """
    INSERT INTO ReportedArticles (UserId, ArticleId, Reason)
    VALUES (?, ?, ?)
"""

FETCH_REPORTED_ARTICLES = """
    SELECT * FROM ReportedArticles
"""

UPDATE_ARTICLE_VISIBILITY = """
    UPDATE Articles SET IsHidden = ? WHERE Id = ?
"""

UPDATE_CATEGORY_VISIBILITY = """
    UPDATE Categories SET IsHidden = ? WHERE Id = ?
"""

INSERT_BLOCKED_KEYWORD = """
    INSERT INTO BlockedKeywords (Keyword) VALUES (?)
"""

GET_BLOCKED_KEYWORDS = """
    SELECT Keyword FROM BlockedKeywords
"""
