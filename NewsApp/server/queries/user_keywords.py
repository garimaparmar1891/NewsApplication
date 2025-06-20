INSERT_USER_KEYWORD = """
    INSERT INTO UserKeywords (UserId, CategoryId, Keyword)
    VALUES (?, ?, ?)
"""

GET_USER_KEYWORDS = """
    SELECT uk.Id, uk.Keyword, c.Name AS Category
    FROM UserKeywords uk
    JOIN Categories c ON uk.CategoryId = c.Id
    WHERE uk.UserId = ?
"""

DELETE_USER_KEYWORD = """
    DELETE FROM UserKeywords WHERE Id = ? AND UserId = ?
"""

GET_USER_KEYWORD_MAP = """
    SELECT CategoryId, Keyword FROM UserKeywords WHERE UserId = ?
"""
