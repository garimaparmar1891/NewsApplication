GET_TODAY_HEADLINES = """
SELECT A.Id, A.Title, A.Content, A.Source, A.Url, C.Name as Category, A.PublishedAt
FROM Articles A
LEFT JOIN Categories C ON A.CategoryId = C.Id
WHERE CAST(A.PublishedAt AS DATE) = ?
ORDER BY A.PublishedAt DESC
"""

INSERT_ARTICLE = """
INSERT INTO Articles (Title, Content, Source, Url, CategoryId, PublishedAt, ServerId)
VALUES (?, ?, ?, ?, ?, ?, ?)
"""

GET_INSERTED_ARTICLE_ID = "SELECT SCOPE_IDENTITY()"

GET_ALL_ARTICLES = """
SELECT A.Id, A.Title, A.Content, A.Source, A.Url, C.Name as Category, A.PublishedAt
FROM Articles A
LEFT JOIN Categories C ON A.CategoryId = C.Id
ORDER BY A.PublishedAt DESC
"""

GET_CATEGORIES = "SELECT Id, Name FROM Categories ORDER BY Name"

SAVE_ARTICLE = """
IF NOT EXISTS (
    SELECT 1 FROM SavedArticles WHERE UserId = ? AND ArticleId = ?
)
BEGIN
    INSERT INTO SavedArticles (UserId, ArticleId)
    VALUES (?, ?)
END
"""

SEARCH_ARTICLES_BY_KEYWORD_AND_RANGE = """
SELECT A.Id, A.Title, A.Content, A.Source, A.Url, C.Name as Category, A.PublishedAt
FROM Articles A
LEFT JOIN Categories C ON A.CategoryId = C.Id
WHERE (A.Title LIKE ? OR A.Content LIKE ?)
AND A.PublishedAt BETWEEN ? AND ?
ORDER BY A.PublishedAt DESC
"""

GET_ARTICLES_FOR_CATEGORIES_SINCE = """
SELECT A.Id, A.Title, A.Content, A.Source, A.Url, A.CategoryId, A.PublishedAt
FROM Articles A
WHERE A.CategoryId IN ({placeholders})
AND A.PublishedAt > ?
ORDER BY A.PublishedAt DESC
"""

GET_ARTICLES_BY_RANGE_BASE = """
    SELECT A.Id, A.Title, A.Content, A.Source, A.Url, C.Name AS Category, A.PublishedAt
    FROM Articles A
    LEFT JOIN Categories C ON A.CategoryId = C.Id
    WHERE A.PublishedAt BETWEEN ? AND ?
    {category_clause}
    ORDER BY A.PublishedAt DESC
"""
