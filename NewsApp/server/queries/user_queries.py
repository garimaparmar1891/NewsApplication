GET_USER_BY_EMAIL = """
SELECT Id, Username, Email, PasswordHash, Role FROM Users WHERE Email = ?
"""

GET_USER_BY_ID = """
SELECT Id, Username, Email FROM Users WHERE Id = ?
"""

CREATE_USER = """
INSERT INTO Users (Username, Email, PasswordHash) VALUES (?, ?, ?)
"""

GET_SAVED_ARTICLES = """
SELECT A.Id, A.Title, A.Content, A.Source, A.Url, C.Name AS Category, A.PublishedAt
FROM SavedArticles SA
JOIN Articles A ON SA.ArticleId = A.Id
JOIN Categories C ON A.CategoryId = C.Id
WHERE SA.UserId = ?
ORDER BY A.PublishedAt DESC
"""

UNSAVE_ARTICLE = """
DELETE FROM SavedArticles WHERE UserId = ? AND ArticleId = ?
"""

CHECK_ARTICLE_SAVED = """
SELECT 1 FROM SavedArticles WHERE UserId = ? AND ArticleId = ?
"""
