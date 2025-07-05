ADD_ARTICLE_REPORT = """
    INSERT INTO ReportedArticles (ArticleId, UserId, Reason)
    VALUES (?, ?, ?);
"""

GET_REPORT_COUNT = """
    SELECT COUNT(*) as count FROM ReportedArticles
    WHERE ArticleId = ?;
"""

GET_ALL_REPORTED_ARTICLES = """
    SELECT 
        ra.ArticleId, 
        ra.UserId, 
        u.Username, 
        u.Email, 
        ra.Reason
    FROM ReportedArticles ra
    JOIN Users u ON ra.UserId = u.Id;
"""

HIDE_ARTICLE = """
    UPDATE Articles SET IsHidden = 1 WHERE Id = ?;
"""

UNHIDE_ARTICLE = """
    UPDATE Articles SET IsHidden = 0 WHERE Id = ?;
"""

HIDE_CATEGORY = """
    UPDATE Categories SET IsHidden = 1 WHERE Id = ?;
"""

UNHIDE_CATEGORY = """
    UPDATE Categories SET IsHidden = 0 WHERE Id = ?;
"""

ADD_BLOCKED_KEYWORD = """
    INSERT INTO BlockedKeywords (Keyword) VALUES (?);
"""

GET_BLOCKED_KEYWORDS = """
    SELECT Id, Keyword FROM BlockedKeywords;
"""

ARTICLE_EXISTS = """
    SELECT 1 FROM Articles WHERE Id = ?;
"""

CLEAR_ARTICLE_REPORTS = """
    DELETE FROM ReportedArticles WHERE ArticleId = ?
"""

DELETE_BLOCKED_KEYWORD = """
    DELETE FROM BlockedKeywords WHERE Id = ?
"""

GET_USER_REPORTED_ARTICLES = """
    SELECT ArticleId FROM ReportedArticles WHERE UserId = ?
"""

GET_ALL_ARTICLES_FOR_UNHIDE = """
    SELECT Id, CategoryId, Title, Content, IsHidden FROM Articles
"""
