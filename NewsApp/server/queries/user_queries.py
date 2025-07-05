GET_USER_BY_EMAIL = """
    SELECT Id, Username, Email, PasswordHash, Role FROM Users WHERE Email = ?
"""

GET_USER_BY_ID = """
    SELECT Id, Username, Email FROM Users WHERE Id = ?
"""

CREATE_USER = """
    INSERT INTO Users (Username, Email, PasswordHash, Role)
    VALUES (?, ?, ?, 'User')
"""

GET_SAVED_ARTICLES = """
    SELECT A.Id, A.Title, A.Content, A.Source, A.Url, C.Name AS Category, A.PublishedAt
    FROM SavedArticles SA
    JOIN Articles A ON SA.ArticleId = A.Id
    JOIN Categories C ON A.CategoryId = C.Id
    WHERE SA.UserId = ? AND C.IsHidden = 0
    ORDER BY A.PublishedAt DESC
"""

UNSAVE_ARTICLE = """
    DELETE FROM SavedArticles WHERE UserId = ? AND ArticleId = ?
"""

CHECK_ARTICLE_SAVED = """
    SELECT 1 FROM SavedArticles WHERE UserId = ? AND ArticleId = ?
"""

SAVE_ARTICLE = """
    IF NOT EXISTS (
        SELECT 1 FROM SavedArticles WHERE UserId = ? AND ArticleId = ?
    )
    BEGIN
        INSERT INTO SavedArticles (UserId, ArticleId)
        VALUES (?, ?)
END
"""

GET_ARTICLE_IS_HIDDEN = """
    SELECT IsHidden FROM Articles WHERE Id = ?
"""

GET_VISIBLE_ARTICLE_IDS = lambda placeholders: f"""
    SELECT Id FROM Articles WHERE Id IN ({placeholders}) AND IsHidden = 0
"""

GET_SAVED_ARTICLE_IDS = """
    SELECT ArticleId FROM SavedArticles WHERE UserId = ?
"""

GET_ADMIN_EMAIL = """
    SELECT Email FROM Users WHERE Role = 'Admin' ORDER BY Id ASC
"""
