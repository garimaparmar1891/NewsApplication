GET_ALL_KEYWORDS = """
SELECT Id, Word, CategoryId
FROM Keywords
"""

INSERT_KEYWORD = """
INSERT INTO Keywords (Word, CategoryId)
VALUES (?, ?)
"""

DELETE_KEYWORD = """
DELETE FROM Keywords
WHERE Id = ?
"""
