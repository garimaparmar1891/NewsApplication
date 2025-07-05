GET_TODAY_HEADLINES = """
    SELECT A.Id, A.Title, A.Content, A.Source, A.Url, C.Name as Category, A.PublishedAt
    FROM Articles A
    LEFT JOIN Categories C ON A.CategoryId = C.Id
    WHERE CAST(A.PublishedAt AS DATE) = ?
    AND A.IsHidden = 0
    AND C.IsHidden = 0
    ORDER BY A.PublishedAt DESC
"""

INSERT_ARTICLE = """
    INSERT INTO Articles (Title, Content, Source, Url, CategoryId, PublishedAt, ServerId, IsHidden)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
"""

GET_INSERTED_ARTICLE_ID = """
    SELECT SCOPE_IDENTITY()
"""

SEARCH_ARTICLES_BY_KEYWORD_AND_RANGE = """
    SELECT A.Id, A.Title, A.Content, A.Source, A.Url, C.Name as Category, A.PublishedAt
    FROM Articles A
    LEFT JOIN Categories C ON A.CategoryId = C.Id
    WHERE (A.Title LIKE ? OR A.Content LIKE ?)
    AND A.PublishedAt BETWEEN ? AND ?
    AND A.IsHidden = 0
    AND C.IsHidden = 0
    ORDER BY A.PublishedAt DESC
"""

GET_ARTICLES_BY_RANGE_BASE = """
    SELECT A.Id, A.Title, A.Content, A.Source, A.Url, C.Name AS Category, A.PublishedAt
    FROM Articles A
    LEFT JOIN Categories C ON A.CategoryId = C.Id
    WHERE A.PublishedAt BETWEEN ? AND ?
    AND A.IsHidden = 0
    AND C.IsHidden = 0
    {category_clause}
    ORDER BY A.PublishedAt DESC
"""

INSERT_READ_HISTORY = """
    INSERT INTO ArticleReadHistory (UserId, ArticleId, ReadAt)
    VALUES (?, ?, GETDATE())
"""

GET_ARTICLE_BY_ID = """
    SELECT A.Id, A.Title, A.Content, A.Source, A.Url, C.Name as Category, A.PublishedAt
    FROM Articles A
    LEFT JOIN Categories C ON A.CategoryId = C.Id
    WHERE A.Id = ?
"""

GET_ALL_ARTICLES = """
    SELECT A.Id, A.Title, A.Content, A.Source, A.Url, C.Name as Category, A.PublishedAt
    FROM Articles A
    LEFT JOIN Categories C ON A.CategoryId = C.Id
    WHERE A.IsHidden = 0
    AND C.IsHidden = 0
    ORDER BY A.PublishedAt DESC
"""

GET_ARTICLE_BY_TITLE = """
    SELECT Id FROM Articles WHERE Title = ?
"""

CHECK_ARTICLE_DUPLICATE = """
    SELECT Id FROM Articles 
    WHERE (Title = ? OR Url = ?) 
    AND PublishedAt = ?
"""

GET_READ_HISTORY = """
    SELECT ArticleId, ReadAt
    FROM ArticleReadHistory
    WHERE UserId = ?
    ORDER BY ReadAt DESC
"""
