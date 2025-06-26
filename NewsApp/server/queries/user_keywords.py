CHECK_USER_KEYWORD_EXISTS = """
SELECT 1
FROM UserKeywords
WHERE UserId = ? AND CategoryId = ? AND LOWER(Keyword) = LOWER(?)
"""

INSERT_USER_KEYWORD = """
    INSERT INTO UserKeywords (UserId, CategoryId, Keyword)
    VALUES (?, ?, ?)
"""

GET_USER_KEYWORDS = """
SELECT uk.Id, uk.Keyword, c.Name AS Category
FROM UserKeywords uk
JOIN Categories c ON uk.CategoryId = c.Id
WHERE uk.UserId = ? AND c.IsHidden = 0
"""

DELETE_USER_KEYWORD = """
    DELETE FROM UserKeywords WHERE Id = ? AND UserId = ?
"""

GET_USER_KEYWORD_MAP = """
SELECT uk.CategoryId, uk.Keyword
FROM UserKeywords uk
JOIN Categories c ON uk.CategoryId = c.Id
WHERE uk.UserId = ? AND c.IsHidden = 0
"""
